"""Import the owner-provided iCloud project directory without changing originals."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAP={
"文字转写_散人的快速会议_503182587.pdf":"research/raw/assistant-interview-transcript.pdf",
"香港理工大学-MO service.m4a":"research/raw/kate-interview-audio.m4a",
"Annual Report.pdf":"references/client/annual-report.pdf",
"main-logo-3x.png":"assets/brand/mo-logo.png",
"MO_GXP_ Profile & Preferences in Action_v3April.pptx":"references/client/mo-gxp-profile-preferences-v3-april.pptx",
"SD5412_Advanced Service Design Methods and Tools.pdf":"references/course/sd5412-syllabus.pdf",
"SD5412_PROJECT_CONTEXT.md":"records/context/2026-10-05-project-context.md",
"SD5412-S01-handout.pdf":"references/course/sd5412-s01-handout.pdf",
"SD5412-S01-slides-compressed.pdf":"references/course/sd5412-s01-slides.pdf",
"SD5412-S02-handout-mandarin-oriental-team-copy(1).pdf":"references/course/sd5412-s02-mandarin-oriental-team.pdf",
"The Hong Kong Polytechnic University MO interview.m4a":"research/raw/mo-interview-english.m4a",
"yingying-li-Q9A4cNBhz9Q-unsplash.jpg":"assets/reference/yingying-li-Q9A4cNBhz9Q-unsplash.jpg",
"mo-room-prototype/.openai/hosting.json":"archive/import-notes/historical-hosting.json",
"mo-room-prototype/dist/app.js":"prototypes/mo-room-preferences/app.js",
"mo-room-prototype/dist/index.html":"prototypes/mo-room-preferences/index.html",
"mo-room-prototype/dist/style.css":"prototypes/mo-room-preferences/style.css",
}
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--source-dir",type=Path,required=True);a=p.parse_args()
 existing=json.loads((ROOT/"archive/source-manifest.json").read_text(encoding="utf-8"))
 by_hash={r["archived_sha256"]:r["repository_path"] for r in existing["files"]}
 actual={s.relative_to(a.source_dir).as_posix() for s in a.source_dir.rglob("*") if s.is_file()}
 if actual!=set(MAP): raise ValueError(f"Review changed source inventory: added={sorted(actual-set(MAP))}, missing={sorted(set(MAP)-actual)}")
 rows=[]
 for i,(rel,dest) in enumerate(MAP.items(),1):
  source=a.source_dir/rel;data=source.read_bytes();digest=sha(data)
  canonical=by_hash.get(digest,dest);target=(ROOT/canonical).resolve()
  if not target.is_relative_to(ROOT):raise ValueError("Unsafe destination")
  reused=target.exists()
  if reused and target.read_bytes()!=data:raise ValueError(f"Conflicting archive: {canonical}")
  target.parent.mkdir(parents=True,exist_ok=True)
  if not reused:target.write_bytes(data)
  if sha(source.read_bytes())!=digest:raise RuntimeError("Source changed during copy")
  rows.append({"id":f"C{i:02}","original_relative_path":rel,"repository_path":canonical,"bytes":len(data),"sha256":digest,"transformation":"byte-for-byte copy","reused_existing_copy":reused})
 (ROOT/"archive/icloud-manifest.json").write_text(json.dumps({"schema_version":1,"imported_on":"2026-10-24","timezone":"Asia/Hong_Kong","source":"Owner-provided iCloud project directory","files":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
 print(f"Accounted for {len(rows)} iCloud files: {sum(r['reused_existing_copy'] for r in rows)} reused, {sum(not r['reused_existing_copy'] for r in rows)} newly copied.")
if __name__=="__main__":main()
