"""
Markdown多平台格式化器

将标准Markdown转换为适配各平台的格式：
- 掘金（Juejin）：标准Markdown + 前置元数据
- 知乎（Zhihu）：处理代码块和图片格式
- 微信公众号（WeChat）：转换为兼容的HTML
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import TextIO

import click
import frontmatter


# ─── Platform Formatters ───────────────────────────────────────────────────────


def format_for_juejin(title: str, content: str, tags: list[str] | None = None) -> str:
    """掘金格式：添加前置元数据块，保持标准Markdown。"""
    tags = tags or ["前端", "AI"]
    tag_str = ", ".join(tags)
    header = f"""---
theme: smartblue
highlight: a11y-dark
---

> 本文使用 [AI Content Pipeline](https://github.com/user/ai-content-pipeline) 辅助生成
> 标签：{tag_str}

"""
    return header + _normalize_headings(content)


def format_for_zhihu(title: str, content: str) -> str:
    """知乎格式：调整代码块样式，处理图片格式。"""
    result = content
    # 知乎不支持某些HTML标签，清理掉
    result = re.sub(r"<details>.*?</details>", "", result, flags=re.DOTALL)
    # 知乎图片格式
    result = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        r'<img src="\2" alt="\1" />',
        result,
    )
    # 添加知乎专栏头部声明
    header = f"""> 本文使用 AI Content Pipeline 辅助生成，工具已开源。

"""
    return header + _normalize_headings(result)


def format_for_wechat(title: str, content: str) -> str:
    """微信公众号格式：转换为简洁HTML，适配公众号编辑器。"""
    html_parts = [
        '<section style="font-size:16px;line-height:1.8;color:#333;">',
        f"<h1>{_escape_html(title)}</h1>",
    ]

    for line in content.split("\n"):
        line = line.rstrip()
        if not line:
            html_parts.append("<br/>")
        elif line.startswith("### "):
            html_parts.append(f"<h3>{_escape_html(line[4:])}</h3>")
        elif line.startswith("## "):
            html_parts.append(f"<h2>{_escape_html(line[3:])}</h2>")
        elif line.startswith("# "):
            continue  # 标题已在顶部
        elif line.startswith("```"):
            html_parts.append(
                '<pre style="background:#f6f8fa;padding:16px;border-radius:6px;'
                'overflow-x:auto;font-size:14px;">'
            )
        elif line == "```":
            html_parts.append("</pre>")
        elif line.startswith("- "):
            html_parts.append(f"<p>• {_escape_html(line[2:])}</p>")
        elif line.startswith("> "):
            html_parts.append(
                f'<blockquote style="border-left:4px solid #ddd;padding-left:16px;'
                f'color:#666;">{_escape_html(line[2:])}</blockquote>'
            )
        else:
            # 处理行内代码
            formatted = re.sub(
                r"`([^`]+)`",
                r'<code style="background:#f0f0f0;padding:2px 6px;border-radius:3px;'
                r'font-size:14px;">\1</code>',
                _escape_html(line),
            )
            # 处理加粗
            formatted = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", formatted)
            html_parts.append(f"<p>{formatted}</p>")

    html_parts.append(
        '<p style="color:#999;font-size:14px;margin-top:24px;">'
        "本文使用 AI Content Pipeline 辅助生成</p>"
    )
    html_parts.append("</section>")
    return "\n".join(html_parts)


# ─── Helpers ───────────────────────────────────────────────────────────────────


def _normalize_headings(content: str) -> str:
    """确保标题层级从h2开始（h1留给平台标题）。"""
    if re.search(r"^# [^#]", content, re.MULTILINE):
        # 将所有标题降一级
        content = re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", content, flags=re.MULTILINE)
    return content


def _escape_html(text: str) -> str:
    """转义HTML特殊字符。"""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def parse_markdown_file(filepath: Path) -> tuple[str, str, dict]:
    """解析带frontmatter的Markdown文件，返回(标题, 正文, 元数据)。"""
    post = frontmatter.load(str(filepath))
    content = post.content
    metadata = dict(post.metadata)
    title = metadata.pop("title", filepath.stem.replace("-", " ").title())
    return title, content, metadata


# ─── CLI ───────────────────────────────────────────────────────────────────────

PLATFORMS = {
    "juejin": format_for_juejin,
    "zhihu": format_for_zhihu,
    "wechat": format_for_wechat,
}


@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--platform",
    "-p",
    type=click.Choice(list(PLATFORMS.keys())),
    required=True,
    help="目标平台",
)
@click.option("--output", "-o", type=click.Path(path_type=Path), help="输出文件路径（默认stdout）")
@click.option("--tags", "-t", multiple=True, help="文章标签（仅掘金）")
def main(input_file: Path, platform: str, output: Path | None, tags: tuple[str, ...]):
    """将Markdown文件格式化为指定平台的格式。

    示例：
        python markdown_formatter.py article.md -p juejin
        python markdown_formatter.py article.md -p wechat -o output/wechat.html
    """
    title, content, metadata = parse_markdown_file(input_file)
    formatter = PLATFORMS[platform]

    if platform == "juejin" and tags:
        result = formatter(title, content, tags=list(tags))
    else:
        result = formatter(title, content)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding="utf-8")
        click.echo(f"✅ 已输出到 {output}")
    else:
        click.echo(result)


if __name__ == "__main__":
    main()
