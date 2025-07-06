# 问题自动生成器

这是一个基于大语言模型（DeepSeek）构建的“问题自动生成器”项目。用户只需输入任意一段文本，即可自动生成带有选项、答案与解析的标准客观题。

---

## 🌟 功能简介

- 输入一段文本（中文或韩文皆可）
- 自动生成包含四个选项的选择题
- 返回正确答案与简要解释
- 支持设置题目难度（简单 / 中等 / 困难）
- 提供 CLI 命令行接口与 Web UI 界面（基于 Streamlit）

---

## 🛠️ 技术栈

| 模块            | 技术/库         |
|----------------|----------------|
| 编程语言        | Python 3.10+   |
| 前端界面        | Streamlit      |
| 语言模型调用     | OpenAI API / DeepSeek API |
| 环境变量管理     | python-dotenv  |
| JSON验证        | jsonschema     |

---

## 📦 安装与部署

### 1. 克隆仓库

```bash
git clone https://github.com/gyeongseo05/question-generator.git
cd question-generator

### 2. 安装依赖

pip install -r requirements.txt

### 3. 配置 API 密钥

创建 .env 文件，并填写以下内容（选择你所使用的模型）：
DEEPSEEK_API_KEY=你的DeepSeek密钥

### 4. 运行项目

运行 Web 应用：
streamlit run app.py

使用命令行生成问题：
python cli.py

---

## 📁 项目结构

├── app.py                   # Streamlit 界面入口
├── cli.py                   # 命令行入口
├── question_generator.py    # 生成问题的核心逻辑
├── validator.py             # JSON格式验证
├── .env                     # API 密钥配置（不应上传）
├── requirements.txt         # 所需依赖

---

## 📺 演示视频

见报告附件中的 演示视频.mp4

---

## 📌 注意事项

请勿上传 .env 文件至 GitHub 公共仓库

若使用 OpenAI，请确保你账户已充值并可调用 GPT-3.5

若使用 DeepSeek，请确保你拥有有效的访问权限和 token
