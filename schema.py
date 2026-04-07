#!/usr/bin/env python3
"""
统一 schema 定义 — 所有脚本共享此模块
解决跨工具模板漂移问题（Codex Phase 0 #2）
"""

import os
import re

# === 路径常量 ===
BASE_DIR = "/mnt/c/Users/hehon/claude work place/配位驱动自组装/try"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CSV_PATH = os.path.join(OUTPUT_DIR, "papers_database.csv")

# === 论文 MD 的 canonical section 名 ===
REQUIRED_SECTIONS = [
    '## 基本信息',
    '## 关键词',
    '## 摘要',
    '## 主要内容',
    '### 研究背景',
    '### 研究方法',
    '### 关键结果',
    '### 结论',
    '## 涉及的配体/金属/结构',
    '## 源文件',
]

# === section 名别名映射（归一化用）===
SECTION_ALIASES = {
    '## 来源文件': '## 源文件',
    '## 原始文件': '## 源文件',
    '### 研究结果': '### 关键结果',
    '### 主要发现': '### 关键结果',
    '### 研究亮点': '### 关键结果',
    '### 主要结果': '### 关键结果',
    '## 配体/金属/结构': '## 涉及的配体/金属/结构',
}

# === 表格必填字段 ===
TABLE_FIELDS = ['作者', '期刊', '年份', '卷号', '期号', '页码', 'DOI']

# === 化学术语对照表（硬约束）===
TERM_TABLE = {
    # 英文 -> 中文标准译名
    'terpyridine': '三联吡啶',
    'tpy': '三联吡啶',
    'bipyridine': '联吡啶',
    'bpy': '联吡啶',
    'tris(bipyridine)': '三(联吡啶)',
    'tris-bipyridine': '三(联吡啶)',
    'pyridine': '吡啶',
}

# === 综述论文识别 ===
REVIEW_JOURNALS = [
    "Chemical Reviews", "Chemical Society Reviews", "Chem. Soc. Rev.",
    "Accounts of Chemical Research", "Acc. Chem. Res.",
    "Nature Reviews", "Nat. Rev.", "Coordination Chemistry Reviews",
    "Progress in Polymer Science", "Annual Review",
    "Macromolecular Rapid Communications",
]
REVIEW_KEYWORDS = ["review", "综述", "perspective", "tutorial", "progress report", "account"]

# === 非论文 MD 文件名排除列表 ===
NON_PAPER_FILES = {
    'quality_report.md', 'discovery_report.md',
    'review_draft.md', 'review_final.md', 'review_log.md',
    'review_candidates.md', 'literature_landscape.md',
    'audit_report.txt', 'validate_report.txt',
}


def is_paper_md(filename):
    """判断一个 MD 文件是否是论文卡片（而非系统产物）"""
    if not filename.endswith('.md'):
        return False
    if filename in NON_PAPER_FILES:
        return False
    if filename.startswith('review_') or filename.startswith('literature_'):
        return False
    return True


def is_review_paper(journal, title, keywords):
    """判断一篇论文是否是综述"""
    journal_lower = journal.lower() if journal else ''
    title_lower = title.lower() if title else ''
    keywords_lower = keywords.lower() if keywords else ''

    for rj in REVIEW_JOURNALS:
        if rj.lower() in journal_lower:
            return True, f"综述期刊({journal})"
    for rk in REVIEW_KEYWORDS:
        if rk in title_lower or rk in keywords_lower:
            return True, f"含关键词({rk})"
    return False, ""


def normalize_sections(content):
    """将 section 别名归一化为 canonical 名称"""
    for alias, canonical in SECTION_ALIASES.items():
        content = content.replace(alias, canonical)
    return content


def atomic_write(filepath, content, encoding='utf-8'):
    """原子写入：先写临时文件，再 rename（防止半截文件）"""
    tmp_path = filepath + '.tmp'
    with open(tmp_path, 'w', encoding=encoding) as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, filepath)


def list_paper_mds():
    """列出所有论文 MD 文件路径"""
    result = []
    for fname in sorted(os.listdir(OUTPUT_DIR)):
        if is_paper_md(fname):
            result.append(os.path.join(OUTPUT_DIR, fname))
    return result
