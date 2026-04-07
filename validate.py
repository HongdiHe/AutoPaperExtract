#!/usr/bin/env python3
"""严格校验 MD 文件是否符合 program.md v2 模板"""

import os
import re
import sys

OUTPUT_DIR = "/mnt/c/Users/hehon/claude work place/配位驱动自组装/try/output"

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

REQUIRED_TABLE_FIELDS = ['作者', '期刊', '年份', '卷号', '期号', '页码', 'DOI']

FORBIDDEN_PATTERNS = [
    (r'\|\s*\*\*', '表格字段名加粗'),
    (r'\|\s*\*?\*?文件名\*?\*?\s*\|', '表格含多余的「文件名」行'),
    (r'\|\s*\*?\*?标题\*?\*?\s*\|', '表格含多余的「标题」行'),
    (r'\[10\.\d+[^\]]*\]\(https?://doi', 'DOI 使用了超链接格式'),
    (r'### 研究结果', 'section 名漂移：「研究结果」应为「关键结果」'),
    (r'### 研究亮点', 'section 名漂移：「研究亮点」应为「关键结果」'),
    (r'### 主要发现', 'section 名漂移：「主要发现」应为「关键结果」'),
]


def validate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    fname = os.path.basename(filepath)
    size = os.path.getsize(filepath)

    # 1. 检查文件大小
    if size < 2000:
        issues.append(('WARN', f'文件过小 ({size} bytes)，可能缺少主要内容'))

    # 2. 检查必要章节
    for section in REQUIRED_SECTIONS:
        if section not in content:
            # 尝试模糊匹配（section 名漂移）
            base = section.lstrip('#').strip()
            if not re.search(re.escape(base), content, re.IGNORECASE):
                issues.append(('ERROR', f'缺少章节: {section}'))

    # 3. 检查表格字段
    for field in REQUIRED_TABLE_FIELDS:
        pattern = rf'\|\s*\*?\*?{field}\*?\*?\s*\|'
        if not re.search(pattern, content):
            issues.append(('ERROR', f'表格缺少字段: {field}'))

    # 4. 检查禁止的格式
    for pattern, desc in FORBIDDEN_PATTERNS:
        if re.search(pattern, content):
            issues.append(('WARN', f'格式违规: {desc}'))

    # 5. 检查关键词格式
    kw_match = re.search(r'## 关键词\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if kw_match:
        kw_body = kw_match.group(1).strip()
        if re.search(r'^-\s', kw_body, re.MULTILINE):
            issues.append(('WARN', '关键词使用了列表格式（应为逗号分隔）'))
        cn_chars = sum(1 for c in kw_body if '\u4e00' <= c <= '\u9fff')
        if cn_chars > 3:
            issues.append(('WARN', '关键词包含中文'))

    # 6. 检查摘要语言
    abs_match = re.search(r'## 摘要\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if abs_match:
        abs_body = abs_match.group(1).strip()
        cn_chars = sum(1 for c in abs_body if '\u4e00' <= c <= '\u9fff')
        if cn_chars > 20:
            issues.append(('INFO', f'摘要为中文 ({cn_chars} 个中文字符)'))

    # 7. 检查源文件路径格式
    src_match = re.search(r'## 源文件\s*\n\s*`([^`]*)`', content)
    if src_match:
        src_path = src_match.group(1)
        if not src_path.startswith('./'):
            issues.append(('WARN', f'源文件路径缺少 ./ 前缀: {src_path[:50]}'))
        if not src_path.endswith('.pdf'):
            issues.append(('WARN', f'源文件路径不以 .pdf 结尾'))
    else:
        issues.append(('ERROR', '找不到源文件路径'))

    # 8. 检查主要内容的最小长度
    for section_name in ['研究背景', '研究方法', '关键结果', '结论']:
        pattern = rf'### {section_name}\s*\n(.*?)(?=\n###|\n##|\Z)'
        m = re.search(pattern, content, re.DOTALL)
        if m:
            body = m.group(1).strip()
            sentences = [s for s in re.split(r'[。.!！]', body) if len(s.strip()) > 5]
            if len(sentences) < 2:
                issues.append(('WARN', f'「{section_name}」内容过短 ({len(sentences)} 句)'))

    return issues


def main():
    total = 0
    pass_count = 0
    error_count = 0
    warn_count = 0
    info_count = 0
    all_issues = {}

    try:
        from schema import list_paper_mds
        paper_files = list_paper_mds()
    except ImportError:
        paper_files = [os.path.join(OUTPUT_DIR, f) for f in sorted(os.listdir(OUTPUT_DIR))
                       if f.endswith('.md') and f not in ('quality_report.md',)]

    for filepath in paper_files:
        fname = os.path.basename(filepath)
        issues = validate_file(filepath)
        total += 1

        if not issues:
            pass_count += 1
        else:
            all_issues[fname] = issues
            for level, _ in issues:
                if level == 'ERROR':
                    error_count += 1
                elif level == 'WARN':
                    warn_count += 1
                else:
                    info_count += 1

    # 输出报告
    print(f"=== 校验报告 ===")
    print(f"总计: {total} 个文件")
    print(f"通过: {pass_count}")
    print(f"ERROR: {error_count} | WARN: {warn_count} | INFO: {info_count}")
    print()

    # 按问题类型统计
    issue_summary = {}
    for fname, issues in all_issues.items():
        for level, desc in issues:
            key = f"[{level}] {desc}" if not any(c in desc for c in '0123456789') else f"[{level}] {desc.split(':')[0]}..."
            issue_summary.setdefault(desc, []).append(fname)

    print("=== 问题汇总（按类型）===")
    for desc, files in sorted(issue_summary.items(), key=lambda x: -len(x[1])):
        print(f"\n{desc}: {len(files)} 个文件")
        if len(files) <= 5:
            for f in files:
                print(f"  - {f[:70]}")
        else:
            for f in files[:3]:
                print(f"  - {f[:70]}")
            print(f"  ... 还有 {len(files)-3} 个")

    # 退出码
    sys.exit(1 if error_count > 0 else 0)


if __name__ == '__main__':
    main()
