# AI Paper2Slide Skill
**面向 AI 研究的会议级论文转幻灯片 Skill**

<p align="center">
  <b>将 AI 论文转换为适合顶会汇报的演示文稿，默认输出 PPTX + 英文 DOCX，并严格遵守 LaTeX-only 图像来源约束。</b>
</p>

<p align="center">
  <a href="../README.md"><img src="https://img.shields.io/badge/English-Read%20EN-blue?style=for-the-badge&logo=github&logoColor=white" alt="English"></a>
  <a href="#中文"><img src="https://img.shields.io/badge/中文-阅读%20CN-red?style=for-the-badge&logo=github&logoColor=white" alt="中文"></a>
  <a href="../LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&logo=github&logoColor=white" alt="License: MIT"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> ·
  <a href="#中文">中文</a>
</p>

---

## 中文版 README

## 一句话简介

`ai-paper2slide-skill` 是一个开源 ChatGPT Skill，用于将 AI 与科学研究论文转换为**会议级别的演示文稿套件**。

它面向 **NeurIPS、ICML、ICLR、CVPR、ACL、KDD、WWW、AAAI、SIGIR、EMNLP、ECCV、ICCV、MICCAI** 等顶级会议，强调两条核心原则：

- **幻灯片图片只能来自用户提供的 LaTeX 源文件包**
- **默认交付 PPTX + 英文逐页演讲稿 DOCX**

---

## 快速开始

> [!IMPORTANT]
> 如果你希望生成的幻灯片包含论文中的图表，请先提供完整的 LaTeX 源文件包。

### 推荐输入

1. **原始 LaTeX 源文件包**  
   支持格式：`.zip`、`.tar`、`.tar.gz`

2. **编译后的论文 PDF**  
   用于交叉检查正文、章节顺序和最终版式。

### 默认输出

- `paper2slide_deck.pptx`
- `paper2slide_speaker_script.docx`
- `visual_source_manifest.json`
- `paper2slide_quality_report.md`

---

## 核心能力

### LaTeX-only 图像来源

Skill 会优先解析论文原始 LaTeX 打包文件，并扫描：

- `\includegraphics` 图片路径
- figure / table 环境
- caption
- label
- 图表附近正文描述
- 模型架构图与方法流程图
- 实验结果表格
- 消融实验和定性可视化图

只有在用户提供的 LaTeX 包中解析到的图片资源，才允许进入最终 slide。

### 默认 PPTX + 英文 DOCX 交付

完整 paper-to-slide 请求默认生成：

| 输出文件 | 是否必需 | 说明 |
|---|---:|---|
| `paper2slide_deck.pptx` | 是 | 16:9 PowerPoint 演示文稿 |
| `paper2slide_speaker_script.docx` | 是 | 英文逐页演讲稿，默认总时长约 10 分钟 |
| `visual_source_manifest.json` | 推荐 | LaTeX 源文件中的图表来源记录 |
| `paper2slide_quality_report.md` | 推荐 | 检查 LaTeX-only 图片合规性、图表准确性、slide 可读性和演讲稿时间 |

### 顶会风格的幻灯片设计

生成的 deck 会尽量保持如下特点：

- 16:9 宽屏比例
- 标题更强调结论和观点
- 文字简洁、适合口头汇报
- 图表和结果来自原始 LaTeX 源文件
- 方法叙事清晰
- 结论页突出贡献与影响

### 语言模式

默认演讲稿为**英文**。如果你需要中文或双语版本，也可以额外指定：

| 模式 | 说明 |
|---|---|
| `English` | 默认模式，适合国际 AI 会议 |
| `Chinese` | 适合中文组会、答辩、内部汇报 |
| `Bilingual` | 英文标题 + 中文说明，或中文幻灯片 + 英文术语 |
| `Custom language` | 你自定义的语言模式 |

---

## 示例请求

### 国际会议汇报

```text
Convert this LaTeX paper package into a 10-minute NeurIPS-style presentation.

Please create:
1. A 16:9 PowerPoint slide deck.
2. A Word document with the English per-slide speaking script.
3. A visual source manifest for all architecture figures and experimental result tables.
4. A quality report checking LaTeX-only image compliance, figure/table placement, and script timing.

Only use images that are included in the provided LaTeX package.
```

### 中文组会汇报

```text
请将这篇论文转换为一个 10 分钟中文组会汇报。

请生成：
1. 中文 PPT。
2. 默认英文逐页演讲稿 Word 文档。
3. 可选中文逐页演讲稿 Word 文档。
4. 图表来源 manifest 和质量报告。

Slide 中的所有图片必须只来自我上传的 LaTeX 源文件包。
```

---

## 项目风格

本项目更强调三件事：

1. **来源可信**：所有图像必须可追溯到 LaTeX 源文件包。
2. **默认交付完整**：不是只给提纲，而是给 PPTX 和英文 DOCX。
3. **适合真实汇报**：风格接近 AI 顶会 presentation，而不是普通商务模板。

---

## 代码结构

```text
ai-paper2slide-skill/
├── README.md
├── docs/
│   └── i18n/
│       └── README_ZH.md
├── LICENSE
├── assets/
│   └── README.md
├── references/
│   ├── ai_conference_style_guide.md
│   ├── latex_visual_localization.md
│   ├── quality_checklist.md
│   └── speaker_script_guide.md
└── scripts/
    ├── inspect_latex_assets.py
    └── validate_visual_sources.py
```

---

## 引用

如果这个 Skill 对你的研究汇报工作有帮助，欢迎引用或链接到仓库：

```bibtex
@misc{ai-paper2slide-skill,
  title        = {AI Paper2Slide Skill: Conference-Grade Paper-to-Slide Generation for AI Research},
  author       = {Zhixiang Lu},
  year         = {2026},
  howpublished = {\url{https://github.com/Leo1998-Lu/ai-paper2slide-skill}},
  note         = {Open-source ChatGPT Skill for LaTeX-only, conference-style paper-to-slide generation.}
}
```
