# Blog from Spec — Claude Code Custom Skill
# 根据Spec文件生成技术博客初稿

---
description: "Generate a tech blog draft from a structured spec file using AI Content Pipeline prompts"
---

## Usage

在Claude Code中使用：

```
/blog-from-spec specs/example-spec.md
```

## 工作流程

1. 读取Spec文件（YAML格式的内容规划）
2. 加载对应的Prompt模板（`prompts/tech-blog-v1.md`）
3. 结合Spec + Prompt生成博客初稿
4. 输出为标准Markdown，带frontmatter元数据

## Skill定义

当用户提供一个spec文件路径时，执行以下步骤：

### Step 1: 解析Spec
读取spec文件，提取以下字段：
- `title`: 文章标题
- `topic`: 核心主题
- `target_audience`: 目标读者
- `key_points`: 关键要点列表
- `pain_point`: 读者痛点
- `unique_angle`: 独特视角
- `code_language`: 代码语言
- `word_count`: 目标字数

### Step 2: 加载Prompt模板
读取 `prompts/tech-blog-v1.md`，将Spec中的字段填入输入格式部分。

### Step 3: 生成博客初稿
按照Prompt模板的输出要求，生成完整的博客文章：

**文章结构：**
1. 引子：以具体场景/问题开头
2. 问题拆解：将核心问题拆为子问题
3. 解决方案：每个子问题给方案+代码示例
4. 实战经验：真实项目案例
5. 总结：Takeaway + 讨论问题

**frontmatter格式：**
```yaml
---
title: "{title}"
date: "{当前日期}"
tags: [根据topic推断]
description: "{基于pain_point生成的SEO描述}"
draft: true
---
```

### Step 4: 输出
将生成的文章保存到 `output/{title-slug}.md`，并在终端显示摘要。

## 示例

输入Spec：
```yaml
title: "如何用Spec驱动开发模式撰写技术博客"
topic: "AI辅助内容生产"
key_points:
  - "传统写作效率低"
  - "Spec驱动模式的优势"
  - "AI的正确定位"
```

输出：一篇~2500字的技术博客初稿，保存在 `output/` 目录。
