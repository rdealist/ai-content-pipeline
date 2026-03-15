# AI Content Pipeline

> 这个仓库记录我用AI工具构建个人数字资产系统的全过程。

用代码和AI工具将内容生产从**手工作坊**升级为**自动化流水线**：Spec驱动 → AI生成初稿 → 风格润色 → 多平台格式化 → 一键发布。

## 🏗️ 项目结构

```
ai-content-pipeline/
├── prompts/                  # Prompt模板库（版本控制的Prompt-as-Code）
│   ├── tech-blog-v1.md       # 技术博客写作Prompt
│   ├── twitter-thread.md     # Twitter线程拆解Prompt
│   └── code-comment.md       # 代码注释生成Prompt
├── scripts/                  # 自动化脚本
│   ├── markdown_formatter.py # Markdown多平台格式化器
│   └── image_uploader.py     # 图片自动上传（图床集成）
├── cli/                      # auto-publish CLI工具
│   ├── __init__.py
│   ├── main.py               # CLI入口
│   ├── platforms/             # 各平台适配器
│   │   ├── juejin.py         # 掘金格式化
│   │   ├── zhihu.py          # 知乎格式化
│   │   └── wechat.py         # 微信公众号格式化
│   └── config.py             # 配置管理
├── skills/                   # Claude Code自定义Skill
│   └── blog-from-spec/       # /blog-from-spec命令
├── specs/                    # 内容Spec模板
│   └── example-spec.md       # 示例Spec
├── output/                   # 生成的内容输出目录
├── pyproject.toml            # Python项目配置
└── README.md
```

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/user/ai-content-pipeline.git
cd ai-content-pipeline

# 安装依赖
pip install -e .
```

### 使用Prompt模板

1. 选择合适的Prompt模板（`prompts/` 目录）
2. 编写内容Spec（参考 `specs/example-spec.md`）
3. 使用AI工具（Claude/GPT）结合Prompt + Spec生成初稿

### 多平台发布

```bash
# 格式化Markdown为各平台格式
python scripts/markdown_formatter.py input.md --platform juejin

# 使用CLI一键发布（开发中）
ai-publish --input article.md --to juejin,zhihu,wechat
```

## 📦 工具资产清单

| 工具 | 状态 | 说明 |
|------|------|------|
| Prompt模板库 | ✅ 可用 | 版本控制的Prompt-as-Code |
| Markdown格式化器 | ✅ 可用 | 多平台Markdown格式转换 |
| auto-publish CLI | 🚧 开发中 | 一键多平台发布 |
| 图片自动上传 | 📋 计划中 | 图床API集成 |
| 内容数据分析 | 📋 计划中 | 多平台数据聚合Dashboard |

## 🧱 五层数字资产体系

本项目是"技术-内容双轮资产"框架的核心工具层：

1. **技能资产**：AI工程化能力、前端架构能力
2. **内容资产**：技术博客、Newsletter
3. **工具资产** ← 本仓库：可复用的AI内容生产工具
4. **自动化资产**：CI/CD式的内容发布流水线
5. **影响力资产**：个人品牌、社区认可

## 📝 内容系列

- **系列1**：《构建AI内容流水线》— 展示工具构建过程
- **系列2**：《AI工程化实战》— 展示专业能力
- **系列3**：《Pre-IPO技术风险管理》— 展示独特经验

---

*本项目持续迭代中。每篇使用本流水线产出的文章，都是对工具有效性的最佳证明。*
