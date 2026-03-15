"""
AI Content Pipeline CLI

一键将Markdown内容格式化并发布到多个平台。

Usage:
    ai-publish format article.md --to juejin,zhihu,wechat
    ai-publish format article.md --to juejin --output output/
    ai-publish platforms  # 列出支持的平台
"""

from __future__ import annotations

from pathlib import Path

import click

from .config import load_config
from .platforms import REGISTRY


@click.group()
@click.version_option(version="0.1.0", prog_name="ai-publish")
def cli():
    """AI Content Pipeline — 多平台内容发布工具"""
    pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--to",
    "platform_names",
    required=True,
    help="目标平台，逗号分隔（如：juejin,zhihu,wechat）",
)
@click.option(
    "--output",
    "-o",
    "output_dir",
    type=click.Path(path_type=Path),
    default=Path("output"),
    help="输出目录（默认：output/）",
)
@click.option("--dry-run", is_flag=True, help="仅预览，不写入文件")
def format(input_file: Path, platform_names: str, output_dir: Path, dry_run: bool):
    """将Markdown格式化为目标平台格式。

    示例：
        ai-publish format article.md --to juejin,zhihu
        ai-publish format article.md --to wechat --output dist/
    """
    import frontmatter

    post = frontmatter.load(str(input_file))
    title = post.metadata.get("title", input_file.stem.replace("-", " ").title())
    content = post.content
    metadata = dict(post.metadata)

    platforms = [p.strip() for p in platform_names.split(",")]

    for platform_name in platforms:
        adapter = REGISTRY.get(platform_name)
        if not adapter:
            click.echo(f"❌ 未知平台: {platform_name}，跳过", err=True)
            continue

        result = adapter.format(title=title, content=content, metadata=metadata)
        ext = adapter.output_extension

        if dry_run:
            click.echo(f"\n{'='*60}")
            click.echo(f"📄 [{platform_name}] 预览：")
            click.echo(f"{'='*60}")
            # 只显示前500字符
            preview = result[:500] + ("..." if len(result) > 500 else "")
            click.echo(preview)
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
            out_path = output_dir / f"{input_file.stem}.{platform_name}{ext}"
            out_path.write_text(result, encoding="utf-8")
            click.echo(f"✅ [{platform_name}] → {out_path}")


@cli.command(name="platforms")
def list_platforms():
    """列出所有支持的平台。"""
    click.echo("📋 支持的平台：\n")
    for name, adapter in REGISTRY.items():
        click.echo(f"  • {name:12s} — {adapter.description}")


if __name__ == "__main__":
    cli()
