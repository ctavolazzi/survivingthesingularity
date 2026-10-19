#!/usr/bin/env python3
"""Render this decision record as Markdown, CSV and an offline interactive table."""
import csv
import html
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'matrix.json').read_text())
keys = [c['id'] for c in data['criteria']]


def score(row, weights):
    total = sum(weights)
    if total <= 0:
        raise ValueError('At least one weight must be positive')
    return sum(w * row['ratings'][k] for k, w in zip(keys, weights)) * 20 / total


def ranked(weights):
    return sorted(data['options'], key=lambda row: (-score(row, weights), row['id']))


weights = data['presets']['Balanced']
rows = ranked(weights)
md = [
    '# Surviving the Singularity next step decision matrix',
    '',
    data['recommendation'],
    '',
    'Evidence date: ' + data['as_of'] + '.',
    '',
    '**Later findings and concrete packets:** [Read the continuation](CONTINUATION.md). The $5 offer and no-account model were already settled; main has advanced, and the failed browser jobs have been diagnosed. The matrix below retains its original assessment timestamp.',
    '',
    '[Open the standalone decision desk](next-steps.html) | [Original weight explorer](matrix.html) | [Spreadsheet CSV](matrix.csv) | [Full decision data](matrix.json)',
    '',
    'The default is balanced progress: strengthen the book and make the public offer credible. These weights and ratings are my judgments for CT to change, not measured probabilities or a statement of CT\'s priorities.',
    '',
    data['interpretation'],
    '',
    '## What changed the priorities',
    '',
]
for item in data['observations']:
    md.append('- ' + item['fact'] + ' [Evidence](' + item['source'] + ').')
md += ['', 'The October 7 request to define the title is resolved on v0.11.0: its Introduction defines survival in terms of food, housing, care and ownership. That does not update main or the live site automatically. [Introduction](https://github.com/ctavolazzi/survivingthesingularity/blob/d48ed396/src/lib/data/book/02-introduction.md#L33).', '', '## Weights and ratings', '', '| Criterion | Weight | What a high score means |', '| --- | ---: | --- |']
for c in data['criteria']:
    md.append(f"| {c['label']} | {c['weight']}% | {c['definition']} |")
