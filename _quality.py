"""Coverage, repetition and authored-link checks; does not claim legal review."""
import collections, difflib, hashlib, json, re, sys
from pathlib import Path
W=Path(__file__).resolve().parent
meta=json.loads((W/'meta.json').read_text()); O=Path(meta['repo_dir'])
units=[json.loads(x) for x in (W/'units.jsonl').read_text().splitlines()]
blocks={}; delimiters=[]
for f in sorted((W/'commentary').glob('*.md')):
    chunks=re.split(r'^=== (\S+)\s*$',f.read_text(),flags=re.M)
    for i in range(1,len(chunks),2):
        delimiters.append(chunks[i]);blocks[chunks[i]]=chunks[i+1].strip()
duplicates=[x for x,c in collections.Counter(delimiters).items() if c>1]
paragraphs=collections.defaultdict(list)
for uid,text in blocks.items():
    for p in text.split('\n\n'):
        p=re.sub(r'\s+',' ',p).strip()
        if len(p)>100:
            paragraphs[p].append(uid)
repeated=[dict(ids=ids,text=p) for p,ids in paragraphs.items() if len(set(ids))>1]
near=[]
for i,left in enumerate(units):
    for right in units[i+1:]:
        a,b=left['id'],right['id']
        ratio=difflib.SequenceMatcher(None,blocks.get(a,''),blocks.get(b,'')).ratio()
        if ratio>0.65:
            near.append(dict(ids=[a,b],similarity=round(ratio,4)))
output_texts={}
for chapter in O.glob('[0-9][0-9]-*.md'):
    if chapter.name.startswith('00-'):
        continue
    chunks=re.split(r'^### § (\d+[a-z]?).*$',chapter.read_text(),flags=re.M)
    for i in range(1,len(chunks),2):
        quote='\n'.join(line[1:].lstrip() for line in chunks[i+1].splitlines() if line.startswith('>'))
        output_texts['p'+chunks[i]]=quote
normal=lambda s:re.sub(r'\s+',' ',s).strip()
output_mismatch=[u['id'] for u in units if normal(output_texts.get(u['id'],''))!=normal(u['text'])]
files=[p for p in O.glob('*.md')]+[O/'cases'/x for x in ['README.md','4-C-5-16.md','4-C-3-21.md','4-B-2-25.md']]
broken=[];local_count=0;external=set()
for f in files:
    for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
        if url.startswith(('http://','https://')):
            external.add(url);continue
        if url.startswith('#'):
            continue
        local_count+=1
        if not (f.parent/url.split('#')[0]).exists():
            broken.append(dict(file=str(f.relative_to(O)),target=url))
ids={u['id'] for u in units}
short=[u['id'] for u in units if len(blocks.get(u['id'],'')) < (120 if len(u['text'])<160 else 400)]
report=dict(total_units=len(units),commented_units=len(ids&set(blocks)),
 missing=sorted(ids-set(blocks)),extra=sorted(set(blocks)-ids),duplicate_delimiters=duplicates,
 commentary_characters=sum(map(len,blocks.values())),per_unit_characters={k:len(v) for k,v in blocks.items()},
 repeated_long_paragraphs=repeated,short_units=short,broken_local_links=broken,
 near_duplicate_units_over_065=near,output_statutory_text_mismatches=output_mismatch,
 output_numbered_provisions=len(output_texts),
 local_links_checked=local_count,external_urls=sorted(external),
 external_link_policy='Official statute and gazette links verified by captured HTTP 200; court links direct 403 but Firecrawl reports 200 and saved full text; GitHub attribution is a project link, not a legal authority.',
 missing_authority_policy='Only three decisions are cited as verified; units without assigned cases make no claim of separately verified case-law coverage.',
 limitations='No semantic automated proof. Similar subject matter in transition provisions requires manual review; no assertion of independent legal review.')
report['ok']=not any(report[k] for k in ['missing','extra','duplicate_delimiters','repeated_long_paragraphs','near_duplicate_units_over_065','output_statutory_text_mismatches','short_units','broken_local_links'])
(W/'quality-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['total_units','commented_units','commentary_characters','local_links_checked','broken_local_links','repeated_long_paragraphs','short_units','ok']},ensure_ascii=False))
raise SystemExit(not report['ok'])
