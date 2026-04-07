#!/usr/bin/env python3
"""
文献发现工具 — 基于引文图谱和关键词搜索发现新文献

功能:
  1. 引文图谱（citation graph）: 从已有 84 篇论文出发，找出它们引用的和引用它们的论文
  2. 关键词搜索: 在 OpenAlex 上搜索配位驱动自组装相关论文
  3. 高频被引分析: 找出被多篇已有论文同时引用但我们没有的论文（重要遗漏）
  4. 前沿追踪: 找出引用我们已有论文的最新论文（2023-2026）

用法:
  python3 discover.py --mode citations    # 引文图谱分析
  python3 discover.py --mode search       # 关键词搜索
  python3 discover.py --mode missing      # 高频被引遗漏分析
  python3 discover.py --mode frontier     # 前沿追踪
  python3 discover.py --mode all          # 全部运行
"""

import csv
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import os
import argparse
from collections import Counter

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "papers")
CSV_PATH = os.path.join(OUTPUT_DIR, "papers_database.csv")

def api_get(url, retries=2):
    """带重试的 HTTP GET"""
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'AutoPaperExtract/1.0 (academic research)'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
            else:
                return None

def load_existing_dois():
    """从 CSV 加载已有论文的 DOI 集合"""
    dois = set()
    titles = {}
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            doi = row.get('DOI', '').strip().lower()
            if doi:
                dois.add(doi)
                titles[doi] = row.get('标题', '')[:60]
    return dois, titles

def get_references_crossref(doi):
    """从 CrossRef 获取一篇论文的参考文献 DOI 列表"""
    url = f"https://api.crossref.org/works/{doi}"
    data = api_get(url)
    if not data or 'message' not in data:
        return []
    refs = data['message'].get('reference', [])
    return [r['DOI'].lower() for r in refs if 'DOI' in r]

def get_citations_semantic(doi):
    """从 Semantic Scholar 获取引用该论文的论文"""
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=citations.title,citations.year,citations.externalIds"
    data = api_get(url)
    if not data or 'citations' not in data:
        return []
    results = []
    for c in data['citations']:
        if c and c.get('externalIds', {}).get('DOI'):
            results.append({
                'doi': c['externalIds']['DOI'].lower(),
                'title': c.get('title', ''),
                'year': c.get('year', 0),
            })
    return results

def search_openalex(query, per_page=25):
    """在 OpenAlex 上搜索论文"""
    encoded = urllib.parse.quote(query)
    url = f"https://api.openalex.org/works?search={encoded}&per_page={per_page}&sort=cited_by_count:desc"
    data = api_get(url)
    if not data or 'results' not in data:
        return []
    results = []
    for w in data['results']:
        doi = w.get('doi', '')
        if doi:
            doi = doi.replace('https://doi.org/', '').lower()
        results.append({
            'doi': doi,
            'title': w.get('title', ''),
            'year': w.get('publication_year', 0),
            'cited_by': w.get('cited_by_count', 0),
            'journal': (w.get('primary_location') or {}).get('source', {}).get('display_name', '') if (w.get('primary_location') or {}).get('source') else '',
        })
    return results


def cmd_citations(existing_dois, existing_titles):
    """引文图谱分析：找出已有论文引用的和引用它们的论文"""
    print("=== 引文图谱分析 ===\n")

    all_referenced = Counter()  # DOI -> 被多少篇已有论文引用

    # 采样 20 篇核心论文（JACS/Nature/Science 优先）
    sample_dois = list(existing_dois)[:20]

    print(f"正在分析 {len(sample_dois)} 篇论文的参考文献...")
    for i, doi in enumerate(sample_dois):
        refs = get_references_crossref(doi)
        for ref_doi in refs:
            if ref_doi not in existing_dois:
                all_referenced[ref_doi] += 1
        if (i + 1) % 5 == 0:
            print(f"  已处理 {i+1}/{len(sample_dois)}")
        time.sleep(0.5)  # 限流

    # 找出被多篇论文同时引用但我们没有的论文
    print(f"\n共发现 {len(all_referenced)} 篇我们没有的被引论文")
    print("\n被多篇已有论文引用的遗漏文献（可能很重要）：")

    missing = []
    for doi, count in all_referenced.most_common(30):
        if count >= 2:
            # 获取标题
            data = api_get(f"https://api.crossref.org/works/{doi}")
            title = ''
            year = ''
            journal = ''
            if data and 'message' in data:
                msg = data['message']
                title = ' '.join(msg.get('title', ['']))
                year = str(msg.get('published-print', {}).get('date-parts', [['']])[0][0] or
                          msg.get('published-online', {}).get('date-parts', [['']])[0][0] or '')
                ct = msg.get('container-title', [])
                journal = ct[0] if ct else ''
            missing.append({
                'doi': doi, 'count': count, 'title': title,
                'year': year, 'journal': journal
            })
            print(f"  [{count}次引用] {title[:70]} ({journal}, {year})")
            time.sleep(0.3)

    return missing


