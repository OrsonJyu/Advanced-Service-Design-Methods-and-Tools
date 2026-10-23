# Advanced Service Design Methods and Tools
## SD5412 · Mandarin Oriental · The Unsaid

本仓库是香港理工大学 **SD5412 Advanced Service Design Methods and Tools** 课程项目的长期资料库，用来衔接研究、设计过程、原型、汇报和案例研究，并保留可追溯的版本记录。

**当前归档版本：v0.1.0 · 2026-10-24（Asia/Hong_Kong）**
这次版本号表示资料库的首次整理，不表示设计已上线或研究已经完成。详细覆盖范围见[迁移报告](docs/05-migration-report.md)。

### 从这里开始

**不知道应该去哪儿看？打开 [INDEX 文档导航](INDEX.md)。找具体文件可查 [CATALOG 完整目录](CATALOG.md)。**

| 读者 / 目的 | 入口 |
|---|---|
| 第一次了解项目 | [项目概览](docs/00-project-overview.md) |
| 接手继续工作 | [PROJECT_STATUS](PROJECT_STATUS.md) → [AGENTS](AGENTS.md) |
| 核对研究结论 | [研究证据与假设](docs/01-research-evidence.md) |
| 理解决策与演变 | [设计决策](docs/02-design-decisions.md) · [过程时间线](docs/03-process-timeline.md) |
| 找原型、汇报、案例研究 | [成果登记表](docs/04-artifact-register.md) |
| 找原始资料、来源与校验值 | [原始资料索引](archive/README.md) · [导入清单](archive/source-manifest.json) |
| 查询版本历史 | [CHANGELOG](CHANGELOG.md) · [版本与同步规则](docs/06-versioning-and-sync.md) |
| 贡献或继续归档 | [CONTRIBUTING](CONTRIBUTING.md) |

### 项目在解决什么

我们研究如何让住客在抵达前感到被认识和理解，并让酒店在可控的成本和运营复杂度下可靠兑现关照。现有成果涉及 Agent 预订沟通、MO App、Dream Maker 服务流程，以及连接前台体验与后台交付的服务设计。

**证据边界：** Kate 的陈述、团队推论、原型文案和实测结果分别标识。用户在最新讨论中确认：方案形成后只有简单模拟，**没有真实用户测试**。NPS、brand equity 和 willingness to pay 的改善均未被本项目证明。

### 目录

```text
docs/                     面向读者和后续 agents 的整理说明
references/course/        课程大纲与讲义副本
research/raw/             Kate 访谈逐字稿与录音
assets/historical/        历史图片及可恢复附件
records/conversations/    历史对话及本次可读取的近期记录
deliverables/figma/        Figma 页面文字、节点索引与可用视觉快照
archive/                  原始资料目录、迁移说明及 SHA-256 清单
scripts/                  导入、生成索引和验证工具
prototypes/               已恢复的可运行网页原型
```

资料来自项目同步文件与明确相关的讨论。原同步目录保持原样；仓库内保留整理后的副本和映射。Figma 在线文件继续作为可编辑设计原稿；文字和视觉导出不等同于原生 `.fig` 文件。

### English orientation

This repository documents the SD5412 Mandarin Oriental service design project: research evidence, decisions, prototypes, presentations, and case-study work. Start with the [project overview](docs/00-project-overview.md), [artifact register](docs/04-artifact-register.md), and [current status](PROJECT_STATUS.md). Chinese documentation retains the original discussion context; English project terminology is preserved throughout.

This is a private course/team archive. Course materials and third-party assets retain their original ownership and access conditions; no repository-wide open-source licence is asserted.

### Validation

Run with Python 3.10 or later:

```sh
python scripts/build_catalog.py
python scripts/validate_repository.py
```
