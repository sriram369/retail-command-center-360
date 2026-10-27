"""Package only portfolio deliverables, with a manifest and CRC verification."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    skip={'.git','node_modules','__pycache__','.venv','workbook_previews'}
    excluded={'workbook_payload.json','operations_payload.json','package_manifest.json','.DS_Store','.env'}
    files=[p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink()
           and not any(x in skip for x in p.relative_to(ROOT).parts)
           and p.name not in excluded and not p.name.endswith(('.pyc','.inspect.ndjson'))]
    manifest=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,
               'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
    mp=ROOT/'reports/package_manifest.json';mp.write_text(json.dumps(manifest,indent=2));files.append(mp)
    target=ROOT.parent/'Retail_Command_Center_360.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(files):z.write(p,Path(ROOT.name)/p.relative_to(ROOT))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
    print(json.dumps({'zip':str(target),'files':len(files),'bytes':target.stat().st_size,'crc_check':'passed'},indent=2))
if __name__=='__main__':main()
