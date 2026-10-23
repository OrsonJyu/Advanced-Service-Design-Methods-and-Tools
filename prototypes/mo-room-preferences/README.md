# Arrival Atelier · Room preferences

这是从 iCloud 恢复的早期房间偏好网页探索，保留原 HTML、CSS、JavaScript 字节。它与后续 MO App、Dream Maker Figma 版本分别保留。

## 如何打开
从仓库根目录运行 Python 3.10+：

```sh
python -m http.server 8768 --directory prototypes/mo-room-preferences
```

然后打开 [本地预览](http://127.0.0.1:8768/)。该地址只在本机服务运行时有效。GitHub 文件页显示源码，不会运行交互。

入口：[index.html](index.html)；样式：[style.css](style.css)；行为：[app.js](app.js)。

## 内容与边界
原型支持房间图中的温度、床侧、果盘和评论探索。它是演示界面，没有真实预订、酒店接单或服务兑现；刷新会重置状态。历史纪要的功能检查不等于用户测试。

来源映射见[ iCloud 清单](../../archive/icloud-manifest.json)，历史实现说明见[2026-10-05 纪要](../../records/context/2026-10-05-project-context.md)。旧托管配置另存作背景，本次未部署网站。
