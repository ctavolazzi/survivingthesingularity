/** Deployment must name the exact reviewed private artifact before taking payment. */
export function validateBundleRelease(env, manifest) {
  const bundle = manifest?.bundle;
  if (!bundle?.object || !bundle?.sha256 || !manifest?.book?.version) {
    return { ok: false, error: 'Current bundle manifest is incomplete' };
  }
  if (env.DOWNLOAD_BUNDLE_PATH !== bundle.object
      || env.DOWNLOAD_BUNDLE_SHA256 !== bundle.sha256
      || env.DOWNLOAD_BUNDLE_BOOK_VERSION !== manifest.book.version
      || (env.DOWNLOAD_BUCKET || 'downloads') !== bundle.bucket) {
    return { ok: false, error: 'Reviewed download bundle is not configured' };
  }
  return { ok: true, path: bundle.object, bucket: env.DOWNLOAD_BUCKET || 'downloads' };
}
