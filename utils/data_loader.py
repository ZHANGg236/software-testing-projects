from pathlib import Path

import yaml


def load_yaml(file_path: str | Path) -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"测试数据文件不存在: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"YAML 顶层结构必须是字典: {path}")
    return data
