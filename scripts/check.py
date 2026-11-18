"""Controlla HTML generato, risorse locali, ancore e protezioni della demo."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = '/rossovento-autotrasporti-demo/'


class Inspect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.labels = []
        self.errors = []
        self.h1s = 0
        self.in_json = False
        self.json_data = []
        self.external_scripts = []
        self.form = False

    def handle_starttag(self, tag, attrs):
        names = [name for name, value in attrs]
        if len(names) != len(set(names)):
            self.errors.append(f'Duplicate attribute on {tag}')
        values = dict(attrs)
        if 'id' in values:
            if values['id'] in self.ids:
                self.errors.append(f'Duplicate ID: {values["id"]}')
            self.ids.add(values['id'])
        if tag == 'h1':
            self.h1s += 1
        for attr in ('href', 'src'):
            if values.get(attr):
                self.refs.append(values[attr])
        if values.get('srcset'):
            self.refs.extend(item.strip().split()[0] for item in values['srcset'].split(','))
        if tag == 'label' and 'for' in values:
            self.labels.append(values['for'])
        if tag == 'script':
            self.in_json = values.get('type') == 'application/ld+json'
            if values.get('src', '').startswith(('http://', 'https://')):
                self.external_scripts.append(values['src'])
        if tag == 'form':
            self.form = 'data-request-form' in values
        if self.form and tag == 'button' and values.get('type') == 'submit' and 'disabled' not in values:
            self.errors.append('Request submit must start disabled until the local script is ready')

    def handle_endtag(self, tag):
        if tag == 'form':
            self.form = False
        if tag == 'script':
            self.in_json = False

    def handle_data(self, data):
        if self.in_json:
            self.json_data.append(data)


def main():
    documents = {}
    failures = []
    for file in ROOT.glob('*.html'):
        parsed = Inspect()
        source = file.read_text(encoding='utf-8')
        parsed.feed(source)
        documents[file.name] = parsed
        failures.extend(f'{file.name}: {error}' for error in parsed.errors)
        if parsed.h1s != 1:
            failures.append(f'{file.name}: expected one h1, found {parsed.h1s}')
        if parsed.external_scripts:
            failures.append(f'{file.name}: external runtime script')
        if 'content="noindex, nofollow"' not in source:
            failures.append(f'{file.name}: demo indexing guard missing')
        for data in parsed.json_data:
            try:
                json.loads(data)
            except json.JSONDecodeError:
                failures.append(f'{file.name}: invalid JSON-LD')

    for name, parsed in documents.items():
        for target in parsed.labels:
            if target not in parsed.ids:
                failures.append(f'{name}: label references missing ID {target}')
        for ref in parsed.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            raw = unquote(url.path)
            if raw.startswith(BASE_PATH):
                raw = raw[len(BASE_PATH):]
            path = raw.lstrip('/') or name
            if not (ROOT / path).is_file():
                failures.append(f'{name}: missing local resource {ref}')
                continue
            if url.fragment and path in documents and url.fragment not in documents[path].ids:
                failures.append(f'{name}: missing fragment {ref}')
    result = {'pages': len(documents), 'failures': failures}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
