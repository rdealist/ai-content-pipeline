# X (Twitter) 平台运营 SOP

## 平台定位

**核心目标**：英文技术圈影响力 + 国际开源项目引流  
**内容语言**：英文为主，偶尔中英双语  
**账号人设**：Frontend engineer building in public, sharing AI-powered dev tools

## 内容类型与策略

### Thread（主力内容，周产出 1-2 条）

**定位**：将长文拆解为 5-12 条推文的Thread  
**触发场景**：每次博客发布后，同步生成Thread版本

**Thread公式**：
```
Tweet 1 (Hook): 反直觉观点/惊人数据 + 🧵👇
Tweet 2-N (Body): 每条一个要点，短句分行
Tweet N-1 (TL;DR): 3-5个bullet总结
Tweet N (CTA): 引导互动 + GitHub链接
```

**Hook类型**（轮流使用）：
1. 数据型：`I built an AI content pipeline in 1 day. Here's what I learned 🧵`
2. 反直觉型：`Most devs think content creation takes hours. It doesn't have to.`
3. 挑战型：`Hot take: Your side project is worthless if nobody knows about it.`
4. 故事型：`Yesterday I shipped 4 blog posts across 4 platforms in 30 minutes. Here's how:`

### Single Tweet（碎片内容，每天 1-2 条）

**定位**：日常技术观察、工具推荐、quick tip  
**字符限制**：≤280字符（英文）

**类型**：
- 🔧 Tool tip: "TIL: You can use Claude Code Skills to..."
- 💡 Insight: "The bottleneck in content creation isn't writing. It's starting."
- 📊 Progress update: "Week 2 of building in public: 12 posts, 3 platforms, 200 followers"
- 🔄 Retweet + comment: 转评技术大V的观点

### Reply & Engagement（互动策略）

- 每天花15分钟回复 #DevTools #AI #BuildInPublic 话题下的推文
- 有价值的评论 > 单纯点赞
- 目标：每周follow 10个同领域账号

## 发布时间

| 类型 | 最佳时间 (UTC+8) | 说明 |
|------|-----------------|------|
| Thread | 周二/四 22:00 | 转换为美西工作时间 |
| Single | 每天 8:00, 22:00 | 早晚两波 |
| Reply | 随时（碎片时间） | 通勤时操作 |

## 标签策略

**常用标签**（不超过3个/推）：
- `#BuildInPublic` — 核心标签
- `#DevTools` — 工具类内容
- `#AI` / `#LLM` — AI相关
- `#OpenSource` — 开源项目
- `#100DaysOfCode` — 可选，持续输出期

## 从长文到Thread的拆解规则

1. 一个key_point = 1-2条推文
2. 代码示例用截图（推文里的代码块可读性差）
3. Thread总长度5-12条，超过12条读者会流失
4. 每条推文独立可读（被转发后也有价值）
5. Hook推文决定80%的阅读率，花最多时间优化

## 引流矩阵

```
X Thread
  └→ 固定推文引导关注
  └→ Thread最后一条放GitHub链接
  └→ Bio里放项目链接
  └→ 每周一条中文内容引导中文用户到小红书/即刻
```

## 自动化方案

### 方案一：inference.sh CLI（推荐）

通过 `infsh` CLI 调用 X API，无需自建OAuth应用：

```bash
# 登录
infsh login

# 发推文
infsh app run x/post-tweet --input '{"text": "..."}'

# 发带图推文
infsh app run x/post-create --input '{"text": "...", "media_url": "..."}'
```

**优势**：开箱即用，不需要申请Twitter Developer账号  
**依赖**：需安装 `infsh` CLI（`npx skills add inference-sh/skills@agent-tools`）

### 方案二：Twitter API v2（备选）

需要申请 Twitter Developer Portal，获取OAuth 2.0凭证：

```python
# 环境变量
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_TOKEN_SECRET=xxx
```

使用 `tweepy` 库：
```python
import tweepy
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
client.create_tweet(text="Hello from AI Content Pipeline!")
```

### 方案三：Playwright 浏览器自动化（兜底）

使用 `playwright-automation` skill 模拟浏览器操作：
- 适合 API 方案受限时使用
- 需要管理登录Cookie
- 参考 `media-auto-publisher` skill 的 storageState 方案

## 数据追踪

| 指标 | 追踪方式 | 目标 |
|------|---------|------|
| 关注者 | 个人主页 | 月增100 |
| Tweet曝光 | Twitter Analytics | 单Thread >1K |
| 互动率 | Twitter Analytics | >2% |
| 链接点击 | GitHub Referrals | 引流到Repo |

## 与其他平台的协同

- **即刻**：Thread的中文精简版 → 发即刻
- **小红书**：Thread中的实操内容 → 改写为小红书笔记
- **知乎**：Thread背后的深度思考 → 扩展为知乎回答
- **GitHub**：所有内容最终引流到GitHub Repo
