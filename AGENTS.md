# AGENTS.md

本仓库用于撰写 MPhil 毕业论文，初步题目为：

`Multimodal Sensing-Assisted User Association and Tracking in Vehicular Networks`

本论文将随着实验和算法设计推进而持续调整。后续协作时，应始终区分
“研究事实”“论文大纲”和“正式 LaTeX 正文”。研究事实和内部待确认事项放在
`docs/work_brief.md` 中维护；正式 LaTeX 正文应保持可供审稿的写法，不暴露
TODO、未完成状态或内部规划口吻。

## 核心工作流程

本仓库固定维护两个中文 Markdown 文档作为写作控制层：

1. `docs/work_brief.md`
   - 这是当前研究工作的事实源。
   - 用于记录论文背景、研究问题、当前贡献表述、系统模型、算法框架、实验计划、
     当前证据和内部待确认事项。
   - 当用户报告新的实验结果、算法修改或研究思路变化时，除非用户另有说明，
     应优先更新此文档。

2. `docs/thesis_outline.md`
   - 这是论文写作蓝图，由 `docs/work_brief.md` 推导和更新。
   - 用于记录毕业论文的 chapter / section / subsection 结构、每部分写作要点、
     叙述逻辑和实验结果空缺。
   - 大纲应呈现当前采用的确定方案，不再使用 `不稳定`、`缺证据` 等会污染正文
     写作的状态标签。方法不确定性应回写到 `docs/work_brief.md`。
   - 在 `docs/work_brief.md` 出现重要变化后，应同步检查并更新此文档。

之后再依据 `docs/thesis_outline.md` 将正式论文内容写入 `chapters/*.tex`。

## 对应 Skills

本项目已创建两个本地 Codex skills，位置在 `C:\Users\user\.codex\skills`：

1. `$brief-to-outline`
   - 用于根据 `docs/work_brief.md` 更新 `docs/thesis_outline.md`。
   - 适用于研究背景、问题定义、贡献、系统模型、算法流程或实验状态发生变化后，
     需要同步论文大纲的场景。
   - 要求不虚构贡献，不把未验证结果写成定量结论；方法空缺应记录到
     `docs/work_brief.md`，outline 只呈现当前采用的确定方案。

2. `$outline-to-thesis-writing`
   - 用于根据 `docs/thesis_outline.md` 撰写或修改 `chapters/*.tex`。
   - 适用于将大纲中的 chapter / section 写成正式英文 LaTeX 正文的场景。
   - 要求保持学术语气、逻辑连贯、符号一致；不得在正文中保留 TODO、
     未完成口吻、内部待办或代码库讲解式描述。

推荐节奏：

```text
用户更新研究进展
-> 更新 docs/work_brief.md
-> 同步更新 docs/thesis_outline.md
-> 根据大纲撰写或修改 chapters/*.tex
-> 编译检查
-> Git 提交并同步到 GitHub / Overleaf
```

## 语言要求

- `docs/work_brief.md` 和 `docs/thesis_outline.md` 使用中文维护。
- `AGENTS.md` 使用中文维护，便于后续协作规则清晰一致。
- `chapters/*.tex` 中的正式论文正文应使用正式学术英语撰写。
- LaTeX 正文不得包含 TODO 标记或中文内部备注。需要保留的待办事项应写入
  `docs/work_brief.md`。

## 论文写作质量要求

- 不得虚构实验结果、baseline、数值、引用或算法细节。
- 如果实验结果不足，正文应只描述实验协议、指标和评价对象，不写定量结论。
- 如果方法细节尚未稳定，应先更新 `docs/work_brief.md` 形成当前采用方案，再写正文。
- 论文中的 claim 必须与 `docs/work_brief.md` 中记录的证据相匹配。
- 正文不得出现 “not yet fixed”、“to be finalized”、“current stage”、“planned
  implementation”、“experimental results are not yet available” 等暴露未完成状态的表述。
- 仿真系统应按学术方法描述，不应写成 repository、codebase、script 或工程实现说明。
- 写作风格应正式、克制、清晰，避免宣传式或过度夸大的表达。
- 保持术语一致，尤其是 multimodal sensing、user association、tracking、
  vehicular networks、RSU、vehicle、user、base station 等概念。
- 保持符号一致。如果系统模型中的符号发生变化，应同步更新
  `docs/work_brief.md` 和相关 LaTeX 章节。
- 除非研究事实或大纲发生实质变化，不应进行大范围重写。

## 仓库结构

- `mythesis.tex`：主 LaTeX 入口文件。
- `chapters/`：正式论文正文、前置部分和附录。
- `docs/work_brief.md`：研究事实源。
- `docs/thesis_outline.md`：论文写作蓝图。
- `figures/`：论文图片。
- `tables/`：论文表格或表格生成源文件。
- `mythesis.bib`：论文参考文献。
- `mythesis_LoP.bib`：List of Publications 使用的参考文献。

## LaTeX 写作实践

- 每个 chapter 单独放在 `chapters/` 下的一个 `.tex` 文件中。
- 使用稳定的 label，例如 `\label{ch:introduction}` 和
  `\label{sec:system-model}`。
- 优先使用语义化 LaTeX 结构，例如 `\chapter`、`\section`、
  `\subsection`，避免手动格式控制。
- 编辑 `.tex`、`.bib` 或 class 相关文件后，如本地工具链可用，应进行编译检查。
- 不要提交 LaTeX 编译中间文件，例如 `.aux`、`.bbl`、`.bcf`、`.log`、
  `.out`、`.toc`、`.xdv` 等，除非用户明确要求。

## 与 Overleaf 同步

- 文件被 `mythesis.tex` 引用后，应尽量保持文件名稳定。
- 新建源文件时避免使用空格。
- 每次提交应保持主题清晰，方便 GitHub 与 Overleaf 同步后检查差异。
