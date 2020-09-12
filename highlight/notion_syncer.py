import itertools
import operator
import os
import time
from typing import List, Callable, Tuple

from notion.block import BasicBlock, Children, SubheaderBlock, DividerBlock, QuoteBlock
from notion.client import NotionClient

from highlight.kindle import kindle_parser
from highlight.kindle.clipping import Clipping
from highlight.koreader import koreader_parser


def render_kindle_book(content: Children, cs: List[Clipping]):
    content.add_new(SubheaderBlock, title=f"{cs[0].title} @{cs[0].author}")
    [content.add_new(QuoteBlock, title=c.content) for c in cs]
    content.add_new(DividerBlock)


def render_kindle_page(page: BasicBlock,
                       clipping_list: List[List[Clipping]],
                       book_render: Callable[[Children, List[Clipping]], None] = render_kindle_book) -> BasicBlock:
    content: Children = page.children
    [c.remove() for c in content]

    page.title = "Kindle Clippings"
    content.add_new("table_of_contents")
    for i, cs in enumerate(clipping_list):
        print(f"Processing {i} out of {len(clipping_list)}...")
        book_render(content, cs)
        # try to avoid exceeding API limit
        time.sleep(5)
    return page


def sync_kindle(token: str,
                page: str,
                file_path: str,
                page_render: Callable[[BasicBlock, List[List[Clipping]]], None] = render_kindle_page):
    clippings: List[Clipping] = sorted(kindle_parser.parse(file_path), key=operator.attrgetter('title'))
    cg = itertools.groupby(clippings, key=lambda c: c.title)
    cl: List[List[Clipping]] = [list(g) for (_, g) in cg]

    client = NotionClient(token_v2=token)
    page_render(client.get_block(page), cl)


def render_koreader_book(content: Children, cs: Tuple[str, List[str]]):
    content.add_new(SubheaderBlock, title=cs[0])
    [content.add_new(QuoteBlock, title=c) for c in cs[1]]
    content.add_new(DividerBlock)


def render_koreader_page(page: BasicBlock,
                         clipping_list: List[Tuple[str, List[str]]],
                         replace: bool,
                         book_render: Callable[
                             [Children, Tuple[str, List[str]]], None] = render_koreader_book,
                         ) -> BasicBlock:
    content: Children = page.children

    if replace:
        [c.remove() for c in content]
        page.title = "KoReader Clippings"
        content.add_new("table_of_contents")
    for i, cs in enumerate(clipping_list):
        print(f"Processing {i} out of {len(clipping_list)}...")
        book_render(content, cs)
        # try to avoid exceeding API limit
        time.sleep(5)
    return page


def sync_koreader(
        token: str,
        page: str,
        path: str,
        page_render: Callable[[BasicBlock, List[Tuple[str, List[str]]], bool], None] = render_koreader_page,
        replace: bool = False
):
    client = NotionClient(token_v2=token)
    cl: List[Tuple[str, List[str]]]
    if os.path.isfile(path):
        cl = [koreader_parser.parse_file(path)]
    elif os.path.isdir(path):
        cl = koreader_parser.parse_dir(path)
    else:
        cl = []
    if cl:
        page_render(client.get_block(page), cl, replace)
