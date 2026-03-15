---
name: content-pipeline-publish
description: "多平台内容分发Skill。将output/目录中已生成的内容按照SOP流程发布到各平台。支持与xiaohongshu-publisher和media-auto-publisher联动实现自动发布。当用户说"发布内容"、"分发到各平台"、"发布文章"、"推送"时使用此Skill。"
metadata:
  version: 1.0.0
  domains: [publishing, distribution, automation]
  type: automation
---

# Content Pipeline Publisher

将已生成的多平台内容按SOP流程分发到各平台。

## 触发词

- "发布内容"、"分发到各平台"、"推送文章"
- "发到小红书"、"发到知乎"、"发到掘金"
- "多平台发布"、"一键发布"
- "发布到所有平台"

## 前置条件

确认 `output/` 目录中已有生成的内容文件：
```bash
ls -la /Users/wushihong/dev/ai-content-pipeline/output/
ls -la /Users/wushihong/dev/ai-content-pipeline/output/xiaohongshu/ 2>/dev/null
ls -la /Users/wushihong/dev/ai-content-pipeline/output/jike/ 2>/dev/null
ls -la /Users/wushihong/dev/ai-content-pipeline/output/zhihu/ 2>/dev/null
```

如果 output/ 为空，提示用户先运行 `content-pipeline-gen` Skill 生成内容。

## 发布工作流

### Step 1: 发布前检查

读取对应平台的SOP进行合规检查：

```bash
cat /Users/wushihong/dev/ai-content-pipeline/sops/xiaohongshu.md
cat /Users/wushihong/dev/ai-content-pipeline/sops/jike.md
cat /Users/wushihong/dev/ai-content-pipeline/sops/zhihu.md
```

**检查清单**：
- [ ] 当前时间是否在最佳发布时段？（参考SOP中的发布时间表）
- [ ] 小红书笔记标题 ≤ 20字？
- [ ] 小红书笔记正文 ≤ 1000字？
- [ ] 知乎文章开头200字包含核心关键词？
- [ ] 所有内容不含公司名称/业务细节？
- [ ] 所有引流话术符合SOP规范？

### Step 2: 平台发布顺序

按照 SOP 建议的顺序执行：

```
1. 知乎（SEO权重最高，先发先索引）
2. 掘金（技术社区同步）
3. 小红书（按SOP最佳时段发布）
4. 即刻（碎片时间发布）
```

### Step 3: 知乎发布

**手动发布流程**：
1. 读取 `output/zhihu/` 目录中的格式化内容
2. 将内容展示给用户，用户复制到知乎编辑器
3. 提醒检查：标题含关键词、开头有结论、有代码示例

**自动发布（已安装 media-auto-publisher 时）**：
```bash
# 检查是否可用
ls ~/.agents/skills/media-auto-publisher/scripts/ 2>/dev/null
# 如果可用，参考 media-auto-publisher Skill 进行自动发布
```

### Step 4: 掘金发布

**手动发布流程**：
1. 读取 `output/juejin/` 目录中的格式化内容
2. 展示给用户复制到掘金编辑器
3. 提醒添加标签和分类

### Step 5: 小红书发布

**手动发布流程**：
1. 依次读取 `output/xiaohongshu/` 下的笔记文件
2. 展示每条笔记的标题和正文
3. 提醒用户准备封面图（参考SOP中的封面规范）

**自动发布（已安装 xiaohongshu-publisher 时）**：
```bash
# 检查是否可用
ls ~/.agents/skills/xiaohongshu-publisher/ 2>/dev/null
# 如果可用且MCP服务运行中：
python3 ~/.agents/skills/xiaohongshu-publisher/simple_publish.py "标题" "正文内容"
```

### Step 6: 即刻发布

**手动发布流程**：
1. 读取 `output/jike/` 下的动态文件
2. 展示给用户复制到即刻
3. 提醒发布到相关圈子

### Step 7: 发布后跟踪

生成发布记录并更新数据追踪文件：

```bash
# 读取周报模板
cat /Users/wushihong/dev/ai-content-pipeline/analytics/weekly-template.yaml
```

提供一份发布记录让用户填入数据：

```yaml
# 追加到 analytics/ 目录的当周文件
published:
  date: "{当前日期}"
  title: "{文章标题}"
  platforms:
    zhihu:
      url: ""       # 用户填写
      published: true
    juejin:
      url: ""
      published: true
    xiaohongshu:
      notes_count: N
      published: true
    jike:
      posts_count: N
      published: true
```

### Step 8: 互动提醒

根据SOP设置提醒：
- "发布后30分钟内回复所有评论。"
- "小红书评论区自己留言补充信息以增加曝光。"
- "知乎文章评论区感谢第一个点赞的人。"

## 平台发布时间参考

| 平台 | 最佳时段 | 备选时段 |
|------|---------|---------|
| 知乎 | 随时（SEO导向） | - |
| 掘金 | 工作日 9:00-11:00 | 14:00-16:00 |
| 小红书 | 12:00-13:00 | 18:00-19:00, 21:00-22:00 |
| 即刻 | 8:00-9:00, 12:00 | 21:00-22:00 |

## 与其他Skill的联动

本Skill可与以下已安装Skill联动：

| Skill | 联动方式 |
|-------|---------|
| `xiaohongshu-publisher` | 小红书自动发布（需MCP服务） |
| `media-auto-publisher` | 多平台自动发布（需Playwright） |
| `content-pipeline-gen` | 先生成内容，再调用本Skill发布 |
| `content-pipeline-review` | 发布后7天调用Review复盘数据 |
