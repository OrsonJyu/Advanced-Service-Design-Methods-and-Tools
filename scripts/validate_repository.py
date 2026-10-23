"""Validate project archive integrity, navigation, coverage and common secret patterns."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import hashlib,json,os,re,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[];hash_checks=0;link_checks=0
def fail(message):errors.append(message)
def load(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def check_file(rel,expected_hash,size=None):
 global hash_checks
 p=(ROOT/rel).resolve()
 if not p.is_relative_to(ROOT):fail(f"Path escapes repository: {rel}");return
 if not p.is_file():fail(f"Missing file: {rel}");return
 data=p.read_bytes()
 if size is not None and len(data)!=size:fail(f"Size mismatch: {rel}")
 if hashlib.sha256(data).hexdigest()!=expected_hash:fail(f"SHA-256 mismatch: {rel}")
 hash_checks+=1
version=(ROOT/"VERSION").read_text().strip()
if not re.fullmatch(r"\d+\.\d+\.\d+",version):fail("Invalid VERSION")
for rel in ["README.md","INDEX.md","CATALOG.md","PROJECT_STATUS.md","AGENTS.md","CHANGELOG.md","project-index.json"]:
 if not (ROOT/rel).is_file():fail(f"Missing handoff entry: {rel}")
src=load("archive/source-manifest.json")
if src["synced_source_files"]!=13 or len(src["files"])!=15:fail("Unexpected initial source coverage")
for r in src["files"]:check_file(r["repository_path"],r["archived_sha256"],r["archived_bytes"])
icloud=load("archive/icloud-manifest.json")
if len(icloud["files"])!=16:fail("Unexpected iCloud source coverage")
for r in icloud["files"]:check_file(r["repository_path"],r["sha256"],r["bytes"])
assets=load("deliverables/figma/2026-10-24/asset-manifest.json")
for r in assets["files"]:check_file(r["path"],r["sha256"],r["bytes"])
derived=load("archive/derived-manifest.json")
for r in derived["files"]:
 check_file(r["path"],r["sha256"],r["bytes"])
 for source in r["source_paths"]:
  if not (ROOT/source).is_file():fail(f"Missing reading-copy input: {source}")
presentation=load("deliverables/figma/2026-10-24/presentation.json")
if presentation["slideCount"]!=36 or len(presentation["slides"])!=36:fail("Presentation coverage changed")
for name in ["research-board","case-study","final-presentation","mo-app-prototype","pre-slides-make","mo-dream-maker"]:
 data=load(f"deliverables/figma/2026-10-24/{name}.json")
 if not data.get("roots") or not data.get("texts"):fail(f"Empty Figma snapshot: {name}")
for rel in ["README.md","PROJECT_STATUS.md","CHANGELOG.md","INDEX.md"]:
 if version not in (ROOT/rel).read_text(encoding="utf-8"):fail(f"Version missing in {rel}")
catalog=load("catalog.json")
if catalog["archive_version"]!=version:fail("Catalogue VERSION mismatch")
actual=set()
for directory,dirs,names in os.walk(ROOT):
 dirs[:]=[d for d in dirs if d not in {".git","__pycache__",".venv","node_modules","tmp",".cache"}]
 for name in names:
  p=Path(directory)/name;rel=p.relative_to(ROOT).as_posix()
  if rel not in set(catalog["self_exclusions"]):actual.add(rel)
listed={r["path"] for r in catalog["files"]}
if actual!=listed:fail(f"Catalogue stale: unlisted={sorted(actual-listed)}, missing={sorted(listed-actual)}")
for r in catalog["files"]:check_file(r["path"],r["sha256"],r["bytes"])
for rel in sorted(actual|{"CATALOG.md"}):
 p=ROOT/rel
 if p.suffix==".md":
  raw=rel.startswith(("records/context/","archive/import-notes/")) or (rel.startswith("records/conversations/") and p.name!="README.md")
  if not raw:
   text=re.sub(r"```.*?```","",p.read_text(encoding="utf-8"),flags=re.S)
   for match in re.finditer(r"!?\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)",text):
    target=match.group(1).strip().strip("<>").split(" ",1)[0]
    if not target or target.startswith("#") or urlsplit(target).scheme:continue
    path=unquote(target.split("#",1)[0])
    if not (p.parent/path).resolve().is_file():fail(f"Broken internal link: {rel} -> {path}")
    link_checks+=1
 if p.suffix.lower() in {".md",".json",".txt",".py",".js",".css",".html",".svg"}:
  text=p.read_text(encoding="utf-8",errors="replace")
  patterns={
   "GitHub credential":r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})",
   "OpenAI credential":r"sk-[A-Za-z0-9_-]{24,}",
   "private key":r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
   "unredacted authentication parameter":r"(?:flow_id|user_code)=(?!\[REDACTED-AUTH\])[^&\s]+",
   "temporary Figma asset URL":r"https://www\.figma\.com/api/mcp/asset/",
  }
  for name,pattern in patterns.items():
   if re.search(pattern,text):fail(f"{name} found in {rel}")
 if p.stat().st_size>=100*1024*1024:fail(f"File exceeds archive single-file threshold: {rel}")
html=(ROOT/"prototypes/mo-room-preferences/index.html").read_text(encoding="utf-8")
for ref in re.findall(r'(?:src|href)=["\x27]([^"\x27]+)',html):
 if not urlsplit(ref).scheme and not ref.startswith("#") and not (ROOT/"prototypes/mo-room-preferences"/ref).is_file():fail(f"Missing prototype resource: {ref}")
if errors:
 print("\n".join("FAIL "+e for e in errors));sys.exit(1)
print(f"PASS: {len(actual)} catalogued files, {hash_checks} checksum checks, {link_checks} internal links; source coverage, version, prototype resources and common-secret scan passed.")
