"""Asset URLs follow file content while static responses remain revalidated."""
import hashlib
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

from flask import url_for

from web.app import app
from web import runtime


def test_asset_hash_changes_only_when_content_changes(monkeypatch):
    root = Path(__file__).resolve().parents[1] / 'tmp' / ('asset_test_' + uuid4().hex)
    asset = root / 'web/static/fixture.css'
    asset.parent.mkdir(parents=True)
    asset.write_bytes(b'body { color: blue; }')
    monkeypatch.setattr(runtime, 'ROOT', root)
    with app.test_request_context('/'):
        first = url_for('static', filename='fixture.css')
        assert first == url_for('static', filename='fixture.css', v='obsolete-version')
        assert parse_qs(urlsplit(first).query)['v'] == [hashlib.sha256(asset.read_bytes()).hexdigest()[:16]]
        asset.write_bytes(b'body { color: teal; }')
        assert url_for('static', filename='fixture.css') != first


def test_static_files_remain_public_and_revalidated():
    response = app.test_client().get('/static/login.css')
    assert response.status_code == 200
    assert response.headers['Cache-Control'] == 'no-cache, must-revalidate'


def test_content_versioned_assets_can_be_reused_without_revalidation():
    with app.test_request_context('/'):
        address = url_for('static', filename='login.css')
    response = app.test_client().get(address)
    assert response.status_code == 200
    assert response.headers['Cache-Control'] == 'public, max-age=31536000, immutable'
    stale = app.test_client().get('/static/login.css?v=outdated')
    assert stale.headers['Cache-Control'] == 'no-cache, must-revalidate'
