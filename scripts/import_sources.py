"""Import source copies without changing the synced project originals (Python 3.10+)."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = [
    ("S01", "SD5412_Advanced Service Design Methods and Tools(2).pdf", "references/course/sd5412-syllabus.pdf"),
    ("S02", "SD5412-S01-handout(3).pdf", "references/course/sd5412-s01-handout.pdf"),
    ("S03", "SD5412-S01-slides-compressed(2).pdf", "references/course/sd5412-s01-slides.pdf"),
    ("S04", "SD5412-S02-handout-mandarin-oriental-team-copy(2).pdf", "references/course/sd5412-s02-mandarin-oriental-team.pdf"),
    ("S05", "访谈逐字稿(2).txt", "research/raw/kate-interview-transcript.txt"),
    ("S06", "香港理工大学-MO service(3).m4a", "research/raw/kate-interview-audio.m4a"),
    ("S07", "历史对话(2).md", "records/conversations/historical-dialogue.md"),
    ("S08", "项目衔接说明(2).md", "archive/import-notes/previous-project-handoff.md"),
    ("S09", "资料目录(2).md", "archive/import-notes/previous-source-catalogue.md"),
    ("S10", "历史附件_01(2).jpg", "assets/historical/history-01.jpg"),
    ("S11", "历史附件_02(2).jpg", "assets/historical/history-02.jpg"),
    ("S12", "历史附件_03(2).png", "assets/historical/history-03.png"),
    ("S13", "历史附件_04(2).png", "assets/historical/history-04.png"),
]
def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--extra", nargs=3, action="append", default=[],
                        metavar=("ID", "SOURCE_PATH", "REPOSITORY_PATH"))
    args = parser.parse_args()
    rows = []
    jobs = [(sid, args.source_dir / original, dest) for sid, original, dest in MAPPING]
    jobs += [(sid, Path(source), dest) for sid, source, dest in args.extra]
    for sid, source, dest in jobs:
        data = source.read_bytes()
        imported = data
        transformation = "byte-for-byte copy"
        if sid == "S07":
            text = data.decode("utf-8-sig")
            text, count = re.subn(r"(?i)(flow_id|user_code)=([^&\s\)<>]+)",
                                  r"\1=[REDACTED-AUTH]", text)
            imported = text.encode("utf-8")
            transformation = f"authentication query values redacted ({count} values); UTF-8"
        target = (ROOT / dest).resolve()
        if not target.is_relative_to(ROOT):
            raise ValueError(f"Destination escapes repository: {dest}")
        if target.exists() and target.read_bytes() != imported:
            raise ValueError(f"Refusing to overwrite differing archive: {dest}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(imported)
        if source.read_bytes() != data:
            raise RuntimeError(f"Source changed during import: {source.name}")
        rows.append({
            "id": sid, "original_name": source.name, "repository_path": dest,
            "source_bytes": len(data), "archived_bytes": len(imported),
            "source_sha256": sha(data), "archived_sha256": sha(imported),
            "transformation": transformation, "imported_on": "2026-10-24",
            "access": "private course/team archive; original ownership retained"
        })
    manifest = {
        "schema_version": 1, "archive_version": "0.1.0",
        "imported_on": "2026-10-24", "timezone": "Asia/Hong_Kong",
        "synced_source_files": 13, "recovered_discussion_attachments": len(args.extra),
        "note": "Source SHA values document provenance; credentials themselves are not archived.",
        "files": rows,
    }
    (ROOT / "archive/source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Imported {len(rows)} files; originals unchanged.")

if __name__ == "__main__":
    main()
