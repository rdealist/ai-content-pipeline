"""平台适配器基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BasePlatformAdapter(ABC):
    """所有平台适配器的基类。"""

    name: str = ""
    description: str = ""
    output_extension: str = ".md"

    @abstractmethod
    def format(self, title: str, content: str, metadata: dict | None = None) -> str:
        """将Markdown内容格式化为平台特定格式。"""
        ...
