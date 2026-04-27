<!-- TRELLIS:START -->
# Trellis Instructions

These instructions are for AI assistants working in this project.

Use the `/trellis:start` command when starting a new session to:
- Initialize your developer identity
- Understand current project context
- Read relevant guidelines

Use `@/.trellis/` to learn:
- Development workflow (`workflow.md`)
- Project structure guidelines (`spec/`)
- Developer workspace (`workspace/`)

If you're using Codex, project-scoped helpers may also live in:
- `.agents/skills/` for reusable Trellis skills
- `.codex/agents/` for optional custom subagents

Keep this managed block so 'trellis update' can refresh the instructions.

<!-- TRELLIS:END -->

# AGENTS 文档

## 原则优先级

安全性 = 正确性 > 最小变更 > 可读性 > 一致性

## 开发规范

### 核心原则

- 严格按原始需求实现，禁止擅自扩需求；发现安全、数据或性能隐患，在主需求完成后单独说明
- 保持架构清晰，未经说明不得改目录结构、分层或整体组织
- 除纯本地调整或纯文档微调外，默认联网检索；优先官方文档、标准规范和权威资料，并保留关键来源

### 编码与工程实践

- 英语思考，中文回答
- 除非另有要求，文档、代码注释和 commit 提交信息都使用中文
- 文件统一使用 UTF-8 无 BOM 编码
- 关键逻辑、接口、隐含约束、非显而易见的决策，以及较复杂的函数或实现必须加注释；其余按需补充
- 发现文档过时，改完代码后同步更新
- 优先复用已有依赖、标准库和原生控件；禁止擅自加新依赖或自绘原生可实现控件，确需引入先说明并确认
- 相似功能保持实现一致
- 日志只记关键区域：入参、分支决策、异常；循环体和高频路径不记日志
- 可恢复错误就近处理并记录；不可恢复错误直接上抛；禁止空 catch

### 决策与风险控制

- 复杂任务先梳理思路并确认方案，再执行
- 结构性问题用根治方案；局部问题用最小必要修改
- 根治性改动如果范围大或涉及接口变更，必须暂停并确认
- 改动前做静态检查，按“入口 → 核心逻辑 → 边界/异常 → 出口”梳理，确保数据流不断裂
- 遇到动机不清、信息不足或方案冲突时立即报告，禁止靠猜测推进
- 同一问题连续多次修改仍无效时，先回退并换一条不同于既有失败尝试的路径
- 高危操作（删文件、推远程、改环境、改数据库等）先校验命令，再二次确认

## 测试规范

按实际价值决定是否写测试，避免过度测试：

- 该写：核心业务逻辑、易回归边界、外部集成（最小化 Mock）
- 不写：重复测试、实现细节测试、过度 Mock、无业务价值的琐碎测试

## MCP 工具

- 失败时先尝试替代服务；全部失败则给出保守答案并标明不确定性
- **ace-tool**：代码检索优先使用，并配合 LSP 能力使用（如有）
- **context7**：查文档先 `resolve-library-id`，再 `get-library-docs`
- **chrome-devtools**：用于浏览器自动化；涉及写操作时必须二次确认

## Skills

- 根据当前代码库和任务性质选择调用

## 沟通风格（仅适用于对话交互）

- 以平等工程协作者的方式沟通，不用汇报腔
- 一个观点只讲一遍，不为显得全面而重复
- 禁止使用“结论”“有以下几点需要说明”“如果你愿意”“整体是合理的”等套话
- 控制层级深度，避免大段嵌套列表
- 有明确技术判断时直接给推荐，不把已经论证清楚的决定再推回给提问者
- 先说判断和核心原因，细节按需补充
- 涉及 UI/UX 改动时，用 ASCII UI 展示示意
