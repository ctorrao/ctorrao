#!/usr/bin/env python3
"""Build README.md and index.html from data/profile.json and templates/."""

import json
from pathlib import Path
from urllib.parse import quote_plus

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent.parent
DATA_FILE = ROOT / "data" / "profile.json"
TEMPLATE_DIR = ROOT / "templates"

OUTPUTS = [
    ("README.md.jinja", "README.md"),
    ("index.html.jinja", "index.html"),
]


def typing_svg_lines(items: list[str]) -> str:
    """Encode a list of strings for the readme-typing-svg ``lines`` query param.

    Each string is percent-encoded (spaces become ``+``, ``&`` becomes ``%26``),
    then the entries are joined with ``;``.
    """
    return ";".join(quote_plus(item) for item in items)


def main() -> None:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        keep_trailing_newline=True,
        autoescape=select_autoescape(enabled_extensions=("html.jinja",)),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    env.filters["typing_svg_lines"] = typing_svg_lines

    for template_name, output_name in OUTPUTS:
        template = env.get_template(template_name)
        output = template.render(**data)
        output_path = ROOT / output_name
        output_path.write_text(output, encoding="utf-8")
        print(f"Generated {output_name}")


if __name__ == "__main__":
    main()
