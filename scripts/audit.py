#!/usr/bin/env python3
"""审计 MD 文件中的潜在事实错误和术语问题"""

import os
import re

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "papers")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 建立 PDF 子目录映射
PDF_SUBDIR = {}
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.pdf'):
            rel = os.path.relpath(root, BASE_DIR)
            PDF_SUBDIR[f] = rel if rel != '.' else '根目录'

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    fname = os.path.basename(filepath)

    # 1. 配体术语交叉检查：单吡啶目录的论文不应该说自己是三联吡啶体系
    source_match = re.search(r'## 源文件\s*\n\s*`([^`]*)`', content)
    if not source_match:
        source_match = re.search(r'## 来源文件\s*\n\s*`([^`]*)`', content)

    if source_match:
        src_path = source_match.group(1)
        if '单吡啶' in src_path:
            # 单吡啶目录的论文
            ligand_section = re.search(r'配体类型[^:：]*[:：]\s*(.*?)(?=\n-|\n#|\Z)', content)
            if ligand_section:
                lig_text = ligand_section.group(1)
                if '三联吡啶' in lig_text and '单吡啶' not in lig_text and '吡啶' in lig_text:
                    issues.append(('HIGH', f'配体术语可疑：单吡啶目录论文但配体写成「三联吡啶」'))
        elif '联吡啶' in src_path and '三联吡啶' not in src_path:
            ligand_section = re.search(r'配体类型[^:：]*[:：]\s*(.*?)(?=\n-|\n#|\Z)', content)
            if ligand_section:
                lig_text = ligand_section.group(1)
                if '三联吡啶' in lig_text and '联吡啶' not in lig_text:
                    issues.append(('HIGH', f'配体术语可疑：联吡啶目录论文但配体写成「三联吡啶」'))

    # 2. terpyridine vs bipyridine vs tris(bipyridine) 混淆
    if 'tris(bipyridine)' in content.lower() or 'tris-bipyridine' in content.lower():
        if '三联吡啶' in content and 'terpyridine' not in content.lower():
            issues.append(('HIGH', 'tris(bipyridine) 被翻译成「三联吡啶」(terpyridine)，应为「三(联吡啶)」'))

    # 3. 检查 "首次/首个/first" 优先权声明
    priority_claims = re.findall(r'(首次|首个|第一次|第一个|first|首先报道|首先合成|首先实现)', content)
    if len(priority_claims) > 3:
        issues.append(('MEDIUM', f'过多优先权声明 ({len(priority_claims)} 处)，需逐一验证'))

    # 4. 检查分子量数值是否合理
    mw_matches = re.findall(r'(\d[\d,]*)\s*(?:Da|g/mol|g·mol)', content)
    for mw_str in mw_matches:
        mw = int(mw_str.replace(',', ''))
        if mw > 200000:
            issues.append(('MEDIUM', f'分子量异常大: {mw_str} Da，请核实'))
        elif mw < 100:
            issues.append(('MEDIUM', f'分子量异常小: {mw_str} Da，请核实'))

    # 5. 检查尺寸数值是否合理
    size_matches = re.findall(r'(\d+\.?\d*)\s*nm', content)
    for size_str in size_matches:
        size = float(size_str)
        if size > 100:
            issues.append(('MEDIUM', f'尺寸异常大: {size_str} nm，请核实'))

    # 6. 检查产率数值
    yield_matches = re.findall(r'(\d+\.?\d*)%\s*(?:产率|yield|产量)', content, re.IGNORECASE)
    for y_str in yield_matches:
        y = float(y_str)
        if y > 100:
            issues.append(('HIGH', f'产率超过100%: {y_str}%'))

    # 7. DOI 格式检查
    doi_match = re.search(r'DOI\s*\|\s*(.*?)(?:\s*\||\s*$)', content, re.MULTILINE)
    if doi_match:
        doi = doi_match.group(1).strip()
        if doi and not re.match(r'10\.\d{4,}/', doi):
            issues.append(('MEDIUM', f'DOI 格式可疑: {doi[:50]}'))

    # 8. 年份一致性：文件名中的年份 vs 提取的年份
    fname_year = re.search(r'Vol\d+_-_(\d{4})', fname) or re.search(r'-_(\d{4})_-', fname)
    content_year = re.search(r'年份\s*\|\s*(\d{4})', content)
    if fname_year and content_year:
        fy = fname_year.group(1)
        cy = content_year.group(1)
        if abs(int(fy) - int(cy)) > 1:
            issues.append(('HIGH', f'年份严重不匹配：文件名 {fy}，提取 {cy}'))

    # 9. 检查「研究结果」等 section 名漂移
    if '### 研究结果' in content and '### 关键结果' not in content:
        issues.append(('LOW', 'section 名漂移：「研究结果」应为「关键结果」'))
    if '### 研究亮点' in content and '### 关键结果' not in content:
        issues.append(('LOW', 'section 名漂移：有「研究亮点」但无「关键结果」'))

    return issues


def main():
    all_issues = {}
    high_count = 0
    medium_count = 0
    low_count = 0

    try:
        from schema import list_paper_mds
        paper_files = list_paper_mds()
    except ImportError:
        paper_files = [os.path.join(OUTPUT_DIR, f) for f in sorted(os.listdir(OUTPUT_DIR))
                       if f.endswith('.md') and f not in ('quality_report.md',)]

    for filepath in paper_files:
        fname = os.path.basename(filepath)
        issues = audit_file(filepath)
        if issues:
            all_issues[fname] = issues
            for level, _ in issues:
                if level == 'HIGH':
                    high_count += 1
                elif level == 'MEDIUM':
                    medium_count += 1
                else:
                    low_count += 1

    print(f"=== 事实审计报告 ===")
    print(f"扫描: 84 个文件")
    print(f"HIGH: {high_count} | MEDIUM: {medium_count} | LOW: {low_count}")
    print()

    if high_count > 0:
        print("=== HIGH 级别问题（必须修正）===")
        for fname, issues in all_issues.items():
            highs = [(l, d) for l, d in issues if l == 'HIGH']
            if highs:
                print(f"\n  {fname[:70]}")
                for _, desc in highs:
                    print(f"    !! {desc}")

    if medium_count > 0:
        print("\n=== MEDIUM 级别问题（建议核实）===")
        for fname, issues in all_issues.items():
            mediums = [(l, d) for l, d in issues if l == 'MEDIUM']
            if mediums:
                print(f"\n  {fname[:70]}")
                for _, desc in mediums:
                    print(f"    ? {desc}")

    # 输出需要人工/Agent核实的文件清单
    files_to_verify = [f for f, issues in all_issues.items()
                       if any(l in ('HIGH', 'MEDIUM') for l, _ in issues)]
    print(f"\n=== 需要核实的文件: {len(files_to_verify)} 篇 ===")
    for f in files_to_verify:
        print(f"  - {f[:70]}")


if __name__ == '__main__':
    main()
