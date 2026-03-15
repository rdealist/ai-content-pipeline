"""微信公众号平台适配器。"""

from __future__ import annotations

import re

from .base import BasePlatformAdapter


class WechatAdapter(BasePlatformAdapter):
    name = "wechat"
    description = "微信公众号 — 社交媒体平台（HTML格式）"
    output_extension = ".html"

    def format(self, title: str, content: str, metadata: dict | None = None) -> str:
        lines = content.split("\n")
        html_parts = [
            "<!DOCTYPE html>",
            '<html><body>',
            '<section style="font-size:16px;line-height:1.8;color:#333;'
            'max-width:640px;margin:0 auto;padding:20px;">',
            f'<h1 style="font-size:24px;font-weight:bold;margin-bottom:16px;">'
            f"{self._escape(title)}</h1>",
        ]

        in_code_block = False

        for line in lines:
            line = line.rstrip()

            # 代码块处理
            if line.startswith("```") and not in_code_block:
                in_code_block = True
                html_parts.append(
                    '<pre style="background:#f6f8fa;padding:16px;border-radius:6px;'
                    'overflow-x:auto;font-size:13px;line-height:1.5;"><code>'
                )
                continue
            if line.startswith("```") and in_code_block:
                in_code_block = False
                html_parts.append("</code></pre>")
                continue
            if in_code_block:
                html_parts.append(self._escape(line))
                continue

            # 空行
            if not line:
                html_parts.append("<br/>")
                continue

            # 标题
            if line.startswith("### "):
                html_parts.append(
                    f'<h3 style="font-size:18px;font-weight:bold;margin:20px 0 8px;">'
                    f"{self._escape(line[4:])}</h3>"
                )
            elif line.startswith("## "):
                html_parts.append(
                    f'<h2 style="font-size:20px;font-weight:bold;margin:24px 0 10px;">'
                    f"{self._escape(line[3:])}</h2>"
                )
            elif line.startswith("# "):
                continue  # 标题已在顶部
            # 列表
            elif line.startswith("- "):
                html_parts.append(
                    f'<p style="margin:4px 0;padding-left:16px;">'
                    f"• {self._format_inline(line[2:])}</p>"
                )
            # 引用
            elif line.startswith("> "):
                html_parts.append(
                    f'<blockquote style="border-left:4px solid #42b983;padding:8px 16px;'
                    f'margin:12px 0;background:#f9f9f9;color:#666;">'
                    f"{self._escape(line[2:])}</blockquote>"
                )
            # 图片
            elif re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line):
                m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
                html_parts.append(
                    f'<img src="{self._escape(m.group(2))}" alt="{self._escape(m.group(1))}" '
                    f'style="max-width:100%;margin:12px 0;border-radius:4px;" />'
                )
            # 普通段落
            else:
                html_parts.append(
                    f'<p style="margin:8px 0;">{self._format_inline(line)}</p>'
                )

        # 底部署名
        html_parts.append(
            '<p style="color:#999;font-size:13px;margin-top:32px;padding-top:16px;'
            'border-top:1px solid #eee;">'
            "本文使用 AI Content Pipeline 辅助生成 | 工具已开源</p>"
        )
        html_parts.append("</section></body></html>")
        return "\n".join(html_parts)

    @staticmethod
    def _escape(text: str) -> str:
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def _format_inline(self, text: str) -> str:
        """处理行内格式：加粗、行内代码、链接。"""
        result = self._escape(text)
        # 行内代码
        result = re.sub(
            r"`([^`]+)`",
            r'<code style="background:#f0f0f0;padding:2px 6px;border-radius:3px;'
            r'font-size:13px;">\1</code>',
            result,
        )
        # 加粗
        result = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", result)
        # 链接（微信公众号不支持外链，显示为文字）
        result = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"<strong>\1</strong>", result)
        return result
