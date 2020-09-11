import json
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, Final

from pytz import timezone

_WEEKDAY: Final = "一二三四五六日"


@dataclass()
class Clipping:
    title: str
    author: str
    content: str
    timestamp: float
    location: Tuple[int, int]
    page: int = None

    def as_raw(self) -> str:
        loc = f"第 {self.page} 页（位置 #{self.location[0]}-{self.location[1]}）" \
            if self.page else f"位置 #{self.location[0]}-{self.location[1]}"
        t = datetime.fromtimestamp(self.timestamp).astimezone(timezone("Asia/Shanghai"))
        return f"{self.title} ({self.author})\n" \
               f"- 您在{loc}的标注 | 添加于 {t.year}年{t.month}月{t.day}日星期{_WEEKDAY[t.weekday()]} " \
               f"{'上午' if t.hour <= 12 else '下午'}{t.hour}:{t.minute}:{t.second}" \
               "\n\n" \
               f"{self.content}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)


def from_json(raw) -> Clipping:
    d = json.loads(raw)
    return Clipping(title=d['title'], author=d['author'], content=d['content'], timestamp=d['timestamp'],
                    location=d['location'], page=d['page'])
