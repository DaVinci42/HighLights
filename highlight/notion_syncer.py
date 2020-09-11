import itertools
import operator
import time
from typing import List, Callable

from notion.block import BasicBlock, Children, SubheaderBlock, DividerBlock, QuoteBlock
from notion.client import NotionClient

from highlight import parser
from highlight.clipping import Clipping


def render_book(content: Children, cs: List[Clipping]):
    content.add_new(SubheaderBlock, title=f"{cs[0].title} @{cs[0].author}")
    [content.add_new(QuoteBlock, title=c.content) for c in cs]
    content.add_new(DividerBlock)


def render_page(page: BasicBlock,
                clipping_list: List[List[Clipping]],
                book_render: Callable[[Children, List[Clipping]], None] = render_book) -> BasicBlock:
    content: Children = page.children
    [c.remove() for c in content]

    page.title = "Kindle Clippings"
    content.add_new("table_of_contents")
    for cs in clipping_list:
        book_render(content, cs)
        # try to avoid exceeding API limit
        time.sleep(5)
    return page


def sync_kindle(token: str,
                page: str,
                file_path: str,
                page_render: Callable[[BasicBlock, List[List[Clipping]]], None] = render_page):
    clippings: List[Clipping] = sorted(parser.parse(file_path), key=operator.attrgetter('title'))
    cg = itertools.groupby(clippings, key=lambda c: c.title)
    cl: List[List[Clipping]] = [list(g) for (_, g) in cg]

    client = NotionClient(token_v2=token)
    page_render(client.get_block(page), cl)
