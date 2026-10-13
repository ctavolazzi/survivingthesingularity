"""Exercise production package validation without writing a package or ZIP.

Four deliberately invalid plans use the real Plan methods and actual local
font notices/artwork. The complete production make_plan is then called once.
Only this edition's package-negative-controls.json evidence is written.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
MODULE = ROOT / 'publication/package.py'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_production():
    spec = importlib.util.spec_from_file_location('sts_production_package', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_fixture(package):
    """A small real-resource plan isolates each rejection from unrelated errors."""
    plan = package.Plan()
    for name in package.FONT_NOTICES:
        plan.copy(package.ASSETS / 'fonts' / name, 'assets/fonts/' + name)
    artwork = package.IMAGES / 'print/intro-nine-stages.svg'
    relative = plan.ref(artwork.as_uri(), package.OUT / 'interior.html', 'probe.html')
    plan.add('probe.html', f'<html><body><img src="{relative}" alt="Nine speculative stages"></body></html>'.encode(),
             'In-memory control fixture; never exported')
    return plan, plan.resources[artwork.resolve()]


def main():
    package = load_production()
    report = {
        'scope': 'Production package validator, deliberately invalid in-memory plans followed by one complete production preflight',
        'version': package.EDITION,
        'production_module': 'publication/package.py',
        'production_module_sha256': sha(MODULE.read_bytes()),
        'export_called': False,
        'controls': {},
        'control_details': {},
        'limits': 'This is an in-memory plan check, not ZIP readback or an offline renderer test. Publication audits may still be finalized after this snapshot; run the production preflight again immediately before export.',
    }
    fixture, resource = valid_fixture(package)

    def rejected(name, operation, expected, mutation, validator):
        try:
            operation()
        except package.PackageError as error:
            message = str(error)
            assert expected in message, (name, 'wrong rejection', message)
            report['controls'][name] = True
            report['control_details'][name] = {
                'mutation': mutation,
                'validator': validator,
                'exception_type': type(error).__name__,
                'rejection': message,
            }
        else:
            raise AssertionError(f'Invalid package control stayed green: {name}')

    missing_asset = copy.deepcopy(fixture)
    removed = missing_asset.files.pop(resource)
    assert removed and any(target == resource for _, target in missing_asset.references)
    rejected('missing_referenced_asset', missing_asset.validate,
             'Missing packaged resource:',
             f'Removed the bytes for {resource} while retaining the real resource reference.',
             'Plan.validate')

    missing_notice = copy.deepcopy(fixture)
    notice = 'assets/fonts/JetBrainsMono-OFL.txt'
    assert b'OPEN FONT LICENSE' in missing_notice.files.pop(notice).upper()
    rejected('missing_font_notices', missing_notice.validate,
             'Missing required font license/provenance: JetBrainsMono-OFL.txt',
             f'Removed only {notice}; other notices and the artwork reference remain valid.',
             'Plan.validate')

    remote = copy.deepcopy(fixture)
    rejected('remote_render_dependency',
             lambda: remote.css('body { background-image: url("https://example.invalid/package-control.png"); }',
                                package.HERE / 'book.css', 'probe.css'),
             'Offline rendering cannot depend on',
             'Passed a remote background-image URL through the production CSS resource parser. No network request is made.',
             'Plan.css -> Plan.ref -> Plan.local_path')

    unsafe = copy.deepcopy(fixture)
    rejected('unsafe_destination',
             lambda: unsafe.add('../package-control.svg', b'<svg xmlns="http://www.w3.org/2000/svg"/>',
                                'In-memory unsafe destination control'),
             'Unsafe package destination:',
             'Tried to add an archive member with a parent-directory traversal.',
             'Plan.add')

    # The unmodified fixture must pass the same validation after the failures.
    fixture.validate()
    report['unmodified_control_fixture_valid'] = True
    report['control_fixture'] = {
        'referenced_asset': resource,
        'asset_sha256': sha(fixture.files[resource]),
        'font_notices': {name: sha(fixture.files['assets/fonts/' + name]) for name in package.FONT_NOTICES},
    }

    # Exactly one full production plan; this function does not invoke export().
    try:
        plan = package.make_plan()
    except Exception as error:
        report['positive_plan'] = {'valid': False, 'exception_type': type(error).__name__, 'error': str(error)}
        target = HERE / 'package-negative-controls.json'
        target.write_text(json.dumps(report, indent=2) + '\n')
        assert json.loads(target.read_text()) == report
        raise
    manifest = json.loads(plan.files['package-manifest.json'])
    report['positive_plan'] = {
        'valid': True,
        'make_plan_calls': 1,
        'files': len(plan.files),
        'bytes': sum(map(len, plan.files.values())),
        'retained_source_images': len(plan.retained),
        'resolved_render_references': len(plan.references),
        'diagnostic_image_placeholders': len(plan.omitted),
        'manuscript_version': manifest['manuscript_version'],
        'package_manifest_sha256': sha(plan.files['package-manifest.json']),
        'snapshot_hashes': {name: sha(data) for name, data in sorted(plan.files.items())
                            if name in ('build.json', 'manuscript/book.json', 'manuscript/baseline-sha256.json')
                            or name.startswith('audits/')},
    }
    assert report['positive_plan']['manuscript_version'] == '0.10.2'
    target = HERE / 'package-negative-controls.json'
    target.write_text(json.dumps(report, indent=2) + '\n')
    assert json.loads(target.read_text()) == report
    print(json.dumps({'controls': report['controls'],
                      'positive_plan': {key: value for key, value in report['positive_plan'].items() if key != 'snapshot_hashes'},
                      'export_called': False}, indent=2))


if __name__ == '__main__':
    main()
