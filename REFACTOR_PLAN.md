# AutoPaperExtract 重构计划

## Phase 0：原地加固 ✅ 已完成 (2026-04-07)
- schema.py 统一定义
- normalize_md.py 归一化 + 综述标记
- start.sh 并发锁 + 正确收尾顺序 + HIGH>0 触发修复
- review_program.md 反抄袭规则

## Phase 1：目录分离 + SQLite 状态机
- 创建 inputs/ artifacts/ exports/ state/ 目录结构
- manifest.sqlite 状态管理（queued/in_progress/extracted/validated/failed）
- 统一所有脚本使用 schema.py
- discover.py 可复现（sorted DOI 列表）

## Phase 2：结构化 JSON 数据层
- paper.json 作为核心数据格式
- render_md.py 从 JSON 渲染 MD（格式保证100%一致）
- rebuild_csv.py 从 JSON 导出（不再用正则）
- Agent 直接输出 JSON

## Phase 3：综述引用系统 + 分批处理
- cite.py 引用管理（{@cite-key} 替代 [编号]）
- 分批处理（10篇/批 + 60秒冷却）
- retry.py 失败重试管理
- review_audit.py 综述反抄袭审计

详细计划见 planner agent 的输出。
