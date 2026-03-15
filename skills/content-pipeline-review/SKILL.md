---
name: content-pipeline-review
description: Use when reviewing weekly content performance, summarizing cross-platform publishing data, or planning the next round of content strategy.
---

# Content Pipeline Review

每周数据复盘 + 策略迭代，形成"生产 → 发布 → 复盘 → 优化"闭环。

## 触发词

- "数据复盘"、"周报"、"内容分析"
- "复盘"、"看看数据"、"本周表现"
- "内容复盘"、"平台数据"

## 工作流程

### Step 1: 收集基础数据

读取当前的数据模板：
```bash
cat /Users/wushihong/dev/ai-content-pipeline/analytics/weekly-template.yaml
```

列出已有的历史周报：
```bash
ls /Users/wushihong/dev/ai-content-pipeline/analytics/weekly/ 2>/dev/null
```

向用户收集本周各平台数据。提供结构化问题：

```
📊 请提供本周各平台数据：

小红书：
  - 当前粉丝数：
  - 本周发布笔记数：
  - 表现最好的笔记标题：
  - 该笔记的数据（浏览/点赞/收藏/评论）：
  - 私信数（引流相关）：

即刻：
  - 当前关注数：
  - 本周发动态数：
  - 获赞最多的动态：
  - 新增关注：

知乎：
  - 当前关注数：
  - 本周发布数（文章+回答）：
  - 总阅读量：
  - 最高赞回答：

GitHub（ai-content-pipeline仓库）：
  - 当前Star数：
  - 本周访客数（Insights > Traffic）：
  - 本周Clone数：

（未开通的平台填0即可）
```

### Step 2: 生成周报

根据收集的数据，创建周报文件：

```bash
# 文件路径
/Users/wushihong/dev/ai-content-pipeline/analytics/weekly/YYYY-WXX.yaml
```

填入模板格式（参考 `analytics/weekly-template.yaml`）。

### Step 3: 数据分析

对收集到的数据进行分析，输出以下维度：

#### 3.1 内容表现排名

```markdown
## 📈 本周Top内容

| 排名 | 平台 | 标题 | 浏览 | 互动率 |
|------|------|------|------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

互动率 = (点赞+收藏+评论) / 浏览量 × 100%
```

#### 3.2 平台增长趋势

```markdown
## 📊 增长趋势

| 平台 | 上周粉丝 | 本周粉丝 | 增长 | 增长率 |
|------|---------|---------|------|--------|
| 小红书 | | | | |
| 即刻 | | | | |
| 知乎 | | | | |
```

#### 3.3 内容类型分析

分析哪种内容类型（实测/工具/经验/福利）表现最好：

```markdown
## 🔍 内容类型表现

| 类型 | 发布数 | 平均浏览 | 平均互动率 | 结论 |
|------|--------|---------|-----------|------|
| 实测分享 | | | | |
| 工具安利 | | | | |
| 经验观点 | | | | |
| 福利引流 | | | | |
```

#### 3.4 引流漏斗

```markdown
## 🔁 引流漏斗

浏览量 → 私信数 → GitHub访问 → 邮箱收集
{X}      {Y}      {Z}         {W}

转化率：{Y/X}% → {Z/Y}% → {W/Z}%
```

### Step 4: 策略建议

根据数据分析结果，给出具体的下周策略建议：

**分析维度**：

1. **爆款复制**：哪条内容表现最好？相似选题还有哪些？
2. **失败分析**：表现最差的内容，问题出在标题/内容/时间？
3. **平台调整**：各平台精力分配是否需要调整？
4. **引流优化**：引流转化率如何？话术/路径是否需要改进？
5. **选题方向**：评论区出现了哪些新的用户痛点？

输出格式：
```markdown
## 🎯 下周行动计划

### 内容方向
1. [基于爆款数据的选题建议]
2. [基于评论区痛点的新选题]
3. [需要停止或调整的内容方向]

### 运营调整
1. [发布时间优化]
2. [互动策略调整]
3. [引流话术更新]

### 工具迭代
1. [Prompt模板是否需要更新]
2. [CLI工具是否有新需求]
3. [SOP文档是否需要修订]
```

### Step 5: 更新SOP（如需要）

如果分析发现以下情况，主动建议更新SOP：

- 某个发布时段效果明显优于SOP推荐 → 更新SOP发布时间表
- 某个标题公式效果特别好 → 添加到SOP标题模板
- 引流话术转化率低 → 更新SOP引流技巧
- 发现新的对标账号 → 添加到SOP对标账号表

读取对应SOP并提出具体修改建议：
```bash
cat /Users/wushihong/dev/ai-content-pipeline/sops/xiaohongshu.md
```

### Step 6: 保存并提交

```bash
cd /Users/wushihong/dev/ai-content-pipeline
git add analytics/
git commit -m "📊 analytics: 第{N}周数据复盘

- 小红书粉丝：{X}（+{Y}）
- 最佳内容：{标题}（{浏览量}浏览）
- 关键发现：{一句话总结}"
```

## 里程碑检查

每次复盘时检查项目整体进展：

```markdown
## 🏁 里程碑进度

| 里程碑 | 目标 | 当前 | 状态 |
|--------|------|------|------|
| 小红书粉丝 | 500 | {X} | {✅/🚧} |
| 即刻关注 | 200 | {X} | |
| 知乎关注 | 100 | {X} | |
| GitHub Star | 50 | {X} | |
| 小报童订阅 | 10 | {X} | |
| 周均内容产出 | 5条 | {X} | |
```

当里程碑达到时，提醒用户参考 `TODO.md` 中的下一阶段计划。

## 文件路径

```
analytics/
├── weekly-template.yaml    # 周报模板
└── weekly/                 # 历史周报
    ├── 2026-W12.yaml
    ├── 2026-W13.yaml
    └── ...
```
