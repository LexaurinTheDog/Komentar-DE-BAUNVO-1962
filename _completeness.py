"""Independent expected-ID enumeration from official TOC, plus raw-text and hierarchy checks."""
import collections, hashlib, json, re, xml.etree.ElementTree as ET
from pathlib import Path
W = Path(__file__).resolve().parent
raw = W/'sources/BJNR004290962.xml'
r = ET.parse(raw).getroot()
toc_norm = next(n for n in r.findall('norm') if n.findtext('metadaten/enbez') == 'Inhaltsübersicht')
expected = []
for row in toc_norm.findall('.//row'):
    first = row.find('entry')
    if first is not None:
        match = re.fullmatch(r'§\s*(\d+[a-z]?)', ''.join(first.itertext()).strip())
        if match:
            expected.append('p'+match[1])
units = [json.loads(x) for x in (W/'units.jsonl').read_text().splitlines() if x.strip()]
byid = {u['id']:u for u in units}
body_norms = { 'p'+re.sub(r'\s+', '', n.findtext('metadaten/enbez',''))[1:]: n
               for n in r.findall('norm') if n.findtext('metadaten/enbez','').startswith('§') }
def chars(t):
    t = re.sub(r'^\|(?:\s*---\s*\|)+\s*$', '', t, flags=re.M)
    return re.sub(r'[\s|]', '', t)
text_failures, hierarchy_failures, notes_failures, slots = [], [], [], []
for uid, n in body_norms.items():
    if uid not in byid:
        continue
    u = byid[uid]
    content = n.find('textdaten/text/Content')
    plain = ''.join(content.itertext()) if content is not None else ''
    if not plain.strip():
        slots.append(dict(id=uid, official_title=n.findtext('metadaten/titel'), disposition='heading reproduced; no operative text added'))
        plain = n.findtext('metadaten/titel','')
    if chars(plain) != chars(u['text']):
        text_failures.append(uid)
    # Exact numbering from every nested list and paragraph must remain in order.
    for dt in n.findall('textdaten/text/Content//DT'):
        if ''.join(dt.itertext()).strip() not in u['text']:
            hierarchy_failures.append(uid)
    for note in n.findall('textdaten/text/Footnotes/Footnote'):
        if not any(chars(''.join(note.itertext())) == chars(x) for x in u.get('notes', [])):
            notes_failures.append(uid)
parsed = [u['id'] for u in units]
annex_norms = [n.findtext('metadaten/enbez','') for n in r.findall('norm')
               if re.match(r'(Anlage|Anhang|Schlussformel)', n.findtext('metadaten/enbez',''))]
report = dict(official_source='https://www.gesetze-im-internet.de/baunvo/xml.zip',
 source_xml=str(raw.relative_to(W)), source_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),
 expected_identifier_method='Enumerate first-column section labels in official XML TOC independently of _parse.py; cross-check all enbez body norms',
 expected_ids=expected, body_ids=list(body_norms), extracted_ids=parsed,
 expected_count=len(expected), extracted_count=len(parsed),
 missing=sorted(set(expected)-set(parsed)), extra=sorted(set(parsed)-set(expected)),
 duplicates=[x for x,c in collections.Counter(parsed).items() if c>1],
 text_failures=text_failures, hierarchy_failures=hierarchy_failures, note_failures=notes_failures,
 empty_slots=slots, annex_disposition='No operative annex or final formula exists in the official TOC or body norm metadata; § 17 table and § 25 footnote are retained in their provisions.',
 annex_nodes=annex_norms,
 structural_disposition='Five section heading nodes and one TOC node are not statutory commentary units. General text-evidence footnote is recorded in SOURCES.md; § 25 editorial footnote is retained separately.',
 limits='Character comparison disregards whitespace, table separator pipes and syntactic Markdown table rule rows only; it is a textual completeness test, not a legal review of the commentary.')
report['ok'] = (set(expected)==set(body_norms)==set(parsed) and len(expected)==len(set(expected))
                and not any(report[k] for k in ['missing','extra','duplicates','text_failures','hierarchy_failures','note_failures'])
                and not annex_norms)
(W/'completeness-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['expected_count','extracted_count','missing','extra','duplicates','text_failures','hierarchy_failures','note_failures','ok']}))
raise SystemExit(not report['ok'])
