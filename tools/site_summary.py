#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/site_summary.py – 读取内置站点资料并输出结构化摘要"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ── 内置站点资料 ──────────────────────────────────────────────
_SITES_DATA = [
    {
        "title": "乐鱼体育",
        "url": "https://app-page-leyu.com.cn",
        "tags": ["体育", "赛事", "直播", "互动"],
        "description": "综合性体育资讯与赛事直播平台，覆盖足球、篮球、网球等主流项目。"
    },
    {
        "title": "资讯频道",
        "url": "https://app-page-leyu.com.cn/news",
        "tags": ["新闻", "快讯", "分析"],
        "description": "提供实时体育新闻、深度赛事分析与专家评论。"
    },
    {
        "title": "社区中心",
        "url": "https://app-page-leyu.com.cn/community",
        "tags": ["用户", "论坛", "讨论"],
        "description": "球迷交流社区，支持话题讨论、比分竞猜与动态分享。"
    }
]

# ── 数据模型 ───────────────────────────────────────────────────
@dataclass
class SiteEntry:
    title: str
    url: str
    tags: List[str]
    description: str
    keywords: List[str] = field(default_factory=list)

    def __post_init__(self):
        # 从标题和标签自动提取关键词
        self.keywords = [self.title] + self.tags

# ── 摘要生成器 ──────────────────────────────────────────────────
class SiteSummaryGenerator:
    def __init__(self, raw_data: List[Dict[str, str]]):
        self.entries = [SiteEntry(**item) for item in raw_data]

    def generate_summary(self) -> str:
        lines = []
        lines.append("=" * 50)
        lines.append("         站点摘要报告")
        lines.append("=" * 50)
        for entry in self.entries:
            lines.append(f"\n▶ 名称   : {entry.title}")
            lines.append(f"  URL    : {entry.url}")
            lines.append(f"  标签   : {', '.join(entry.tags)}")
            lines.append(f"  简介   : {entry.description}")
            lines.append(f"  关键词 : {', '.join(entry.keywords)}")
        lines.append("\n" + "─" * 50)
        lines.append(f"共收录 {len(self.entries)} 个站点")
        return "\n".join(lines)

# ── 输出格式选项 ──────────────────────────────────────────────
def format_as_json(entries: List[SiteEntry]) -> str:
    output = []
    for e in entries:
        output.append({
            "title": e.title,
            "url": e.url,
            "tags": e.tags,
            "description": e.description
        })
    return json.dumps(output, ensure_ascii=False, indent=2)

def format_as_markdown(entries: List[SiteEntry]) -> str:
    lines = ["# 站点摘要\n"]
    for e in entries:
        lines.append(f"## {e.title}")
        lines.append(f"- **URL**: [{e.url}]({e.url})")
        lines.append(f"- **标签**: {', '.join(e.tags)}")
        lines.append(f"- **简介**: {e.description}")
        lines.append("")
    return "\n".join(lines)

# ── 主入口 ─────────────────────────────────────────────────────
def main():
    generator = SiteSummaryGenerator(_SITES_DATA)
    summary = generator.generate_summary()
    print(summary)

    print("\n\n--- JSON 格式 ---")
    print(format_as_json(generator.entries))

    print("\n\n--- Markdown 格式 ---")
    print(format_as_markdown(generator.entries))

if __name__ == "__main__":
    main()