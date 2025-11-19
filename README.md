# SummerCode

<div align="center">

**一个基于 LangChain 和 Textual 的智能代码助手**

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-1.0+-green.svg)](https://python.langchain.com/)
[![Textual](https://img.shields.io/badge/Textual-6.6+-purple.svg)](https://textual.textualize.io/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

</div>

## 📖 项目简介

SummerCode 是一个功能强大的 AI 编码助手，它结合了：
- 🤖 **LangChain Agent** - 智能代理系统，能够理解和执行复杂的编程任务
- 🎨 **Textual UI** - 现代化的终端用户界面，支持鼠标操作
- 🛠️ **丰富的工具集** - 9 个专业工具用于文件操作、代码搜索和命令执行

### ✨ 主要功能

- **文件系统操作**
  - 📂 列出目录内容 (ListDirectoryTool)
  - 🌳 显示目录树结构 (TreeTool)
  - 📄 查看文件内容 (ViewFileTool)
  - ✍️ 创建新文件 (CreateFileTool)
  - ➕ 插入内容到指定行 (InsertContentTool)
  - 🔄 字符串替换 (StrReplaceTool)

- **代码搜索与管理**
  - 🔍 在文件中搜索模式 (GrepTool)
  - 📝 管理 TODO 列表 (TodoWriteTool)

- **命令执行**
  - ⚡ 执行 Bash 命令 (BashTool)

- **交互式界面**
  - 🖱️ 支持鼠标操作
  - 🎨 美观的富文本显示
  - ⚡ 实时反馈 Agent 的思考过程

## 🚀 快速开始

### 前置要求

- **Python**: 3.14 或更高版本
- **uv**: Python 包管理工具 ([安装指南](https://github.com/astral-sh/uv))

### 安装步骤

#### 1. 克隆项目

```bash
git clone <your-repo-url>
cd SummerCode
```

#### 2. 安装 uv (如果尚未安装)

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3. 设置环境变量

创建 `.env` 文件或设置环境变量 `ARK_API_KEY`：
注意，这里仅支持火山引擎模型的API_KEY

**Windows (PowerShell):**
```powershell
$env:ARK_API_KEY="your-api-key-here"
```

**macOS/Linux:**
```bash
export ARK_API_KEY="your-api-key-here"
```

> **注意**: 本项目默认使用火山引擎的 ARK API。如果您想使用其他 LLM 提供商，请修改 `src/summercode/models/chat_model.py`。

#### 4. 安装依赖

```bash
uv sync
```

这将自动安装所有依赖项：
- langchain[openai] >= 1.0.8
- langchain-openai
- langgraph >= 1.0.3
- textual >= 6.6.0
- rich >= 14.2.0
- pydantic >= 2.12.4
- httpx[socks] >= 0.28.1
- jinja2 >= 3.1.6
- langchain-mcp-adapters >= 0.1.13
- pexpect >= 4.9.0

## 📦 项目结构

```
SummerCode/
├── src/
│   └── summercode/
│       ├── agents/           # Agent 定义
│       │   └── coding_agent.py
│       ├── models/           # LLM 模型配置
│       │   └── chat_model.py
│       ├── tools/            # 工具集合
│       │   ├── ls_tool.py
│       │   ├── tree_tool.py
│       │   ├── grep_tool.py
│       │   ├── view_file_tool.py
│       │   ├── create_file_tool.py
│       │   ├── insert_content_tool.py
│       │   ├── str_replace_tool.py
│       │   ├── todo_write_tool.py
│       │   └── bash_tool.py
│       └── ui/               # Textual 用户界面
│           ├── app.py
│           └── callbacks.py
├── test_tools.py             # 工具测试脚本
├── TEST_REPORT.md            # 测试报告
├── pyproject.toml            # 项目配置
└── README.md                 # 项目文档
```

## 🎮 使用方法

### 启动 Console UI

```bash
cd src/summercode
uv run python ui/app.py
```

或者从项目根目录：

```bash
uv run python src/summercode/ui/app.py
```

### 使用界面

1. **启动应用**后，您将看到一个终端界面，包含：
   - 📋 顶部的标题栏
   - 💬 中间的聊天日志区域（显示对话历史）
   - ⌨️ 底部的输入框

2. **输入指令**，例如：
   ```
   列出当前目录的文件
   ```
   ```
   在 src 目录中搜索包含 "def" 的 Python 文件
   ```
   ```
   创建一个名为 hello.py 的文件，内容是 "print('Hello World')"
   ```

3. **观察 Agent 工作**:
   - 🤔 看到 Agent 的思考过程
   - 🔧 查看它使用了哪些工具
   - ✅ 获得最终结果

4. **退出应用**: 按 `Q` 键

### 运行工具测试

验证所有工具是否正常工作：

```bash
uv run python test_tools.py
```

## 🛠️ 配置

### 更改 LLM 模型

编辑 `src/summercode/models/chat_model.py`:

```python
def init_chat_model():
    return ChatOpenAI(
        base_url="https://your-llm-provider.com/api/v3",  # 修改为您的 API 端点
        api_key=os.environ.get("YOUR_API_KEY"),           # 修改为您的 API Key
        model="your-model-name",                          # 修改为您的模型名称
        temperature=0,
        max_tokens=8 * 1024,
    )
```

### 自定义工具

在 `src/summercode/tools/` 目录下创建新工具：

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class YourToolInput(BaseModel):
    param: str = Field(..., description="参数描述")

class YourTool(BaseTool):
    name: str = "your_tool"
    description: str = "工具描述"
    args_schema: Type[BaseModel] = YourToolInput

    def _run(self, param: str, run_manager=None) -> str:
        # 实现您的工具逻辑
        return "结果"
```

然后在 `coding_agent.py` 中添加您的工具。

## 📊 工具详情

查看 [TEST_REPORT.md](./TEST_REPORT.md) 了解每个工具的详细参数和使用方法。

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📄 许可证

本项目采用 **GNU Affero General Public License v3.0 (AGPL-3.0)** 许可证。

详细信息请参阅 [LICENSE](./LICENSE) 文件。

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## 🙏 致谢

- [LangChain](https://python.langchain.com/) - 强大的 LLM 应用框架
- [Textual](https://textual.textualize.io/) - 现代化的 TUI 框架
- [火山引擎 ARK](https://www.volcengine.com/product/ark) - LLM API 提供商

## 📞 联系方式

有问题或建议？请[提交 Issue](your-repo-issues-url)

---

<div align="center">
Made with ❤️ by SummerCode Duoru Chen
</div>
