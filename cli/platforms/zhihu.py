"""知乎平台适配器。"""

from __future__ import annotations

import re

from .base import BasePlatformAdapter


class ZhihuAdapter(BasePlatformAdapter):
    name = "zhihu"
    description = "知乎专栏 — 知识分享平台（Markdown格式）"
    output_extension = ".md"

    def format(self, title: str, content: str, metadata: dict | None = None) -> str:
        result = content

        # 知乎不支持<details>折叠
        result = re.sub(r"<details>.*?</details>", "", result, flags=re.DOTALL)

        # 知乎图片用标准Markdown即可，但需要确保alt text存在
        result = re.sub(
            r"!\[\]\(([^)]+)\)",
            r"![image](\1)",
            result,
        )

        # 移除HTML注释
        result = re.sub(r"<!--.*?-->", "", result, flags=re.DOTALL)

        header = f"""# {title}

> 本文使用 AI Content Pipeline 辅助生成，工具已开源。

"""
        return header + result
