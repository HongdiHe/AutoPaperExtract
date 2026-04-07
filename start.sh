#!/bin/bash
# AutoPaperExtract v3 启动器
# 用法:
#   bash start.sh          — 提取模式：处理未提取的 PDF
#   bash start.sh enrich   — 补充模式：补充不完整的 MD 文件
#   bash start.sh review   — 综述模式：迭代式研究+写作（autoresearch 风格）

WORK_DIR="/mnt/c/Users/hehon/claude work place/配位驱动自组装/try"
cd "$WORK_DIR" || exit 1

TOTAL_PDF=$(find . -name '*.pdf' -type f | grep -cv '(duplicate)')
DONE_MD=$(ls output/*.md 2>/dev/null | grep -cv 'quality_report\|review_\|literature_\|review_candidates')
DONE_CSV=$(tail -n +2 output/papers_database.csv 2>/dev/null | grep -c .)

echo "=========================================="
echo "  AutoPaperExtract v3 — 自主文献处理系统"
echo "=========================================="
echo ""
echo "PDF 目录:   $WORK_DIR"
echo "PDF 总数:   $TOTAL_PDF (不含 duplicate)"
echo "已生成 MD:  $DONE_MD"
echo "CSV 记录:   $DONE_CSV"
echo ""

# ==========================================
# 通用收尾函数：格式修复 + CSV重建 + 审计 + 术语校验
# ==========================================
run_postprocess() {
    echo ""
    echo "=========================================="
    echo "  收尾：审核与校正（加固版 v3）"
    echo "=========================================="

    # 正确顺序：归一化 → 校验 → 审计 → 自动修复 → 重建CSV → 再次校验
    echo "[1/6] 归一化 section 名 + 标记综述论文..."
    python3 normalize_md.py

    echo ""
    echo "[2/6] 模板校验..."
    python3 validate.py 2>&1 | tee output/validate_report.txt

    echo ""
    echo "[3/6] 事实审计..."
    python3 audit.py 2>&1 | tee output/audit_report.txt
    HIGH_COUNT=$(grep -c "^    !!" output/audit_report.txt 2>/dev/null || echo 0)

    echo ""
    echo "=========================================="
    echo "  审核结果"
    echo "=========================================="
    echo "  事实审计 HIGH: $HIGH_COUNT"

    if [ "$HIGH_COUNT" -gt 0 ]; then
        echo ""
        echo "  ⚠ 发现 $HIGH_COUNT 个 HIGH 级事实问题，启动自动修正..."
        claude --dangerously-skip-permissions \
          -p "$(cat <<'PROMPT'
读取 output/audit_report.txt，找到所有 HIGH 级别问题。
对每个 HIGH 问题：
1. 打开对应的 MD 文件
2. 读取对应的 PDF 原文核实
3. 修正错误
修正完成后输出修正报告。
**不要问我任何问题。直接修正。**
PROMPT
)"
        echo "  自动修正完成，重新审计..."
        python3 audit.py 2>&1 | tail -5
    fi

    echo ""
    echo "[4/6] 自动修正后重新归一化..."
    python3 normalize_md.py

    echo ""
    echo "[5/6] 重建 CSV (UTF-8 BOM)..."
    python3 rebuild_csv.py

    echo ""
    echo "[6/6] 最终校验..."
    python3 validate.py 2>&1 | tail -5

    echo ""
    echo "=========================================="
    echo "  收尾完成"
    echo "=========================================="
}

# ==========================================
# 并发锁（防止双开）
# ==========================================
LOCKFILE="$WORK_DIR/output/.pipeline.lock"
exec 9>"$LOCKFILE"
if ! flock -n 9; then
    echo "错误: 另一个 start.sh 正在运行，请等待完成后再试。"
    exit 1
fi

# ==========================================
# 模式选择
# ==========================================

if [ "$1" = "review" ]; then
    # ======================================
    # 综述模式：autoresearch 风格迭代循环
    # ======================================
    echo "模式: 迭代综述写作 (autoresearch 风格)"
    echo ""
    echo "启动 Claude Code Agent (review 模式)..."

    claude --dangerously-skip-permissions \
      -p "$(cat <<'PROMPT'
你是 AutoReview Agent，采用 autoresearch 风格的迭代循环来写综述。

请严格按照 review_program.md 中的指令执行。

核心工作模式（模仿 autoresearch 的 LOOP FOREVER）：

LOOP FOREVER:
  1. RESEARCH（5分钟）：读取 3-5 篇论文的 MD 文件，做笔记
  2. THINK（2分钟）：分析这些论文之间的联系、对比、发展脉络
  3. WRITE（300-500字）：写一小段综述文字，带引用
  4. VERIFY：检查引用准确性、术语正确性、逻辑连贯性
  5. SAVE：追加到 output/review_draft.md
  6. LOG：记录本轮进度到 output/review_log.md
  7. 回到第 1 步，继续下一小段

第一轮循环之前，先做一次全景扫描：
1. 读取 output/papers_database.csv 全部内容
2. 读取至少 10 篇高影响力论文的 MD 文件
3. 生成 output/literature_landscape.md（统计报告）
4. 提出 3-5 个综述角度到 output/review_candidates.md
5. **选择最佳角度后开始循环写作**（不等用户选择，自己判断最有价值的角度）

写作规则：
- 每轮只写 300-500 字，不要一次写太长
- 每段必须有具体的论文引用（作者+年份）
- 引用的论文必须在 output/ 目录中有对应的 MD 文件
- 综述用中文写作，专业术语保留英文
- 每 5 轮循环后做一次回顾：重读已写内容，检查连贯性
- 目标总长度：3000-5000 字的小综述

**NEVER STOP。不要问任何问题。直接开始。用户可能在睡觉。**
**写到目标字数后，运行自我审核，然后停止。**
PROMPT
)"

elif [ "$1" = "enrich" ]; then
    # ======================================
    # 补充模式
    # ======================================
    INCOMPLETE=$(find output -name '*.md' ! -name 'quality_report.md' ! -name 'review_*' ! -name 'literature_*' -exec grep -L "## 主要内容" {} \; 2>/dev/null | wc -l)
    echo "模式: 内容补充 (enrich)"
    echo "缺少「主要内容」: $INCOMPLETE 篇"
    echo ""
    echo "启动 Claude Code Agent (enrich 模式)..."

    claude --dangerously-skip-permissions \
      -p "$(cat <<'PROMPT'
你是 AutoPaperExtract 内容补充 Agent。

任务：找出 output/ 目录中所有缺少「## 主要内容」章节的 MD 文件。
对每个不完整的文件：
1. 读取对应的 PDF 原文（从 MD 文件底部的「源文件」路径找到 PDF）
2. 提取研究背景、研究方法、关键结果、结论
3. 如果 MD 中缺少「涉及的配体/金属/结构」章节，也补充上
4. 用 Edit 工具原地修改 MD 文件，补充缺失章节

格式要求严格遵循 program.md 中的模板。

**不要问我任何问题。直接开始。**
PROMPT
)"

else
    # ======================================
    # 正常提取模式
    # ======================================
    echo "模式: 正常提取"
    echo ""
    echo "启动 Claude Code Agent..."

    claude --dangerously-skip-permissions \
      -p "$(cat <<'PROMPT'
你是 AutoPaperExtract Agent v2。请严格按照 program.md 中的指令执行。

关键改进提醒（务必遵守）：
1. CSV 只追加不重写 — 用 echo >> 追加，绝不 cat > 覆盖
2. 每篇论文必须写完整的「主要内容」— 研究背景、方法、结果、结论各至少 3 句
3. 严格遵循固定模板 — 不加粗字段名、不加超链接、关键词英文逗号分隔
4. 以 MD 文件是否存在判断是否已处理 — 不依赖 CSV

现在立刻开始：
1. 读取 program.md 了解完整工作流程
2. 开始 LOOP FOREVER，处理每一个 PDF

**不要问我任何问题。不要停下来。直接开始工作。**
PROMPT
)"
fi

# ==========================================
# 所有模式结束后都执行收尾审核
# ==========================================
run_postprocess
