# Figma 归档

本目录保存 **2026-10-24** 的读取与导出快照。可编辑设计原稿：[5412 Service](https://www.figma.com/design/a5Mf39eUB7M9nGiT0P9lj3/5412-Service)；汇报原稿：[5412-Pre](https://www.figma.com/slides/mmSZ6q6mDoVdPXCpLub6OO/5412-Pre)。

| 页面 | 文字 / 节点文件 |
|---|---|
| Page 1 / 研究墙 | [research-board.json](2026-10-24/research-board.json) |
| Case study | [case-study.json](2026-10-24/case-study.json) |
| Final Presentation | [final-presentation.json](2026-10-24/final-presentation.json) |
| MO App Prototype | [mo-app-prototype.json](2026-10-24/mo-app-prototype.json) |
| MO · Pre Slides Make | [pre-slides-make.json](2026-10-24/pre-slides-make.json) |
| MO Dream Maker | [mo-dream-maker.json](2026-10-24/mo-dream-maker.json) |
| 36 页 Slides 文字与讲稿 | [presentation.json](2026-10-24/presentation.json) |
| Slides 网格顺序与节点 | [presentation-inventory.json](2026-10-24/presentation-inventory.json) |
| 视觉、配图、SVG 来源与校验值 | [asset-manifest.json](2026-10-24/asset-manifest.json) |

Design JSON 中 `roots` 是顶层节点；`texts` 每项为 `[textNodeId, parentNodeId, originalText]`。父级 ID 不构成完整图层树，遍历顺序不保证等同于叙事阅读顺序。Slides JSON 为逐页对象，含 `speakerNotes` 和文本节点。

`visuals/` 保存板概览、CSM 单页 PDF 和汇报 PNG；`source-images/`、`source-vectors/` 保存可导出的素材，重复字节共用一份。所有来源关系在资产清单中可查。完整定位见[CATALOG](../../CATALOG.md)。

隐藏原版 A3 的文字已取得，画面导出返回空值。整板渲染及素材截断标志不能代替原生文件、完整交互和全部源素材的备份。
