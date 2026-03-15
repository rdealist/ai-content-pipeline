"""
blog-from-spec: 根据Spec文件生成技术博客初稿的脚本。

可单独运行，也可作为CLI子命令使用。
读取YAML Spec → 结合Prompt模板 → 输出博客骨架Markdown。
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import click
import yaml


PROMPT_TEMPLATE_PATH = Path(__file__).parent.parent.parent / "prompts" / "tech-blog-v1.md"


def parse_spec(spec_path: Path) -> dict:
    """解析Spec文件（Markdown中的YAML块或纯YAML）。"""
    text = spec_path.read_text(encoding="utf-8")

    # 尝试提取YAML frontmatter
    match = re.match(r"^---\s*\n(.+?)\n---", text, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))

    # 尝试整体解析为YAML（跳过Markdown标题行）
    yaml_lines = []
    for line in text.split("\n"):
        if line.startswith("#") or line.startswith("---"):
            continue
        yaml_lines.append(line)
    yaml_text = "\n".join(yaml_lines).strip()
    if yaml_text:
        try:
            return yaml.safe_load(yaml_text) or {}
        except yaml.YAMLError:
            pass

    return {}


def slugify(title: str) -> str:
    """将标题转换为文件名安全的slug。"""
    # 简单slug：移除特殊字符，空格和冒号转为连字符
    slug = re.sub(r"[：:？?！!《》「」]", "", title)
    slug = re.sub(r"[\s]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug.lower()


def generate_skeleton(spec: dict) -> str:
    """根据Spec生成博客骨架Markdown。"""
    title = spec.get("title", "Untitled")
    topic = spec.get("topic", "")
    key_points = spec.get("key_points", [])
    pain_point = spec.get("pain_point", "")
    unique_angle = spec.get("unique_angle", "")
    code_language = spec.get("code_language", "")
    word_count = spec.get("word_count", "2000-3000")
    target_audience = spec.get("target_audience", "")

    today = date.today().isoformat()

    parts = [
        f"---",
        f"title: \"{title}\"",
        f"date: \"{today}\"",
        f"tags: [{topic}]",
        f"description: \"{pain_point}\"",
        f"draft: true",
        f"---",
        f"",
        f"# {title}",
        f"",
        f"<!-- 目标读者：{target_audience} -->",
        f"<!-- 目标字数：{word_count} -->",
        f"",
        f"## 引子",
        f"",
        f"<!-- 以一个具体场景/问题开头，让读者产生共鸣 -->",
        f"<!-- 痛点：{pain_point} -->",
        f"",
        f"[在这里描述一个读者会遇到的具体场景...]",
        f"",
    ]

    # 问题拆解
    if key_points:
        parts.append("## 问题拆解")
        parts.append("")
        for i, point in enumerate(key_points, 1):
            parts.append(f"{i}. **{point}**")
        parts.append("")

    # 每个要点的解决方案
    for i, point in enumerate(key_points, 1):
        parts.append(f"## {point}")
        parts.append("")
        parts.append(f"<!-- 解释「为什么」而不仅仅是「怎么做」 -->")
        parts.append("")
        parts.append("[详细分析和解决方案...]")
        parts.append("")
        if code_language:
            parts.append(f"```{code_language.split(',')[0].strip().lower()}")
            parts.append(f"# 代码示例（不超过30行）")
            parts.append(f"```")
            parts.append("")

    # 实战经验
    parts.extend([
        "## 实战经验",
        "",
        f"<!-- 独特视角：{unique_angle} -->",
        "",
        "[分享一个真实项目中的应用案例或踩坑经历...]",
        "",
    ])

    # 总结
    parts.extend([
        "## 总结",
        "",
        "### Takeaway",
        "",
    ])
    for i in range(1, min(len(key_points) + 1, 6)):
        parts.append(f"{i}. [可执行的要点 {i}]")
    parts.extend([
        "",
        "### 讨论",
        "",
        "[引导讨论的开放性问题]",
        "",
        "---",
        "",
        "*本文使用 [AI Content Pipeline](https://github.com/user/ai-content-pipeline) 辅助生成。*",
    ])

    return "\n".join(parts)


@click.command()
@click.argument("spec_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default=Path("output"),
    help="输出目录",
)
def main(spec_file: Path, output_dir: Path):
    """根据Spec文件生成博客骨架。

    示例：
        python blog_generator.py specs/example-spec.md
    """
    spec = parse_spec(spec_file)
    if not spec:
        click.echo("❌ 无法解析Spec文件，请检查格式", err=True)
        raise SystemExit(1)

    title = spec.get("title", "untitled")
    skeleton = generate_skeleton(spec)

    output_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(title)
    out_path = output_dir / f"{slug}.md"
    out_path.write_text(skeleton, encoding="utf-8")

    click.echo(f"✅ 博客骨架已生成: {out_path}")
    click.echo(f"   标题: {title}")
    click.echo(f"   要点: {len(spec.get('key_points', []))}个")
    click.echo(f"\n下一步: 使用AI工具（配合 prompts/tech-blog-v1.md）填充内容")


if __name__ == "__main__":
    main()
