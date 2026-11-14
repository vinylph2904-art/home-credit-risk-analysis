"""Verify and unpack the bundled MySQL snapshot without overwriting existing SQL."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(4 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def validate(path, expected):
    if path.stat().st_size != expected['bytes'] or file_hash(path) != expected['sha256']:
        raise ValueError(f'Checksum or size mismatch: {path.name}')


def prepare(folder, check_only=False):
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    archive = folder / 'database.sql.gz'
    validate(archive, manifest['files']['database.sql.gz'])
    if check_only:
        print('Database archive checksum verified.')
        return archive
    output = folder / 'database.sql'
    if output.exists():
        validate(output, manifest['uncompressed_sql'])
        print('Existing SQL verified; no file overwritten.')
        return output
    partial = folder / 'database.sql.partial'
    # Exclusive creation also prevents two unpacking processes sharing a file.
    with partial.open('xb') as target:
        try:
            with gzip.open(archive, 'rb') as source:
                for block in iter(lambda: source.read(4 * 1024 * 1024), b''):
                    target.write(block)
        except BaseException:
            target.close()
            partial.unlink()
            raise
    try:
        validate(partial, manifest['uncompressed_sql'])
        # rename on Windows fails if another process has created the final file.
        partial.rename(output)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    print(f'SQL ready: {output}')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true', help='Verify archive without unpacking')
    options = parser.parse_args()
    prepare(ROOT / 'data/database', options.check_only)
