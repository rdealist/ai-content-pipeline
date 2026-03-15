"""平台适配器注册表。"""

from __future__ import annotations

from .juejin import JuejinAdapter
from .zhihu import ZhihuAdapter
from .wechat import WechatAdapter

REGISTRY: dict[str, object] = {
    "juejin": JuejinAdapter(),
    "zhihu": ZhihuAdapter(),
    "wechat": WechatAdapter(),
}
