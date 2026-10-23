"""Finalize Figma asset provenance and deduplicate downloaded image/vector bytes."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"deliverables/figma/2026-10-24"
def sha(b):return hashlib.sha256(b).hexdigest()
p=argparse.ArgumentParser(description=__doc__);p.add_argument("--records",type=Path,required=True);args=p.parse_args()
records=json.loads(args.records.read_text(encoding="utf-8"))
aliases={};removed=0;saved=0
for folder in ("source-images","source-vectors"):
 seen={}
 for file in sorted((BASE/folder).glob("*")):
  if not file.is_file():continue
  resolved=file.resolve()
  if not resolved.is_relative_to((BASE/folder).resolve()):raise ValueError("Unsafe path")
  data=file.read_bytes();key=sha(data);rel=file.relative_to(ROOT).as_posix()
  if key in seen:
   aliases[rel]=seen[key];saved+=len(data);file.unlink();removed+=1
  else:seen[key]=rel
for rec in records:
 valid=[]
 for file in rec["files"]:
  if file["path"].endswith(".undefined"):continue
  file["path"]=aliases.get(file["path"],file["path"])
  if not (ROOT/file["path"]).is_file():raise FileNotFoundError(file["path"])
  if file not in valid:valid.append(file)
 rec["files"]=valid
 rec["render_status"]="archived" if any(x["kind"]=="configured-node-export" for x in valid) else "unavailable: original A3 frame is hidden; Figma returned export=null"
physical=[]
for folder in ("visuals","source-images","source-vectors"):
 for f in sorted((BASE/folder).glob("*")):
  if f.is_file():
   data=f.read_bytes();physical.append({"path":f.relative_to(ROOT).as_posix(),"bytes":len(data),"sha256":sha(data)})
manifest={"schema_version":1,"archived_on":"2026-10-24","timezone":"Asia/Hong_Kong","note":"Configured export formats used; no source Figma nodes edited. Temporary signed download URLs excluded.","deduplicated_files":removed,"bytes_saved":saved,"records":sorted(records,key=lambda r:r["slug"]),"files":physical}
(BASE/"asset-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps({"unique_assets":len(physical),"asset_bytes":sum(x["bytes"] for x in physical),"duplicates_removed":removed,"bytes_saved":saved,"unavailable_renders":sum(r["render_status"]!="archived" for r in records)}))
