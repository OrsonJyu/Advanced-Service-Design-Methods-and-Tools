# 如何继续维护

先读 [AGENTS](AGENTS.md) 和 [当前状态](PROJECT_STATUS.md)。新增资料时保留来源、日期、作者或发言角色、版本、验证程度，以及它替代或补充了什么。

## 文件与记录
- 使用稳定、可读、尽量短的英文文件名；正文保留原始语言。
- 日期写为 `YYYY-MM-DD`，时间注明时区；本次归档日期为香港时间。
- 原始资料与整理解释分开保存。需要修订原稿时新增版本，并解释差异。
- 数字注明来源、样本、时间与验证状态；概念中的目标不能写成已实现收益。
- 每个外部成果应记录在线入口、本地归档路径和缺口；只有链接不算取得了文件。
- 新增与本项目相关的文件即可，不上传环境配置、认证信息、缓存或无关个人资料。

## 常用操作
```sh
git status --short --branch
git remote -v
git log -5 --oneline
git fetch origin
python scripts/validate_repository.py
git diff --check
```

核对差异后只提交本次内容，正常推送；推送前再次 fetch，并核对并发更新。具体版本规则见[版本与同步](docs/06-versioning-and-sync.md)。
