"""Check published-page discoverability and metadata without network access."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1] / 'public'
seen_titles = set()
canonical_urls = set()
for page in sorted(root.glob('*.html')):
    source = page.read_text()
    titles = re.findall(r'<title>(.*?)</title>', source)
    canonicals = re.findall(r'<link rel="canonical" href="([^"]+)"', source)
    assert len(titles) == len(canonicals) == 1, page.name
    assert titles[0] not in seen_titles, f'Duplicate title: {page.name}'
    seen_titles.add(titles[0])
    canonical_urls.add(canonicals[0])
    assert len(re.findall(r'<h1(?:\s|>)', source)) == 1, page.name
    assert re.search(r'<meta name="description" content="[^"]+"', source), page.name
    for payload in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', source, re.S):
        schema = json.loads(payload)
        if page.name in ('index.html', 'privacy.html'):
            assert schema['@type'] != 'WebApplication', page.name
    for href in re.findall(r'(?:href|src)="(/[^"?#]*)', source):
        target = root / (href.lstrip('/') or 'index.html')
        assert target.exists() or target.with_suffix('.html').exists(), (page.name, href)
    for field_id in re.findall(r'<label for="([^"]+)"', source):
        assert f'id="{field_id}"' in source, (page.name, field_id)
sitemap = ET.parse(root / 'sitemap.xml')
urls = [node.text for node in sitemap.findall('.//{*}loc')]
assert len(urls) == len(set(urls)), 'Duplicate sitemap URL'
assert set(urls) <= canonical_urls, 'Sitemap URL has no matching canonical page'
assert canonical_urls - set(urls) <= {'https://getkerfcalc.com/privacy'}, 'Public page missing from sitemap'
print(f'PASS: {len(seen_titles)} pages; titles, descriptions, canonical URLs, schema, internal assets, labels and sitemap.')
