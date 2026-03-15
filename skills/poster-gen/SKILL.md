---
name: poster-gen
description: 根据内容自动生成深色主题卡片海报图片，用于社媒发布。支持从文章、spec或手动数据生成。
---

# Poster Generator — 内容卡片海报生成器

自动将结构化内容渲染为高质量的深色主题 AMA/Notes 风格海报图片，可直接用于小红书、即刻、X 等平台发布。

## 触发词

- "生成海报"、"生成卡片"、"做一张图"
- "内容海报"、"发布图片"
- "poster"、"card image"

## 设计风格

- **深色背景**：深藏蓝渐变（#111827 → #0f172a → #1a1033）
- **金色强调**：Q 标记、bullet、主标签用琥珀金色（#c7a356）
- **双栏 Q&A 布局**：信息密度高，视觉层次清晰
- **品牌区域**：左下角 Logo + 品牌名，右下角标签

## 工作流程

### Step 1: 准备数据

从内容中提取结构化数据。数据格式如下：

```yaml
category: "AGENT FRAMEWORK"        # 左上角分类标签
series: "PI DAY AMA"               # 右上角系列标签
title: "Pi Day: 对话 Pi 框架作者"   # 主标题
subtitle: "深入探讨其设计哲学..."    # 副标题（可选）
brand_name: "AI 启蒙小伙伴"        # 品牌名
brand_sub: "AGENT FRAMEWORKS"      # 品牌副标题
tags:                              # Footer 标签（第一个高亮）
  - "Pi Framework"
  - "AMA NOTES"
sections:                          # Q&A 内容块（建议4-8个）
  - question: "问题标题"
    points:
      - "回答要点1"
      - "回答要点2"
```

**从文章自动提取的规则**：
1. 文章标题 → `title`
2. 文章 frontmatter 的 topic/description → `subtitle`
3. 文章的 H2/H3 标题 → 各 section 的 `question`
4. 每个标题下的要点/段落 → 对应 `points`
5. 控制在 4-8 个 section，每个 section 2-4 个 points
6. 每个 point 尽量精简到 1-2 行（≤50字）

### Step 2: 保存数据文件

将提取的数据保存为 YAML 文件：

```bash
# 保存到 output/ 目录
cat > output/poster-data.yaml << 'EOF'
category: "..."
title: "..."
...
EOF
```

### Step 3: 生成海报

运行生成脚本：

```bash
cd /Users/wushihong/dev/ai-content-pipeline
source .venv/bin/activate
python scripts/poster_generator.py --yaml output/poster-data.yaml -o output/poster.png
```

脚本会：
1. 加载 YAML 数据
2. 渲染 HTML 模板（scripts/poster_template.html）
3. 使用 Playwright 截图为 PNG
4. 输出到指定路径

### Step 4: 可选 — 调整尺寸

通过 `--width` 参数调整宽度（高度自适应）：

```bash
# 默认 1200px 宽（适合大多数平台）
python scripts/poster_generator.py --yaml data.yaml -o output/poster.png -w 1200

# 小红书竖版（窄一些）
python scripts/poster_generator.py --yaml data.yaml -o output/poster-xhs.png -w 1080
```

## 与其他 Skill 的集成

### 在 content-pipeline-gen 中使用

在 Step 7（格式化输出）后，自动生成海报：

1. 从刚生成的长文中提取 Q&A 结构数据
2. 保存为 YAML
3. 调用 poster_generator 生成图片
4. 海报保存到 `output/poster/` 目录

### 在 content-pipeline-publish 中使用

发布时将海报图片作为封面/配图使用：
- 小红书：作为笔记首图
- 即刻：作为动态配图
- X/Twitter：作为 Thread 首图

## 数据示例

```yaml
category: "TECH BLOG"
series: "BUILD LOG #1"
title: "如何用 Spec 驱动开发模式撰写技术博客"
subtitle: "我的 AI 辅助写作工作流：从一份结构化 Spec 到五平台内容分发的完整实践。"
brand_name: "AI 启蒙小伙伴"
brand_sub: "CONTENT PIPELINE"
tags:
  - "AI Writing"
  - "BUILD LOG"
sections:
  - question: "为什么需要 Spec 驱动写作？"
    points:
      - "传统写作缺乏结构，AI 容易产生泛泛内容"
      - "Spec 定义目标读者、核心观点和文章骨架"
      - "让 AI 成为执行者而非决策者"
  - question: "Spec 文件包含哪些关键字段？"
    points:
      - "title、topic、target_audience：定义方向"
      - "key_points：3-5 个核心论点"
      - "pain_point + unique_angle：差异化切入"
  - question: "自动化流程是怎样的？"
    points:
      - "Spec → 长文初稿 → 格式化 → 多平台内容"
      - "CLI 工具一键转换掘金/知乎/微信格式"
      - "6 个 Prompt 模板确保各平台风格一致"
  - question: "效果如何？"
    points:
      - "从构思到五平台发布：< 30 分钟"
      - "内容质量稳定，不依赖灵感"
      - "一次创作，五平台分发"
```
