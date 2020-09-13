import os
import re
from typing import Tuple, List

from lxml import html


def parse_file(path: str) -> Tuple[str, List[str]]:
    with open(path) as f:
        tree = html.fromstring(f.read())
        template = r"(页码 (\d+) )?([\s\S]+)"
        return (
            tree.xpath('//h2/text()')[0],
            [re.search(template, c, re.MULTILINE).group(3) for c in
             tree.xpath('//div[contains(@style, "12pt")]/span/text()')]
        )


def parse_dir(path: str) -> List[Tuple[str, List[str]]]:
    return [parse_file(os.path.join(path, f)) for f in os.listdir(path) if f.endswith(".html")]
