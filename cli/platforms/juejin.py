"""掘金平台适配器。"""

from __future__ import annotations

import re

from .base import BasePlatformAdapter


class JuejinAdapter(BasePlatformAdapter):
    name = "juejin"
    description = "掘金 — 技术社区（Markdown格式）"
    output_extension = ".md"

    def format(self, title: str, content: str, metadata: dict | None = None) -> str:
        metadata = metadata or {}
        tags = metadata.get("tags", ["前端", "AI"])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        tag_str = ", ".join(tags)

        header = f"""---
theme: smartblue
highlight: a11y-dark
---

# {title}

> 标签：{tag_str}
> 本文使用 [AI Content Pipeline](https://github.com/user/ai-content-pipeline) 辅助生成

"""
        return header + self._normalize_headings(content)

    @staticmethod
    def _normalize_headings(content: str) -> str:
        """确保正文标题从h2开始。"""
        lines = content.split("\n")
        result = []
        for line in lines:
            if re.match(r"^# [^#]", line):
                result.append("#" + line)  # h1 → h2
            else:
                result.append(line)
        return "\n".join(result)
