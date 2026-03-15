"""
poster_generator.py — 内容卡片/海报生成器

将结构化内容渲染为白底黑字 + 随机主题色的卡片海报图片。
使用 Jinja2 模板 + Playwright 截图实现。

用法:
    python scripts/poster_generator.py --json data.json --output output/poster.png
    python scripts/poster_generator.py --yaml data.yaml --output output/poster.png

数据格式示例 (JSON/YAML):
    category: "AGENT FRAMEWORK"
    series: "PI DAY AMA"
    title: "Pi Day: 对话 Pi 框架作者"
    subtitle: "作为 OpenClaw 背后的极简 Agent 框架..."
    brand_name: "AI 启蒙小伙伴"
    brand_sub: "AGENT FRAMEWORKS"
    tags: ["Pi Framework", "AMA NOTES"]
    sections:
      - question: "为什么只用4个核心工具？"
        points:
          - '"Bash is all you need"：允许 LLM 组合命令实现所有功能'
          - "极简系统提示：让模型自主决定调用时机"
      - question: "如何让 Agent 长时间稳定运行？"
        points:
          - "使用外部确定性循环监控重启"
          - "安全第一：不 skip permissions"
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import click
import yaml
from jinja2 import Template

TEMPLATE_PATH = Path(__file__).parent / "poster_template.html"

# 主题色调色板：每次随机选一组，保证白底下可读性好
THEME_COLORS = [
    {"accent": "#2563eb", "accent_light": "#dbeafe", "accent_dark": "#1e40af"},  # Blue
    {"accent": "#7c3aed", "accent_light": "#ede9fe", "accent_dark": "#5b21b6"},  # Violet
    {"accent": "#059669", "accent_light": "#d1fae5", "accent_dark": "#047857"},  # Emerald
    {"accent": "#dc2626", "accent_light": "#fee2e2", "accent_dark": "#b91c1c"},  # Red
    {"accent": "#d97706", "accent_light": "#fef3c7", "accent_dark": "#b45309"},  # Amber
    {"accent": "#0891b2", "accent_light": "#cffafe", "accent_dark": "#0e7490"},  # Cyan
    {"accent": "#c026d3", "accent_light": "#fae8ff", "accent_dark": "#a21caf"},  # Fuchsia
    {"accent": "#4f46e5", "accent_light": "#e0e7ff", "accent_dark": "#3730a3"},  # Indigo
    {"accent": "#0d9488", "accent_light": "#ccfbf1", "accent_dark": "#0f766e"},  # Teal
    {"accent": "#e11d48", "accent_light": "#ffe4e6", "accent_dark": "#be123c"},  # Rose
]


def load_data(json_path: str | None = None, yaml_path: str | None = None) -> dict:
    """从 JSON 或 YAML 文件加载海报数据。"""
    if json_path:
        with open(json_path, encoding="utf-8") as f:
            return json.load(f)
    if yaml_path:
        with open(yaml_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    raise ValueError("必须提供 --json 或 --yaml 参数")


def pick_theme(data: dict) -> dict:
    """注入随机主题色（如果数据中未指定）。"""
    if "accent_color" not in data:
        theme = random.choice(THEME_COLORS)
        data["accent_color"] = theme["accent"]
        data["accent_light"] = theme["accent_light"]
        data["accent_dark"] = theme["accent_dark"]
    return data


def render_html(data: dict) -> str:
    """用 Jinja2 渲染 HTML 海报。"""
    data = pick_theme(data)
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    template = Template(template_text)
    return template.render(**data)


def html_to_png(html: str, output_path: str, width: int = 1200) -> str:
    """使用 Playwright 将 HTML 渲染为 PNG 图片。"""
    from playwright.sync_api import sync_playwright

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 800})
        page.set_content(html, wait_until="networkidle")
        # 让页面自适应高度
        height = page.evaluate("document.documentElement.scrollHeight")
        page.set_viewport_size({"width": width, "height": height})
        page.screenshot(path=str(out), full_page=True, type="png")
        browser.close()

    return str(out)


def generate_poster(
    data: dict,
    output_path: str = "output/poster.png",
    width: int = 1200,
) -> str:
    """主入口：从数据字典生成海报图片，返回输出路径。"""
    html = render_html(data)
    return html_to_png(html, output_path, width)


@click.command()
@click.option("--json", "json_path", type=click.Path(exists=True), help="JSON 数据文件")
@click.option("--yaml", "yaml_path", type=click.Path(exists=True), help="YAML 数据文件")
@click.option("--output", "-o", default="output/poster.png", help="输出图片路径")
@click.option("--width", "-w", default=1200, type=int, help="海报宽度(px)")
def main(json_path: str | None, yaml_path: str | None, output: str, width: int):
    """生成内容卡片海报图片。"""
    data = load_data(json_path, yaml_path)
    result = generate_poster(data, output, width)
    click.echo(f"✅ 海报已生成: {result}")


if __name__ == "__main__":
    main()
