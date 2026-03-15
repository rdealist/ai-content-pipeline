---
name: content-pipeline-gen
description: Use when generating a blog post and related multi-platform content from a single spec file in this repository.
---

# Content Pipeline Generator

从一份Spec出发，自动生成五平台内容，实现"一次创作，五平台分发"。

## 触发词

- "写一篇文章"、"生成博客"、"从spec生成"
- "内容生产"、"生成小红书内容"
- "根据spec写"、"写技术博客"
- "一键生成"、"全平台内容"

## 工作流程

```
Spec文件 → 加载Prompt模板 → 生成四种格式内容 → 保存到output/
```

### Step 1: 解析或创建Spec

如果用户提供了Spec文件路径，读取并解析：
```bash
cat specs/<spec-file>.md
```

如果用户只提供了主题，先引导创建Spec。Spec格式：

```yaml
title: "文章标题"
topic: "核心主题"
target_audience: "目标读者"
key_points:
  - "要点1"
  - "要点2"
  - "要点3"
pain_point: "读者痛点"
unique_angle: "独特视角"
code_language: "代码语言（可选）"
word_count: "2000-3000"
```

将Spec保存到 `specs/` 目录。

### Step 2: 生成长文初稿

读取Prompt模板：
```bash
cat prompts/tech-blog-v1.md
```

根据Prompt模板中的**角色定义、输出要求、风格约束**，结合Spec内容，生成完整技术博客文章。

输出要求：
- Markdown格式，带YAML frontmatter
- 字数：Spec中指定的 word_count
- 结构：引子 → 问题拆解 → 解决方案（含代码示例）→ 实战经验 → 总结
- 文末附："*本文使用 [AI Content Pipeline](https://github.com/rdealist/ai-content-pipeline) 辅助生成*"

保存到 `output/<slug>.md`

### Step 3: 生成小红书笔记（3-5条）

读取小红书Prompt模板：
```bash
cat prompts/xiaohongshu-note.md
```

将长文拆解为3-5条独立小红书笔记：

**拆解规则**：
1. 每个key_point可拆成1条笔记
2. 整体总结可作为1条引流笔记
3. 每条笔记独立可读，不超过500字

**每条笔记格式**：
```
标题：{包含工具名+数据+身份标签}（≤20字）
正文：{Hook → 3个要点 → 总结 → CTA}（≤500字）
标签：#AI提效 #程序员 #效率工具 + 3-5个相关标签
```

**小红书风格约束**（来自SOP）：
- ❌ 不用技术术语
- ✅ 结果导向："从X小时变成Y分钟"
- ✅ 用emoji做视觉锚点
- ✅ 每段不超过3行

保存到 `output/xiaohongshu/` 目录，每条笔记一个文件。

### Step 4: 生成即刻动态

读取即刻Prompt模板：
```bash
cat prompts/jike-post.md
```

从长文中提炼最有观点的段落，生成1-2条即刻短动态：

**格式**：
```
{场景：1-2句}
{观点：2-4句}
{开放性问题：1句}
```

**即刻风格约束**（来自SOP）：
- 口语化，像和朋友聊天
- 有明确观点
- 200-400字
- 文末自然附GitHub链接

保存到 `output/jike/` 目录。

### Step 5: 生成知乎回答/文章

读取知乎Prompt模板：
```bash
cat prompts/zhihu-answer.md
```

将长文重组为知乎格式：

**格式**：
```
{直接结论：1-2句}
---
{论点展开：含代码示例}
---
总结：3-5条要点
---
引导：关注小红书获取更多
```

保存到 `output/zhihu/` 目录。

### Step 6: 生成 X/Twitter Thread

读取 X/Twitter Prompt模板：
```bash
cat prompts/twitter-thread.md
```

参考 X 平台SOP：
```bash
cat sops/x-twitter.md
```

将长文拆解为 5-12 条推文的 Thread：

**Thread结构**：
```
Tweet 1 (Hook): 反直觉观点/惊人数据 + 🧵👇（≤200字符）
Tweet 2-N (Body): 每条一个要点，短句分行（≤280字符）
Tweet N-1 (TL;DR): 3-5个bullet总结
Tweet N (CTA): 行动号召 + GitHub链接
```

**X风格约束**（来自SOP）：
- 英文为主
- 每条推文独立可读
- 用 → 代替冗长解释
- 标签不超过3个：#BuildInPublic #DevTools #AI
- Hook推文决定80%阅读率，重点打磨

保存到 `output/x/` 目录，thread整体保存为一个文件。

### Step 7: 格式化输出

使用CLI工具格式化长文为各平台最终格式：
```bash
cd /Users/wushihong/dev/ai-content-pipeline
source .venv/bin/activate
python scripts/markdown_formatter.py output/<slug>.md -p juejin -o output/juejin/
python scripts/markdown_formatter.py output/<slug>.md -p zhihu -o output/zhihu/
python scripts/markdown_formatter.py output/<slug>.md -p wechat -o output/wechat/
```

### Step 7.5: 生成内容海报

从长文中提取 Q&A 结构数据，生成深色主题卡片海报图片：

1. **提取数据**：从长文中提取 4-8 个核心 Q&A 对，每个 2-4 个精简要点
2. **保存 YAML**：以 `output/poster/<slug>-data.yaml` 保存数据文件
3. **生成海报**：
```bash
python scripts/poster_generator.py --yaml output/poster/<slug>-data.yaml -o output/poster/<slug>.png
```

数据格式参考 `skills/poster-gen/SKILL.md` 中的说明。海报可作为各平台的封面配图使用。

### Step 8: 生成发布摘要

生成一份发布检查清单：

```markdown
## 📋 内容生产完成 — 发布清单

### 生成的文件：
- [ ] 长文：output/<slug>.md
- [ ] 掘金格式：output/juejin/<slug>.md
- [ ] 知乎格式：output/zhihu/<slug>.md
- [ ] 微信格式：output/wechat/<slug>.html
- [ ] 小红书笔记：output/xiaohongshu/<n>.md × N条
- [ ] 即刻动态：output/jike/<n>.md × N条
- [ ] X Thread：output/x/<slug>-thread.md
- [ ] 内容海报：output/poster/<slug>.png

### 发布顺序（建议）：
1. 知乎（SEO权重最高，先发）
2. 掘金（技术社区）
3. X/Twitter Thread（国际社区，周二/四 22:00发）
4. 小红书（按SOP时间发布）
5. 即刻（碎片时间发布）

### 发布后：
- [ ] 30分钟内回复各平台评论
- [ ] 记录数据到 analytics/weekly-template.yaml
```

## 限制

- 一次只处理一份Spec
- 代码示例使用Spec中指定的语言
- 小红书笔记每条不超过500字、标题不超过20字
- 长文图片需要手动准备和上传

## 文件路径参考

```
/Users/wushihong/dev/ai-content-pipeline/
├── prompts/          # Prompt模板（Step 2-5读取）
├── specs/            # Spec输入文件
├── scripts/          # 格式化脚本（Step 6执行）
├── sops/             # 运营SOP（风格参考）
└── output/           # 所有输出
    ├── <slug>.md     # 长文原稿
    ├── juejin/       # 掘金格式
    ├── zhihu/        # 知乎格式
    ├── wechat/       # 微信HTML
    ├── xiaohongshu/  # 小红书笔记
    ├── jike/         # 即刻动态
    ├── x/            # X/Twitter Thread
    └── poster/       # 内容海报图片
```
