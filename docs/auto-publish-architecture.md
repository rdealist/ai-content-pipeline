# 自动化推送平台 — 架构设计

## 概述

将内容从 `output/` 目录自动推送到各平台。采用**适配器模式**，每个平台一个 Publisher，
统一接口，按配置文件控制推送行为。

## 架构图

```
                    ┌─────────────────┐
                    │  publish.yaml   │  ← 账号配置 + API Key
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ PublishManager  │  ← 调度中心
                    └────────┬────────┘
                             │
        ┌────────────┬───────┴───────┬────────────┬──────────┐
        ▼            ▼               ▼            ▼          ▼
  ┌──────────┐ ┌──────────┐  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ X/Twitter│ │  知乎    │  │  掘金    │ │ 小红书   │ │  即刻    │
  │ Publisher│ │ Publisher│  │ Publisher│ │ Publisher│ │ Publisher│
  └──────────┘ └──────────┘  └──────────┘ └──────────┘ └──────────┘
       │            │               │            │          │
   infsh CLI   Playwright      Playwright   XHS API    Playwright
```

## 平台接入方案对比

| 平台 | 方案 | 依赖 | 自动化程度 | 账号要求 |
|------|------|------|-----------|---------|
| **X/Twitter** | inference.sh CLI | `infsh` | ⭐⭐⭐ 全自动 | infsh 账号 |
| **知乎** | Playwright | `playwright` | ⭐⭐ 半自动 | 登录Cookie |
| **掘金** | Playwright | `playwright` | ⭐⭐ 半自动 | 登录Cookie |
| **小红书** | XHS MCP API | `localhost:18060` | ⭐⭐⭐ 全自动 | MCP Server |
| **即刻** | Playwright | `playwright` | ⭐⭐ 半自动 | 登录Cookie |
| **微信公众号** | Playwright | `playwright` | ⭐⭐ 半自动 | 登录Cookie |

## 配置文件

`~/.ai-content-pipeline/publish.yaml`（用户后续补充）：

```yaml
# X/Twitter — 通过 inference.sh
x:
  enabled: true
  method: "infsh"  # infsh | tweepy | playwright
  # infsh 方案：运行 `infsh login` 完成授权即可
  # tweepy 方案：填写以下字段
  # api_key: ""
  # api_secret: ""
  # access_token: ""
  # access_token_secret: ""

# 知乎 — 通过 Playwright
zhihu:
  enabled: false
  method: "playwright"
  cookie_file: "~/.ai-content-pipeline/cookies/zhihu.json"

# 掘金 — 通过 Playwright
juejin:
  enabled: false
  method: "playwright"
  cookie_file: "~/.ai-content-pipeline/cookies/juejin.json"

# 小红书 — 通过 MCP API
xiaohongshu:
  enabled: false
  method: "mcp"
  mcp_endpoint: "http://localhost:18060"

# 即刻 — 通过 Playwright
jike:
  enabled: false
  method: "playwright"
  cookie_file: "~/.ai-content-pipeline/cookies/jike.json"

# 微信公众号 — 通过 Playwright
wechat:
  enabled: false
  method: "playwright"
  cookie_file: "~/.ai-content-pipeline/cookies/wechat.json"
```

## Publisher 基类

```python
# cli/publishers/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PublishResult:
    platform: str
    success: bool
    url: str | None = None
    error: str | None = None

class BasePublisher(ABC):
    """所有平台 Publisher 的基类"""

    platform_name: str

    @abstractmethod
    def publish(self, content_path: Path, **kwargs) -> PublishResult:
        """发布内容到平台"""
        ...

    @abstractmethod
    def check_auth(self) -> bool:
        """检查认证状态"""
        ...
```

## X Publisher 实现

```python
# cli/publishers/x_twitter.py
import subprocess, json
from .base import BasePublisher, PublishResult

class XTwitterPublisher(BasePublisher):
    platform_name = "x"

    def __init__(self, method="infsh"):
        self.method = method

    def publish(self, content_path, **kwargs):
        text = content_path.read_text()
        if self.method == "infsh":
            return self._publish_via_infsh(text)
        elif self.method == "tweepy":
            return self._publish_via_tweepy(text, **kwargs)

    def _publish_via_infsh(self, text):
        input_data = json.dumps({"text": text})
        result = subprocess.run(
            ["infsh", "app", "run", "x/post-tweet", "--input", input_data],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return PublishResult("x", True)
        return PublishResult("x", False, error=result.stderr)

    def publish_thread(self, tweets: list[str]):
        """发布Thread（多条推文）"""
        results = []
        for tweet in tweets:
            r = self._publish_via_infsh(tweet)
            results.append(r)
        return results

    def check_auth(self):
        r = subprocess.run(["infsh", "whoami"], capture_output=True, text=True)
        return r.returncode == 0
```

## Playwright Publisher 通用逻辑

```python
# cli/publishers/playwright_base.py
from playwright.sync_api import sync_playwright
from .base import BasePublisher

class PlaywrightPublisher(BasePublisher):
    """基于 Playwright 的平台 Publisher 基类"""

    login_url: str
    publish_url: str

    def __init__(self, cookie_file: str):
        self.cookie_file = cookie_file

    def _launch_browser(self):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=self.cookie_file)
        return p, browser, context

    def check_auth(self):
        try:
            p, browser, ctx = self._launch_browser()
            page = ctx.new_page()
            page.goto(self.login_url)
            # 子类实现登录状态检测逻辑
            is_logged_in = self._check_login_status(page)
            browser.close()
            p.stop()
            return is_logged_in
        except Exception:
            return False

    def _check_login_status(self, page) -> bool:
        """子类覆盖：检测是否已登录"""
        return True
```

## 实现优先级

### Phase 1（本周）
- [x] X/Twitter SOP
- [x] 架构设计文档
- [ ] X Publisher 实现（infsh 方案）
- [ ] publish.yaml 配置加载

### Phase 2（下周）
- [ ] Playwright 基础 Publisher
- [ ] 知乎 Publisher
- [ ] 掘金 Publisher

### Phase 3（之后）
- [ ] 小红书 MCP Publisher
- [ ] 即刻 Publisher
- [ ] 微信公众号 Publisher
- [ ] PublishManager 调度中心

## 关联 Skill

已安装可复用的发布相关 Skill：

| Skill | 用途 | 安装来源 |
|-------|------|---------|
| `twitter-automation` | X 发推/Thread | inferen-sh/skills |
| `media-auto-publisher` | 6平台 Playwright 发布 | aaaaqwq/claude-code-skills |
| `xiaohongshu-publisher` | 小红书 MCP API | solar-luna/skills |
| `playwright-automation` | 通用浏览器自动化 | aaaaqwq/claude-code-skills |
| `social-media-automation` | 自媒体全流程 | garfield-bb/hap-skills |
