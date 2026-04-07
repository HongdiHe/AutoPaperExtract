#!/usr/bin/env python3
"""
归一化所有论文 MD 文件：
1. section 名别名 → canonical 名
2. 标记综述论文（在基本信息表中加入「论文类型」字段）
3. 修复源文件路径
"""

import os
import re
import csv
from schema import (OUTPUT_DIR, BASE_DIR, list_paper_mds, normalize_sections,
                    atomic_write, is_review_paper)

# 建立 PDF 路径映射
PDF_DIR_MAP = {}
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.pdf'):
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
            PDF_DIR_MAP[f] = './' + rel.replace('\\', '/')


def normalize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 1. 归一化 section 名
    content = normalize_sections(content)
    if content != original:
        changes.append('section名归一化')

    # 2. 去掉表格中的加粗字段名
    new_content = re.sub(r'\|\s*\*\*([^*]+)\*\*\s*\|', r'| \1 |', content)
    if new_content != content:
        content = new_content
        changes.append('去除加粗字段名')

    # 3. 去掉多余的「文件名」和「标题」行
    for field in ['文件名', '标题']:
        pattern = rf'\|\s*{field}\s*\|[^\n]*\n'
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes.append(f'移除多余{field}行')

    # 4. DOI 超链接 → 纯文本
    doi_pattern = r'\[([^\]]*10\.[^\]]+)\]\(https?://doi\.org/[^\)]+\)'
    if re.search(doi_pattern, content):
        content = re.sub(doi_pattern, r'\1', content)
        changes.append('DOI去超链接')

    # 5. 关键词列表格式 → 逗号分隔
    kw_match = re.search(r'(## 关键词\s*\n)(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if kw_match:
        kw_body = kw_match.group(2).strip()
        if re.search(r'^-\s', kw_body, re.MULTILINE):
            keywords = [line.strip().lstrip('- ').strip() for line in kw_body.split('\n') if line.strip()]
            new_kw = ', '.join(keywords)
            content = content[:kw_match.start(2)] + '\n' + new_kw + '\n' + content[kw_match.end(2):]
            changes.append('关键词改逗号分隔')

    # 6. 修复源文件路径
    src_match = re.search(r'(## 源文件\s*\n\s*`)(.*?\.pdf)(`)', content)
    if src_match:
        current_path = src_match.group(2)
        pdf_name = os.path.basename(current_path.replace('_', ' '))
        correct_path = None
        for name, path in PDF_DIR_MAP.items():
            if name == pdf_name:
                correct_path = path
                break
            if name[:30] == pdf_name[:30]:
                correct_path = path
                break
        if correct_path and correct_path != current_path:
            content = content[:src_match.start(2)] + correct_path + content[src_match.end(2):]
            changes.append('修复源文件路径')

    # 7. 标记综述论文
    journal_match = re.search(r'期刊\s*\|\s*(.*?)(?:\s*\||\s*$)', content, re.MULTILINE)
    title_match = re.match(r'#\s+(.+)', content)
    kw_section = re.search(r'## 关键词\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)

    journal = journal_match.group(1).strip() if journal_match else ''
    title = title_match.group(1).strip() if title_match else ''
    keywords = kw_section.group(1).strip() if kw_section else ''

    is_review, reason = is_review_paper(journal, title, keywords)
    if is_review and '论文类型' not in content:
        # 在基本信息表末尾（DOI 行之后）插入论文类型行
        doi_line = re.search(r'(\|\s*DOI\s*\|[^\n]*\n)', content)
        if doi_line:
            insert_pos = doi_line.end()
            type_line = f'| 论文类型 | 综述 ({reason}) |\n'
            content = content[:insert_pos] + type_line + content[insert_pos:]
            changes.append(f'标记为综述({reason})')

    if content != original:
        atomic_write(filepath, content)
        return changes
    return []


def main():
    files = list_paper_mds()
    total = len(files)
    changed = 0
    review_count = 0

    for filepath in files:
        changes = normalize_file(filepath)
        if changes:
            changed += 1
            print(f"  修改: {os.path.basename(filepath)[:60]}")
            for c in changes:
                print(f"    - {c}")

    # 统计综述
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            if '论文类型 | 综述' in f.read():
                review_count += 1

    print(f"\n归一化完成: {total} 篇, 修改了 {changed} 篇, 其中 {review_count} 篇标记为综述")


if __name__ == '__main__':
    main()