md += ['', 'Rate each criterion from 1 to 5: 1 = little contribution, 3 = meaningful contribution, 5 = direct substantial contribution. For ease, 5 means a small bounded task and 1 means large or uncertain work. Intermediate scores are allowed. **Score = sum(weight × rating ÷ 5)** with weights normalized to 100. The possible range is 20 to 100.', '', data['effort_note'], '', data['dependency_note'], '', '## Weighted matrix', '', 'V = value, T = trust, U = work unlocked, L = learning, E = ease. The score is priority under the chosen weights; phase and dependencies determine scheduling.', '', '| ID | Option | V | T | U | L | E | /100 | Timing |', '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
for r in rows:
    vals = ' | '.join(str(r['ratings'][k]) for k in keys)
    md.append(f"| {r['id']} | {r['option']} | {vals} | {score(r, weights):.0f} | {r['phase']} |")
md += ['', '## Sensitivity to priorities', '', '| Weights | Leading options |', '| --- | --- |']
for name, ws in data['presets'].items():
    top = ', '.join(f"{r['id']} ({score(r, ws):.0f})" for r in ranked(ws)[:8])
    md.append(f"| {name}: {' / '.join(str(w) for w in ws)} | {top} |")
md += ['', 'Weight order is V / T / U / L / E. Offer clarity, delivery and a shared baseline remain near the top in all three scenarios. Learning-first moves reader sessions and the chapter pilot upward; delivery-first moves release checks and edition parity upward. Scores within four points are treated as a group. A one-point change in a value rating moves the default score by six points, so close ranks are not precise distinctions.', '', '## Paths available', '', '| Path | Assessment | Tradeoff |', '| --- | --- | --- |']
for s in data['strategies']:
    md.append(f"| {s['path']} | {s['recommendation']} | {s['tradeoff']} |")
md += ['', '## Recommended sequence', '']
md += [f'{i}. {s}' for i, s in enumerate(data['decision_sequence'], 1)]
md += ['', 'The next author decisions are the working edition, the role of the foreword, the provisional opening/ending, and the exact paid offer. Research, source comparison and narrow engineering checks can proceed alongside those decisions. A free feedback excerpt can precede a paid launch. Publication and outreach remain separate execution decisions.', '', '## Evidence and completion criteria', '']
for r in rows:
    md += [f"### {r['id']} {r['option']}", '', r['evidence'], '', f"**First step:** {r['first_step']}", '', f"**Done when:** {r['acceptance']}", '', f"Owner: {r['owner']}. Effort: {r['effort']}. Evidence confidence: {r['evidence_confidence']}. Dependencies: {', '.join(r['dependencies']) or 'None'}.", '']
    if r.get('conditions'):
        md += [r['conditions'], '']
    md += ['Sources: ' + ', '.join(f'[source {i}]({url})' for i, url in enumerate(r['sources'], 1)) + '.', '']
md += ['## Existing assets worth reusing', '', '- Core cut, block decisions, seams and author voice history: preparation for CT\'s writing and focused review.', '- Site-audit tools, measured fixes, fonts and video-loading work: finish and integrate after checking the current owner\'s diff.', '- Twenty-one scripts, a ledger route and the labor-hour essay: select one experiment; older branches mix editorial changes and dated launch assumptions.', '- Lexical manuscript search: useful editing support without making generated answers a dependency.', '- PDF/EPUB tooling, art and proofs: reuse after the chosen text is stable.', '- MVP components and design documents: reusable patterns; its purchase button is intentionally inert. Game is a separate prototype, and production tracker remains a scaffold.', '', 'No market-demand or conversion result was established here. Existing AI critique counts are hypotheses. HTML inspection does not establish hydrated behavior, and CI status does not establish payment or email delivery. The matrix does not authorize merging, deployment, purchases, or messages to readers.', '']
(ROOT / 'README.md').write_text('\n'.join(md))

buf = io.StringIO(newline='')
writer = csv.writer(buf, lineterminator='\n')
writer.writerow(['id', 'option', *keys, 'balanced_score', 'delivery_first_score', 'learning_first_score', 'phase', 'owner', 'effort', 'evidence_confidence', 'dependencies', 'conditions', 'evidence', 'first_step', 'done_when', 'sources'])
for r in rows:
    writer.writerow([r['id'], r['option'], *[r['ratings'][k] for k in keys], *[round(score(r, ws), 2) for ws in data['presets'].values()], r['phase'], r['owner'], r['effort'], r['evidence_confidence'], '; '.join(r['dependencies']), r.get('conditions', ''), r['evidence'], r['first_step'], r['acceptance'], '; '.join(r['sources'])])
(ROOT / 'matrix.csv').write_text(buf.getvalue())

template = r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>STS next step decision matrix</title>
<style>
:root{color-scheme:light;font:16px/1.5 system-ui,sans-serif;color:#192c32;background:#f4f3ef}body{margin:0}main{max-width:1200px;margin:auto;padding:36px 22px}h1{font-size:clamp(1.8rem,4vw,2.7rem);line-height:1.15;max-width:850px}p{max-width:850px}a{color:#006554}button,select,input{font:inherit}button,select{padding:8px 12px;border:1px solid #7b8985;border-radius:4px;background:white;color:#192c32}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid #006554;outline-offset:3px}.controls{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:20px;margin:24px 0;padding:22px;background:white;border:1px solid #bdc9c3}.control label{display:block;font-weight:600}.control input{width:100%}.note{color:#435853;font-size:.9rem}#status{font-weight:600;min-height:24px}.tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center}.scroll{overflow:auto;background:white;border:1px solid #bdc9c3;margin-top:20px}table{border-collapse:collapse;width:100%;min-width:710px}th,td{padding:12px 14px;border-bottom:1px solid #d9e0dc;text-align:left;vertical-align:top}th{background:#e6ede8;font-size:.85rem;white-space:nowrap}.score{font-size:1.2rem;font-variant-numeric:tabular-nums;font-weight:700;color:#006554}.bar{height:4px;background:#dbe7df;min-width:72px;margin-top:4px}.bar span{height:100%;display:block;background:#006554}summary{cursor:pointer;font-weight:600}details p{margin:10px 0;font-size:.92rem;max-width:630px}.id{display:block;font-size:.78rem;color:#526962}.phase{font-size:.85rem}.small{font-size:.85rem}footer{margin-top:30px;border-top:1px solid #bac9c0;padding-top:12px}.screenreader{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}@media(max-width:600px){main{padding:24px 14px}.controls{padding:16px;gap:12px}th,td{padding:10px}h1{max-width:95%}}@media print{.controls,.tools{display:none}.scroll{overflow:visible}table{min-width:0}main{padding:0}details p{font-size:.8rem}}
</style>
<main><p class="note">October 10, 2026 · Decision support for CT · 27 options</p>
<h1>Where Surviving the Singularity goes next</h1>
<p class="note"><a href="CONTINUATION.md">Read later findings and concrete decision packets</a>. Offer and account rulings were already settled; this matrix retains its original assessment timestamp.</p>
<p>Converge the manuscript and offer, make the reader path dependable, then test an opening and a practical chapter before expanding the rewrite.</p>
<p class="note">Scores are judgments, not probabilities. Treat scores within four points as tied. Dependencies determine sequence, and overlapping scores cannot be added into an ROI. Evidence confidence describes current facts, not expected payoff.</p>
<div class="tools" id="presets" aria-label="Weight presets"></div>
<div class="controls" id="controls"></div>
<p id="status" role="status" aria-live="polite"></p>
<div class="tools"><label for="phase">Show</label><select id="phase"><option value="all">All timing groups</option></select><button id="download">Download current ranking CSV</button><a href="README.md">Read full assessment</a></div>
<p class="note">Weights are normalized automatically. Ratings stay fixed for comparison; edit matrix.json to change the underlying judgments. Open any option for evidence, dependencies and a completion criterion. This file works offline and makes no network requests.</p>
<noscript><p>Enable JavaScript for adjustable rankings, or open <a href="matrix.csv">the static matrix CSV</a>.</p></noscript>
<div class="scroll" role="region" aria-label="Ranked decision matrix" tabindex="0"><table><caption class="screenreader">Ranked options and completion criteria</caption><thead><tr><th scope="col">Rank</th><th scope="col">Option and evidence</th><th scope="col">Score / 100</th><th scope="col">Timing</th><th scope="col">Effort</th></tr></thead><tbody id="rows"></tbody></table></div>
<footer><p class="note">Possible paths: converge and validate; release a selected interim v0.11 edition after the relevant gates; prioritize a full author rewrite; or expand distribution/platform work. The first is the default recommendation. An interim digital release does not require finishing v0.12 or a physical print proof.</p><p class="note">Live-site checks: approximately 06:51 Pacific. Archive coverage has its own 06:15 cutoff; active source work continued afterward. This assessment does not publish or change the book, offer or live site.</p></footer></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const data=JSON.parse(document.querySelector('#data').textContent);
const keys=data.criteria.map(c=>c.id);
const inputs=[];
let current=[];
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const [i,c] of data.criteria.entries()){
 const box=document.createElement('div');box.className='control';
 box.innerHTML=`<label for="w-${c.id}">${escapeHTML(c.label)}</label><input type="range" id="w-${c.id}" min="0" max="100" step="5" value="${c.weight}"><output id="out-${c.id}" for="w-${c.id}"></output>`;
 document.querySelector('#controls').append(box);inputs.push(box.querySelector('input'));inputs[i].addEventListener('input',render);
}
for(const [name,weights] of Object.entries(data.presets)){
 const b=document.createElement('button');b.textContent=name;b.addEventListener('click',()=>{inputs.forEach((input,i)=>input.value=weights[i]);render()});document.querySelector('#presets').append(b);
}
for(const phase of [...new Set(data.options.map(r=>r.phase))]){const o=document.createElement('option');o.value=phase;o.textContent=phase;document.querySelector('#phase').append(o)}
document.querySelector('#phase').addEventListener('change',render);
function render(){
 const ws=inputs.map(i=>Number(i.value));const total=ws.reduce((a,b)=>a+b,0);
 inputs.forEach((input,i)=>document.querySelector('#out-'+keys[i]).textContent=total?`${(ws[i]*100/total).toFixed(1)}% normalized`:'0%');
 if(!total){document.querySelector('#status').textContent='Set at least one weight above zero.';document.querySelector('#rows').innerHTML='';current=[];document.querySelector('#download').disabled=true;return}
 document.querySelector('#download').disabled=false;
 current=data.options.map(r=>({...r,score:keys.reduce((sum,k,i)=>sum+ws[i]*r.ratings[k],0)*20/total})).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
 const phase=document.querySelector('#phase').value;const visible=current.filter(r=>phase==='all'||r.phase===phase);
 document.querySelector('#status').textContent=`${visible.length} of ${current.length} options shown. Highest score: ${current[0].id}, ${current[0].score.toFixed(1)} / 100.`;
 document.querySelector('#rows').innerHTML=visible.map(r=>`<tr data-id="${r.id}"><td>${current.indexOf(r)+1}</td><td><details><summary><span class="id">${r.id}</span>${escapeHTML(r.option)}</summary><p>${escapeHTML(r.evidence)}</p><p><strong>First step:</strong> ${escapeHTML(r.first_step)}</p><p><strong>Done when:</strong> ${escapeHTML(r.acceptance)}</p><p><strong>Dependencies:</strong> ${escapeHTML(r.dependencies.join(', ')||'None')}. ${escapeHTML(r.conditions||'')}</p><p><strong>Owner:</strong> ${escapeHTML(r.owner)}. <strong>Evidence confidence:</strong> ${escapeHTML(r.evidence_confidence)}.</p><p><strong>Ratings:</strong> ${keys.map(k=>`${k} ${r.ratings[k]}`).join(' · ')}</p><p>${r.sources.map((url,i)=>`<a href="${escapeHTML(url)}" target="_blank" rel="noreferrer">Source ${i+1}</a>`).join(' · ')}</p></details></td><td><span class="score">${r.score.toFixed(1)}</span><div class="bar" aria-hidden="true"><span style="width:${r.score}%"></span></div></td><td class="phase">${escapeHTML(r.phase)}</td><td class="small">${escapeHTML(r.effort)}</td></tr>`).join('');
}
document.querySelector('#download').addEventListener('click',()=>{
 const quote=s=>'"'+String(s).replace(/"/g,'""')+'"';const ws=inputs.map(i=>Number(i.value));const total=ws.reduce((a,b)=>a+b,0);
 const lines=[['id','option','score','phase',...keys.map(k=>k+'_weight_percent')],...current.map(r=>[r.id,r.option,r.score.toFixed(2),r.phase,...ws.map(w=>(w*100/total).toFixed(2))])];
 const url=URL.createObjectURL(new Blob([lines.map(row=>row.map(quote).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='sts-current-ranking.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
render();
</script></html>'''
template = template.replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('<', '\\u003c'))
(ROOT / 'matrix.html').write_text(template)
print(f'Rendered {len(rows)} options as README.md, matrix.csv and matrix.html')
