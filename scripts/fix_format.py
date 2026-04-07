#!/usr/bin/env python3
"""批量修复 MD 文件格式问题"""

import os
import re

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "papers")

# PDF 文件名 -> 正确的相对路径映射
PDF_DIR_MAP = {}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.pdf'):
            rel = os.path.relpath(os.path.join(root, f), BASE_DIR)
            PDF_DIR_MAP[f] = './' + rel.replace('\\', '/')

stats = {
    'bold_fixed': 0,
    'filename_row_removed': 0,
    'doi_fixed': 0,
    'keywords_fixed': 0,
    'source_fixed': 0,
    'total': 0,
}

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # 1. 移除表格中的「文件名」行
    pattern = r'\|\s*\*?\*?文件名\*?\*?\s*\|[^\n]*\n'
    if re.search(pattern, content):
        content = re.sub(pattern, '', content)
        stats['filename_row_removed'] += 1
        changed = True

    # 同时移除「标题」行（标题已在 # 标题中，表格里重复了）
    pattern = r'\|\s*\*?\*?标题\*?\*?\s*\|[^\n]*\n'
    if re.search(pattern, content):
        content = re.sub(pattern, '', content)
        changed = True

    # 2. 统一表格字段名：去掉加粗
    def debold_field(m):
        return f'| {m.group(1)} |'
    content_new = re.sub(r'\|\s*\*\*([^*]+)\*\*\s*\|', debold_field, content)
    if content_new != content:
        stats['bold_fixed'] += 1
        content = content_new
        changed = True

    # 3. DOI 格式统一为纯文本（去掉超链接）
    doi_link = re.search(r'\[([^\]]*10\.[^\]]+)\]\(https?://doi\.org/[^\)]+\)', content)
    if doi_link:
        content = re.sub(
            r'\[([^\]]*10\.[^\]]+)\]\(https?://doi\.org/[^\)]+\)',
            r'\1',
            content
        )
        stats['doi_fixed'] += 1
        changed = True

    # 4. 关键词格式统一：列表格式 -> 逗号分隔；分号 -> 逗号
    kw_section = re.search(r'(## 关键词\s*\n)(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if kw_section:
        kw_body = kw_section.group(2).strip()
        # 如果是列表格式（- keyword）
        if re.search(r'^-\s', kw_body, re.MULTILINE):
            keywords = [line.strip().lstrip('- ').strip() for line in kw_body.split('\n') if line.strip()]
            new_kw = ', '.join(keywords)
            content = content[:kw_section.start(2)] + '\n' + new_kw + '\n' + content[kw_section.end(2):]
            stats['keywords_fixed'] += 1
            changed = True
        # 分号分隔 -> 逗号分隔
        elif ';' in kw_body and ',' not in kw_body:
            new_kw = kw_body.replace(';', ',')
            content = content[:kw_section.start(2)] + '\n' + new_kw + '\n' + content[kw_section.end(2):]
            stats['keywords_fixed'] += 1
            changed = True

    # 5. 修复源文件路径
    source_section = re.search(r'(## 源文件\s*\n\s*`)(.*?\.pdf)(`)', content)
    if source_section:
        current_path = source_section.group(2)
        # 从路径中提取文件名
        pdf_name = os.path.basename(current_path.replace('_', ' '))
        # 也尝试保留下划线的版本
        pdf_name_underscore = os.path.basename(current_path)

        correct_path = None
        for name, path in PDF_DIR_MAP.items():
            if name == pdf_name or name == pdf_name_underscore:
                correct_path = path
                break
            # 模糊匹配：前30字符
            if name[:30] == pdf_name[:30] or name[:30] == pdf_name_underscore[:30]:
                correct_path = path
                break

        if correct_path and correct_path != current_path:
            content = content[:source_section.start(2)] + correct_path + content[source_section.end(2):]
            stats['source_fixed'] += 1
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    stats['total'] += 1
    return changed

def main():
    fixed_count = 0
    for fname in sorted(os.listdir(OUTPUT_DIR)):
        if not fname.endswith('.md') or fname in ('quality_report.md',):
            continue
        filepath = os.path.join(OUTPUT_DIR, fname)
        if fix_file(filepath):
            fixed_count += 1

    print(f"处理完成: {stats['total']} 个文件")
    print(f"修复了 {fixed_count} 个文件:")
    print(f"  - 移除加粗字段名: {stats['bold_fixed']}")
    print(f"  - 移除多余文件名行: {stats['filename_row_removed']}")
    print(f"  - 统一 DOI 格式: {stats['doi_fixed']}")
    print(f"  - 统一关键词格式: {stats['keywords_fixed']}")
    print(f"  - 修复源文件路径: {stats['source_fixed']}")

if __name__ == '__main__':
    main()
