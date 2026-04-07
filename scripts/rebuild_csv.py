#!/usr/bin/env python3
"""从 output/ 目录的 MD 文件重建 papers_database.csv"""

import os
import re
import csv

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "papers")

def extract_field(content, field_name):
    """从 MD 表格中提取字段值"""
    # 匹配 | 字段名 | 值 | 或 | **字段名** | 值 | 格式
    patterns = [
        rf'\|\s*\*?\*?{field_name}\*?\*?\s*\|\s*(.*?)\s*\|',
        rf'\|\s*\*?\*?{field_name}\*?\*?\s*\|\s*(.*?)\s*$',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.MULTILINE | re.IGNORECASE)
        if m:
            val = m.group(1).strip().strip('|').strip()
            # 清理超链接格式 [text](url) -> text
            val = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', val)
            return val
    return ""

def extract_section(content, section_name):
    """提取 ## 或 ### 段落内容"""
    pattern = rf'##\s*{section_name}\s*\n(.*?)(?=\n##|\Z)'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # 去掉列表符号，合并为单行
        lines = [l.strip().lstrip('- ').strip() for l in text.split('\n') if l.strip()]
        return '; '.join(lines) if lines else ""
    return ""

def extract_source_file(content):
    """提取源文件路径中的文件名"""
    m = re.search(r'`([^`]*\.pdf)`', content)
    if m:
        path = m.group(1)
        return os.path.basename(path)
    return ""

def extract_title(content):
    """提取标题（第一个 # 开头的行）"""
    m = re.match(r'#\s+(.+)', content)
    if m:
        return m.group(1).strip()
    return ""

def process_md(filepath):
    """处理单个 MD 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title = extract_title(content)
    authors = extract_field(content, '作者')
    journal = extract_field(content, '期刊')
    year = extract_field(content, '年份')
    volume = extract_field(content, '卷号')
    issue = extract_field(content, '期号')
    pages = extract_field(content, '页码')
    doi = extract_field(content, 'DOI')

    keywords = extract_section(content, '关键词')
    abstract = extract_section(content, '摘要')

    source_file = extract_source_file(content)
    if not source_file:
        # 从 MD 文件名推断
        md_name = os.path.basename(filepath).replace('.md', '').replace('_', ' ')
        source_file = md_name + '.pdf'

    return {
        '文件名': source_file,
        '标题': title,
        '作者': authors,
        '期刊名': journal,
        '年份': year,
        '卷号': volume,
        '期号': issue,
        '页码': pages,
        'DOI': doi,
        '关键词': keywords,
        '摘要': abstract,
    }

def main():
    rows = []
    skipped = []

    # 使用 schema 的统一过滤器（避免把 review_draft.md 等当成论文）
    try:
        from schema import list_paper_mds, atomic_write, is_review_paper
        paper_files = list_paper_mds()
    except ImportError:
        paper_files = [os.path.join(OUTPUT_DIR, f) for f in sorted(os.listdir(OUTPUT_DIR))
                       if f.endswith('.md') and f not in ('quality_report.md', 'review_draft.md',
                       'review_final.md', 'review_log.md', 'review_candidates.md',
                       'literature_landscape.md', 'discovery_report.md')]

    for filepath in paper_files:
        try:
            row = process_md(filepath)
            if row['标题']:
                rows.append(row)
            else:
                skipped.append(fname)
        except Exception as e:
            skipped.append(f"{fname} (error: {e})")

    # 写入 CSV
    csv_path = os.path.join(os.path.dirname(OUTPUT_DIR), 'papers_database.csv')  # output/papers_database.csv
    fieldnames = ['文件名', '标题', '作者', '期刊名', '年份', '卷号', '期号', '页码', 'DOI', '关键词', '摘要']

    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV 重建完成: {len(rows)} 条记录")
    if skipped:
        print(f"跳过 {len(skipped)} 个文件: {skipped}")

if __name__ == '__main__':
    main()
