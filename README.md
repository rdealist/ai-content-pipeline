# AI Content Pipeline

> 这个仓库记录我用AI工具构建个人数字资产系统的全过程。

用代码和AI工具将内容生产从**手工作坊**升级为**自动化流水线**：

```
Spec撰写 → AI生成初稿 → 风格润色 → 多平台格式化 → 一键发布 → 数据复盘
```

**核心理念**：一次创作，四平台分发。每篇内容同时产出工具测试案例、GitHub示例、多平台素材。

## 🏗️ 项目结构

```
ai-content-pipeline/
├── prompts/                    # Prompt-as-Code 模板库
│   ├── tech-blog-v1.md         # 技术博客写作Prompt
│   ├── xiaohongshu-note.md     # 小红书笔记写作Prompt
│   ├── jike-post.md            # 即刻动态写作Prompt
│   ├── zhihu-answer.md         # 知乎回答写作Prompt
│   ├── twitter-thread.md       # Twitter线程拆解Prompt
│   └── code-comment.md         # 代码注释生成Prompt
├── sops/                       # 各平台运营SOP
│   ├── xiaohongshu.md          # 小红书SOP（主阵地）
│   ├── jike.md                 # 即刻SOP（专业人设）
│   ├── zhihu.md                # 知乎SOP（SEO资产）
│   ├── xiaobaotong.md          # 小报童SOP（变现层）
│   └── content-distribution.md # 内容复用与分发全流程
├── scripts/                    # 自动化脚本
│   └── markdown_formatter.py   # Markdown多平台格式化器
├── cli/                        # auto-publish CLI工具
│   ├── main.py                 # CLI入口
│   ├── config.py               # 配置管理
│   └── platforms/              # 各平台适配器
│       ├── base.py             # 适配器基类
│       ├── juejin.py           # 掘金格式化
│       ├── zhihu.py            # 知乎格式化
│       └── wechat.py           # 微信公众号格式化
├── skills/                     # Claude Code自定义Skill
│   └── blog-from-spec/         # Spec → 博客骨架生成器
├── specs/                      # 内容Spec模板
│   └── example-spec.md         # 示例Spec
├── analytics/                  # 数据追踪
│   └── weekly-template.yaml    # 周报数据模板
├── output/                     # 生成的内容输出目录
├── TODO.md                     # 项目进度追踪
├── pyproject.toml              # Python项目配置
└── README.md
```

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/rdealist/ai-content-pipeline.git
cd ai-content-pipeline
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### 内容生产流程

```bash
# 1. 从Spec生成博客骨架
python skills/blog-from-spec/blog_generator.py specs/example-spec.md

# 2. 用AI填充内容（配合 prompts/tech-blog-v1.md）

# 3. 格式化为各平台格式
python scripts/markdown_formatter.py output/article.md -p juejin
python scripts/markdown_formatter.py output/article.md -p wechat -o output/

# 4. 使用CLI批量格式化
ai-publish format article.md --to juejin,zhihu,wechat
```

### 查看平台SOP

各平台有独立的运营标准流程文档（`sops/` 目录），包含：
- 账号设置指南
- 内容选题流程
- 标题/封面/正文模板
- 发布时间与互动策略
- 引流话术
- 数据复盘模板

## 📦 工具资产清单

| 工具 | 状态 | 说明 |
|------|------|------|
| Prompt模板库（6个） | ✅ 可用 | 技术博客/小红书/即刻/知乎/Twitter/代码注释 |
| 平台SOP（5份） | ✅ 可用 | 小红书/即刻/知乎/小报童/分发流程 |
| Markdown格式化器 | ✅ 可用 | 支持掘金/知乎/微信公众号格式转换 |
| auto-publish CLI | ✅ 可用 | 批量格式化 + 平台适配器架构 |
| Blog骨架生成器 | ✅ 可用 | Spec → 结构化博客Markdown |
| 数据追踪模板 | ✅ 可用 | 多平台周报YAML模板 |
| 图片自动上传 | 📋 计划中 | 图床API集成 |
| API直接发布 | 📋 计划中 | 掘金/知乎API集成 |
| 数据分析面板 | 📋 计划中 | 多平台数据聚合Dashboard |

## 🎯 平台策略矩阵

```
┌──────────────────────────────────────────────────────┐
│                  内容分发矩阵                          │
│                                                      │
│  ┌──────────┐   ┌────────┐   ┌────────┐             │
│  │  小红书    │   │  即刻   │   │  知乎   │             │
│  │ 流量入口   │   │专业人设  │   │SEO资产  │             │
│  │  70%精力  │   │ 20%精力 │   │ 10%精力 │             │
│  └────┬─────┘   └───┬────┘   └───┬────┘             │
│       │             │            │                   │
│       └──────────┬──┴────────────┘                   │
│                  ▼                                   │
│         ┌────────────────┐                           │
│         │  私域沉淀        │                           │
│         │ GitHub · 邮箱    │                           │
│         └───────┬────────┘                           │
│                 ▼                                    │
│         ┌────────────────┐                           │
│         │  小报童 · 付费   │                           │
│         │  变现层          │                           │
│         └────────────────┘                           │
└──────────────────────────────────────────────────────┘
```

## 🧱 五层数字资产体系

1. **技能资产**：AI工程化能力、前端架构能力
2. **内容资产**：多平台内容矩阵（小红书/即刻/知乎/掘金）
3. **工具资产** ← **本仓库**：可复用的AI内容生产工具链
4. **自动化资产**：Spec → 生产 → 分发 → 复盘的闭环流水线
5. **影响力资产**：个人品牌、社区认可、付费订阅

## 📝 内容系列

- **系列1**：《构建AI内容流水线》— 展示工具构建过程
- **系列2**：《AI工程化实战》— 展示专业能力
- **系列3**：《Pre-IPO技术风险管理》— 展示独特经验

## 📊 项目进度

详见 [TODO.md](TODO.md)

---

*本项目持续迭代中。每篇使用本流水线产出的文章，都是对工具有效性的最佳证明。*

*本文使用自研的AI Pipeline生成 — 获取工具模板请Star本仓库。*