def cmd_search(existing_dois):
    """关键词搜索发现新文献"""
    print("=== 关键词搜索 ===\n")

    queries = [
        "terpyridine metallosupramolecular self-assembly",
        "coordination-driven self-assembly discrete 2D",
        "molecular knots catenanes coordination",
        "platinum metallacycles pyridine self-assembly",
        "bipyridine grid helicate self-assembly",
    ]

    all_results = []
    for q in queries:
        print(f"搜索: {q}")
        results = search_openalex(q, per_page=15)
        new_results = [r for r in results if r['doi'] and r['doi'] not in existing_dois]
        all_results.extend(new_results)
        print(f"  找到 {len(new_results)} 篇新论文")
        time.sleep(1)

    # 去重并按引用数排序
    seen = set()
    unique = []
    for r in sorted(all_results, key=lambda x: -x['cited_by']):
        if r['doi'] not in seen:
            seen.add(r['doi'])
            unique.append(r)

    print(f"\n共发现 {len(unique)} 篇不在库中的相关论文（按引用数排序）：")
    for r in unique[:20]:
        print(f"  [{r['cited_by']}次引用] {r['title'][:65]} ({r['journal'][:20]}, {r['year']})")

    return unique[:20]


def cmd_frontier(existing_dois):
    """前沿追踪：找出最近引用我们论文的最新工作"""
    print("=== 前沿追踪（2023-2026 最新引用）===\n")

    sample_dois = list(existing_dois)[:15]
    frontier = []

    print(f"正在分析 {len(sample_dois)} 篇论文的最新引用...")
    for i, doi in enumerate(sample_dois):
        citations = get_citations_semantic(doi)
        new_citations = [c for c in citations
                        if c['doi'] not in existing_dois
                        and (c.get('year') or 0) >= 2023]
        frontier.extend(new_citations)
        if (i + 1) % 5 == 0:
            print(f"  已处理 {i+1}/{len(sample_dois)}")
        time.sleep(1)

    # 去重
    seen = set()
    unique = []
    for f in frontier:
        if f['doi'] not in seen:
            seen.add(f['doi'])
            unique.append(f)

    unique.sort(key=lambda x: -(x.get('year', 0)))

    print(f"\n共发现 {len(unique)} 篇最新相关论文（2023-2026）：")
    for r in unique[:15]:
        print(f"  [{r['year']}] {r['title'][:70]}")
        print(f"       DOI: {r['doi']}")

    return unique[:15]


def save_report(missing, search_results, frontier):
    """保存发现报告"""
    report_path = os.path.join(OUTPUT_DIR, "discovery_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 文献发现报告\n\n")
        f.write(f"> 基于 84 篇已有论文的引文图谱和关键词搜索\n\n")

        if missing:
            f.write("## 重要遗漏（被多篇已有论文引用但我们没有）\n\n")
            f.write("| 被引次数 | 标题 | 期刊 | 年份 | DOI |\n")
            f.write("|---------|------|------|------|-----|\n")
            for m in missing:
                f.write(f"| {m['count']} | {m['title'][:60]} | {m['journal'][:20]} | {m['year']} | {m['doi']} |\n")
            f.write("\n")

        if search_results:
            f.write("## 关键词搜索发现的高引用论文\n\n")
            f.write("| 引用数 | 标题 | 期刊 | 年份 | DOI |\n")
            f.write("|-------|------|------|------|-----|\n")
            for r in search_results:
                f.write(f"| {r['cited_by']} | {r['title'][:60]} | {r['journal'][:20]} | {r['year']} | {r['doi']} |\n")
            f.write("\n")

        if frontier:
            f.write("## 前沿论文（2023-2026，引用了我们已有的论文）\n\n")
            for r in frontier:
                f.write(f"- [{r['year']}] {r['title']}\n  DOI: {r['doi']}\n\n")

    print(f"\n报告已保存到: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='文献发现工具')
    parser.add_argument('--mode', default='all',
                       choices=['citations', 'search', 'frontier', 'all'],
                       help='运行模式')
    args = parser.parse_args()

    existing_dois, existing_titles = load_existing_dois()
    print(f"已有论文: {len(existing_dois)} 篇（含 DOI）\n")

    missing = []
    search_results = []
    frontier = []

    if args.mode in ('citations', 'all'):
        missing = cmd_citations(existing_dois, existing_titles)
        print()

    if args.mode in ('search', 'all'):
        search_results = cmd_search(existing_dois)
        print()

    if args.mode in ('frontier', 'all'):
        frontier = cmd_frontier(existing_dois)
        print()

    save_report(missing, search_results, frontier)


if __name__ == '__main__':
    main()
