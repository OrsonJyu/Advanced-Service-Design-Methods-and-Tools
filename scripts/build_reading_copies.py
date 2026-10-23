"""Assemble convenient reading copies from archived Figma exports; originals remain unchanged."""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader,PdfWriter
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"deliverables/figma/2026-10-24"
OUT=ROOT/"deliverables/reading-copies"
OUT.mkdir(parents=True,exist_ok=True)
sources=[BASE/"visuals"/f"case-study-csm-{i:02}.pdf" for i in range(1,21)]
writer=PdfWriter()
for i,p in enumerate(sources,1):
 reader=PdfReader(p)
 if len(reader.pages)!=1:raise ValueError(f"Expected a one-page source: {p.name}")
 writer.append(reader,outline_item=f"Page {i:02}" if i<=10 else f"Appendix A{i-10:02}")
writer.add_metadata({"/Title":"SD5412 Mandarin Oriental - CSM style case study - archival reading copy","/Subject":"20 original Figma page exports assembled on 2026-10-24"})
case=OUT/"case-study-csm-v0.1.0.pdf"
with case.open("wb") as stream:writer.write(stream)
presentation=OUT/"presentation-36-slides-v0.1.0.pdf"
canvas=Canvas(str(presentation),pagesize=(1920,1080),pageCompression=1)
canvas.setTitle("SD5412 Mandarin Oriental - 36-slide archival reading copy")
slide_sources=[]
for i in range(1,37):
 p=BASE/"visuals"/f"presentation-slide-{i:02}.png";slide_sources.append(p)
 with Image.open(p) as im:
  if abs(im.width/im.height-16/9)>.01:raise ValueError(f"Unexpected slide aspect: {p.name}")
 canvas.drawImage(str(p),0,0,width=1920,height=1080,mask="auto")
 canvas.showPage()
canvas.save()
rows=[]
for p,inputs in [(case,sources),(presentation,slide_sources)]:
 data=p.read_bytes();rows.append({"path":p.relative_to(ROOT).as_posix(),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"pages":len(PdfReader(p).pages),"source_paths":[x.relative_to(ROOT).as_posix() for x in inputs]})
(ROOT/"archive/derived-manifest.json").write_text(json.dumps({"created_on":"2026-10-24","version":"0.1.0","note":"Case study preserves original exported PDF pages. Presentation is a raster reading copy; editable source remains in Figma.","files":rows},indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps([{k:v for k,v in r.items() if k!="source_paths"} for r in rows]))
