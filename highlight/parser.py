import re
from datetime import datetime
from re import Match
from typing import List, AnyStr

from pytz import timezone

from highlight.clipping import Clipping

CLIPPING_DIVIDER = "=========="


def parse(path: str) -> List[Clipping]:
    with open(path) as f:
        return [_parseClipping(c) for c in f.read().split(CLIPPING_DIVIDER) if c.strip()]


# """
# 百年孤独 (加西亚·马尔克斯)
# - 您在位置 #12-13的标注 | 添加于 2018年11月18日星期日 下午7:48:45
#
# 多年以后，面对行刑队，奥雷里亚诺·布恩迪亚上校将会回想起父亲带他去见识冰块的那个遥远的下午。
# ==========
# 围城（爱熄灭了灯，心围一座城。出版七十周年纪念版） (钱钟书)
# - 您在第 24 页（位置 #935-935）的标注 | 添加于 2019年4月6日星期六 下午6:34:26
#
# 约她们是七点半，看表才七点四十分，决不会这时候。
# """
def _parseClipping(raw: str) -> Clipping:
    template = r'(.+) \((.+)\)\n+' \
               r'(.+第 (\d+) 页)?.+(位置 #(\d+)-(\d+))' \
               r'.+(\d{4})年(\d{1,2})月(\d{1,2})日.+(下)?午(\d{1,2}):(\d{1,2}):(\d{1,2})\s+' \
               r'(.+)'
    m = re.search(template, raw)

    hour = int(m.group(12))
    if m.group(11) and hour != 12:
        hour += 12

    time: float = _parse_local_timestamp(year=_int_group(m, 8),
                                         month=_int_group(m, 9),
                                         day=_int_group(m, 10),
                                         hour=hour,
                                         minute=_int_group(m, 13),
                                         second=_int_group(m, 14))
    return Clipping(title=m.group(1),
                    author=m.group(2),
                    page=_int_group(m, 4),
                    location=(_int_group(m, 6), _int_group(m, 7)),
                    timestamp=time,
                    content=m.group(15))


def _parse_local_timestamp(year: int, month: int, day: int, hour: int, minute: int, second: int,
                           tz: timezone = timezone("Asia/Shanghai")) -> float:
    return datetime.timestamp(datetime(year=year,
                                       month=month,
                                       day=day,
                                       hour=hour,
                                       minute=minute,
                                       second=second, tzinfo=tz))


def _int_group(m: Match, index: int) -> int:
    g: AnyStr = m.group(index)
    return int(g) if g else None
