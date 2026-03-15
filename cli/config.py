"""配置管理：加载用户配置和平台凭据。"""

from __future__ import annotations

from pathlib import Path

import yaml


DEFAULT_CONFIG_PATH = Path.home() / ".ai-content-pipeline" / "config.yaml"

DEFAULT_CONFIG = {
    "default_platforms": ["juejin", "zhihu"],
    "output_dir": "output",
    "author": "",
    "image_host": {
        "provider": "local",  # local | smms | imgur
        "api_key": "",
    },
}


def load_config(config_path: Path | None = None) -> dict:
    """加载配置文件，不存在则返回默认配置。"""
    path = config_path or DEFAULT_CONFIG_PATH
    if path.exists():
        with open(path, encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        merged = {**DEFAULT_CONFIG, **user_config}
        return merged
    return dict(DEFAULT_CONFIG)
