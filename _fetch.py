"""Capture official HTTP evidence without accepting mislabeled binary documents."""
import datetime, hashlib, json, pathlib, urllib.request, sys
ROOT = pathlib.Path(__file__).resolve().parent
manifest = ROOT / 'sources/verification.json'
data = json.loads(manifest.read_text())
for name, url in [x.split('=', 1) for x in sys.argv[1:]]:
    dest = ROOT / name
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            body = response.read()
            status = response.status
            mime = response.headers.get('Content-Type')
        if dest.suffix == '.pdf':
            assert body.startswith(b'%PDF-'), 'not a PDF'
        elif dest.suffix == '.xml':
            import xml.etree.ElementTree as ET
            ET.fromstring(body)
        elif dest.suffix == '.html':
            assert b'<html' in body.lower(), 'not HTML'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        record = dict(url=url, accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      http_status=status, content_type=mime, sha256=hashlib.sha256(body).hexdigest(),
                      path=name, format_validated=True)
    except Exception as exc:
        record = dict(url=url, accessed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), error=str(exc))
    data['fetches'].append(record)
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(record.get('path', url), record.get('http_status', record.get('error')))
