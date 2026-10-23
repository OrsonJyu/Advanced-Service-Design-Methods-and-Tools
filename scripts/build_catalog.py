"""Generate the complete human and machine file catalogues (Python standard library)."""
from pathlib import Path
from urllib.parse import quote
import hashlib,json,os
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={"CATALOG.md","catalog.json"}
def files():
 for directory,dirs,names in os.walk(ROOT):
  dirs[:]=sorted(d for d in dirs if d not in {".git","__pycache__",".venv","node_modules","tmp",".cache"})
  for name in sorted(names):
   p=Path(directory)/name
   if p.relative_to(ROOT).as_posix() not in EXCLUDE:yield p
def digest(path):
 h=hashlib.sha256()
 with path.open("rb") as stream:
  for b in iter(lambda:stream.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def category(rel):
 if rel.startswith("docs/") or "/" not in rel:return "01 · 阅读导航与项目说明"
 if rel.startswith("references/"):return "02 · 课程与客户资料"
 if rel.startswith("research/"):return "03 · 研究原始资料"
 if rel.startswith("records/"):return "04 · 历史讨论与项目纪要"
 if rel.startswith("prototypes/"):return "05 · 可运行原型"
 if rel.startswith("deliverables/reading-copies/"):return "06 · 成果阅读 PDF"
 if rel.startswith("deliverables/"):return "07 · Figma 快照与素材"
 if rel.startswith("assets/"):return "08 · 原始视觉附件"
 if rel.startswith("archive/"):return "09 · 来源与验证记录"
 return "10 · 维护工具"
def status(rel):
 if rel.startswith("deliverables/reading-copies/"):return "阅读副本"
 if rel.startswith(("references/","research/raw/","assets/","records/context/","archive/import-notes/")):return "来源副本"
 if rel.startswith("records/conversations/") and not rel.endswith("README.md"):return "历史记录"
 if rel.startswith("deliverables/figma/"):return "日期快照"
 if rel.startswith("prototypes/") and not rel.endswith("README.md"):return "可运行原型原件"
 if rel.startswith("scripts/"):return "维护工具"
 return "整理文档"
def main():
 version=(ROOT/"VERSION").read_text().strip()
 rows=[{"path":p.relative_to(ROOT).as_posix(),"category":category(p.relative_to(ROOT).as_posix()),"status":status(p.relative_to(ROOT).as_posix()),"format":p.suffix.lstrip(".") or "text","bytes":p.stat().st_size,"sha256":digest(p)} for p in files()]
 rows.sort(key=lambda r:(r["category"],r["path"]))
 (ROOT/"catalog.json").write_text(json.dumps({"schema_version":1,"archive_version":version,"generated_on":"2026-10-24","timezone":"Asia/Hong_Kong","self_exclusions":sorted(EXCLUDE),"files":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
 lines=["# 完整文件目录 / Complete file catalogue","",f"归档版本：{version} · 日期：2026-10-24（香港时间）","",f"共 {len(rows)} 个实际文件。先按目的查阅 [INDEX](INDEX.md)，再在这里按目录定位。机器可读路径、大小与 SHA-256 见 [catalog.json](catalog.json)。目录自身不计入清单，以避免自引用校验。",""]
 for cat in sorted({r["category"] for r in rows}):
  group=[r for r in rows if r["category"]==cat]
  lines += [f"## {cat}","",f"{len(group)} 个文件。",""]
  if len(group)>40:lines += ["<details>","<summary>展开完整文件清单</summary>",""]
  lines += ["| 文件路径（可点击） | 格式 | 定位 |","|---|---|---|"]
  for r in group:lines.append(f'| [{r["path"]}]({quote(r["path"],safe="/.-_")}) | {r["format"]} | {r["status"]} |')
  lines.append("")
  if len(group)>40:lines += ["</details>",""]
 lines += ["由 `python scripts/build_catalog.py` 生成。新增、改名或修改文件后请重新生成并运行验证。",""]
 (ROOT/"CATALOG.md").write_text("\n".join(lines),encoding="utf-8",newline="\n")
 print(f"Catalogued {len(rows)} files.")
if __name__=="__main__":main()
