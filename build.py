#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按手动指定顺序拼接 Markdown 文件。
"""

import sys
from pathlib import Path

MD_FILES = [
    "亲族与共约4.1.md",
    "亲族与共约/单性生殖、古典社会与乌托邦.md",
    "亲族与共约/古典时期民族印象.md",
    "亲族与共约/铁路、电网、电报与民族国家.md",
    "亲族与共约/意识国家、现代国家与新秩序.md",
    "亲族与共约/现存政权列表.md",
]

TARGET = "亲族与共约4.1.txt"

def main() -> int:
    base_dir = Path(__file__).resolve().parent

    parts: list[str] = []
    missing: list[str] = []

    for rel in MD_FILES:
        path = base_dir / rel
        if not path.is_file():
            missing.append(rel)
            continue

        text = path.read_text(encoding="utf-8")

        if text.startswith("\ufeff"):
            text = text[1:]

        parts.append(text.rstrip() + "\n")

    if missing:
        print("以下文件不存在，已中止：", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    # 文件之间用两个换行分隔，保证 Markdown 段落/标题不被粘连
    merged = "\n\n".join(parts)

    target_path = base_dir / TARGET
    target_path.write_text(merged, encoding="utf-8")

    print(
        f"已生成 {target_path}\n"
        f"共拼接 {len(parts)} 个文件，{len(merged)} 字符。"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
