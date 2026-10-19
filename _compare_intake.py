"""Compare preserved intake with newly verified official text, separating the editorial footnote."""
from pathlib import Path
import hashlib, json, re
W = Path(__file__).resolve().parent
old = W/'sources/intake-2026-10-01.md'
s = old.read_text()
units = {u['id']:u for u in map(json.loads,(W/'units.jsonl').read_text().splitlines())}
heads = list(re.finditer(r'^#### § (\d+[a-z]?) (.*)$',s,re.M))
def norm(x):
    x=re.sub(r'^\|(?:\s*---\s*\|)+\s*$', '', x, flags=re.M)
    return re.sub(r'[\s|]', '', x)
changes = []
for i,h in enumerate(heads):
    t = s[h.end():heads[i+1].start() if i+1<len(heads) else len(s)]
    t = re.split(r'^### ', t, flags=re.M)[0].strip()
    uid = 'p'+h[1]; u=units[uid]
    if not t:
        t=h[2]
    notes_ok = None
    if uid == 'p25':
        marker = 'Diese Vorschrift betrifft die Fortführung'
        body, sep, footnote = t.partition(marker)
        assert sep
        t=body.strip()
        notes_ok=norm(marker+footnote)==norm(u['notes'][0])
    same=norm(t)==norm(u['text'])
    item=dict(id=uid, same_statutory_text_ignoring_layout=same)
    if notes_ok is not None:
        item.update(editorial_footnote_unchanged=notes_ok, presentation_change='Previously appended footnote is now separately identified from operative text.')
    if not same:
        item.update(old_text=t,new_text=u['text'])
    changes.append(item)
report=dict(intake_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),
 official_xml_sha256=hashlib.sha256((W/'sources/BJNR004290962.xml').read_bytes()).hexdigest(),
 comparison='Complete numbered units, with § 25 editorial footnote separated on both sides; whitespace, table separator pipes and syntactic Markdown table rule rows ignored.',
 intake_unit_count=len(heads), verified_unit_count=len(units), units=changes,
 no_substantive_text_change=(len(heads)==len(units) and all(x['same_statutory_text_ignoring_layout'] for x in changes)
                            and all(x.get('editorial_footnote_unchanged',True) for x in changes)))
(W/'sources/change-map.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Intake comparison:', report['no_substantive_text_change'])
raise SystemExit(not report['no_substantive_text_change'])
