"""Reproducible BauNVO extraction; structural nodes and editorial notes stay separate."""
from pathlib import Path
import hashlib, json, re, xml.etree.ElementTree as ET
W = Path(__file__).resolve().parent
X = W / 'sources/BJNR004290962.xml'
root = ET.parse(X).getroot()
assert root.find('norm/metadaten/jurabk').text == 'BauNVO'

def render(e):
    if e is None:
        return ''
    if e.tag == 'BR':
        return '\n'
    if e.tag in ('FnR', 'Footnotes'):
        return ''
    if e.tag == 'table':
        rows = e.findall('.//row')
        first = rows[0].find('entry') if rows else None
        merge = first is not None and first.get('namest') == 'col1' and first.get('nameend') == 'col2'
        lines = []
        for row in rows:
            cells = [' '.join(render(c).split()) for c in row]
            if merge and not (row[0].get('namest') == 'col1' and row[0].get('nameend') == 'col2'):
                cells = [' '.join(cells[:2])] + cells[2:]
            lines.append('| ' + ' | '.join(cells) + ' |')
        if lines:
            columns = lines[0].count('|') - 1
            lines.insert(1, '| ' + ' | '.join(['---']*columns) + ' |')
        return '\n\n' + '\n'.join(lines) + '\n\n'
    if e.tag == 'row':
        return ' | '.join(' '.join(render(c).split()) for c in e) + '\n'
    out = e.text or ''
    for c in e:
        out += render(c) + (c.tail or '')
    if e.tag in ('P',):
        out += '\n\n'
    elif e.tag == 'DT':
        out += ' '
    elif e.tag in ('DD', 'DL', 'table'):
        out += '\n'
    if e.tag in ('DL', 'table'):
        out = '\n' + out
    return out

def clean(t):
    t = t.replace('\xa0', ' ')
    t = '\n'.join(re.sub(r'[ \t]+', ' ', line).strip() for line in t.splitlines())
    return re.sub(r'\n{3,}', '\n\n', t).strip()

units, structure, dispositions = [], [], []
section = 0
for n in root.findall('norm'):
    m = n.find('metadaten')
    g = m.find('gliederungseinheit')
    if g is not None:
        section += 1
        structure = [' — '.join(filter(None, [g.findtext('gliederungsbez'), g.findtext('gliederungstitel')]))]
        dispositions.append(dict(kind='structure', doknr=n.get('doknr'), title=structure[0]))
        continue
    label = m.findtext('enbez', '')
    if not label.startswith('§ '):
        dispositions.append(dict(kind='metadata' if not label else 'contents', doknr=n.get('doknr'), title=label))
        continue
    title = clean(render(m.find('titel')))
    content = n.find('textdaten/text/Content')
    text = clean(render(content))
    empty = not text
    if empty:
        text = title
    notes = [clean(render(x)) for x in n.findall('textdaten/text/Footnotes/Footnote')]
    if empty:
        notes.append('Die amtliche konsolidierte XML enthält an dieser Stelle nur die Überschrift und keinen Regelungstext. Die Überschrift wird zur Sichtbarkeit der Leerstelle wiedergegeben.')
    unit = dict(id='p'+label[2:], label=label, title=title, chapter=section,
                structure=structure[:], text=text, notes=notes, official_doknr=n.get('doknr'), empty_slot=empty)
    units.append(unit)
(W/'units.jsonl').write_text(''.join(json.dumps(u, ensure_ascii=False)+'\n' for u in units))
canonical = ['# BauNVO — verifizierter konsolidierter Text',
             'Quelle: https://www.gesetze-im-internet.de/baunvo/xml.zip',
             'Stand: Bekanntmachung 21.11.2017; zuletzt Art. 2 G 3.7.2023 I Nr. 176.']
for u in units:
    canonical.extend(['## '+u['label']+' '+u['title'], u['text']])
    canonical.extend(u['notes'])
(W/'sources/canonical.md').write_text('\n\n'.join(canonical)+'\n')
chapters = [
    ('nutzungsarten','Art der baulichen Nutzung (§§ 1–15)'),
    ('nutzungsmass','Maß der baulichen Nutzung (§§ 16–21a)'),
    ('bauweise','Bauweise und überbaubare Grundstücksfläche (§§ 22–23)'),
    ('leerstelle','Weggefallener vierter Abschnitt (§ 24)'),
    ('ueberleitung','Überleitungs- und Schlussvorschriften (§§ 25–27)')]
meta = dict(cc='de', lang='de', repo='Komentar-DE-BAUNVO-1962',
    repo_dir='/Volumes/LaCie/open-commentary/de/Komentar-DE-BAUNVO-1962',
    title='Kommentar zur Baunutzungsverordnung (BauNVO)',source_path=str(W/'sources/canonical.md'),
    intro_file='00-einleitung.md',intro_desc='Fassung, Methode und Anwendung',
    labels=dict(text='Wortlaut der Vorschrift',chapter='Kommentarkapitel',notes='Quellenhinweis'),
    chapters=[dict(n=i+1,slug=s,title=t) for i,(s,t) in enumerate(chapters)])
(W/'meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
(W/'sources/structure-disposition.json').write_text(json.dumps(dispositions,ensure_ascii=False,indent=2)+'\n')
print(f'{len(units)} Paragraphen; {sum(u["empty_slot"] for u in units)} leere Stellen; {section} Abschnitte')
