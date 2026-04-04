<div align="center">

# ComfyUI General API Node Pack
*本节点包由 FeiMao-326 创作*

[**English**](README.md) | [**中文**](README_CN.md)

</div>

---

## 🇨🇳 中文

一套为 ComfyUI 设计的、功能强大且用途广泛的实用节点包，旨在简化涉及大语言模型和文本处理的复杂工作流。本节点包由 FeiMao-326 创作。

### ✨ 包含的节点

本节点包包含以下节点，您都可以在 **`FeiMao-326`** 分类下找到它们：

1.  **General API Node**: **[核心]** 强大的多模态 AI 交互引擎。
    -   **2026 模型原生适配**: 完美支持 Gemini 3.1 (Pro/Flash)、GPT-5.4、Llama 4 及 Claude 3.5。
    -   **智能任务路由**: 针对 Google Gemini 实现自动重定向。使用标准模型名（如 `gemini-3.1-pro`,`gemini-3.1-pro-image-preview`）进行对话或读图；当检测到模型名包含 `image-` 关键字时，自动切换为生图模式。
    -   **显存双重清理**: 专为本地 Ollama 打造。勾选 `cleanup_local_gpu` 后，节点会通过 REST API 发送 `keep_alive: 0` 并辅助 CLI 命令强制卸载模型，在运行完毕后瞬间物理腾空 GPU 显存。
    -   **多模态视觉解析**: 支持多达 2 张及以上图像的并发解析与对比。
    -   **高级种子控制**: 包含 `固定`, `递增`, `随机` 等工业级种子逻辑。
2.  **Text Batch Replace**: 一个强大的文本工具，可在单个节点中执行多达8次的查找与替换操作。
3.  **JSON Parser**: 可将复杂的、深度嵌套的JSON结构，解析为多个独立的文本输出，并自带带标签的预览功能。它会深度搜索用户定义的关键字，非常适合处理结构化提示词。
4.  **Show Text**: 直接在节点界面上显示输入的文本。
5.  **Simple Text**: 一个简单的文本输入节点，用于将字符串传递给其他节点。
6.  **Text Split By Delimiter**: 根据分隔符将文本字符串分割为列表。
7.  **Get List Element**: 通过索引从列表中检索特定元素。
8.  **Text Iterator**: 根据分隔符分割文本并作为批次输出，触发下游节点的批次执行。
9.  **Markdown Extractor**: 智能正则表达式提取，专为抓取 LLM 回复中的 ` ```json ` 或代码块设计。
10. **Text Template (Dynamic)**: **[推荐]** 动态插槽模板，支持 `{变量}` 自动生成输入端口，支持中文变量名。
11. **Prompt Cleaner**: 提示词清洗，自动去重、规范逗号、清理空括号。
12. **Text Logic Switch**: 文本逻辑开关，基于内容匹配实现工作流 If-Else 分流。
13. **Regex Extractor Pro**: 高级正则提取，支持捕获组筛选。
14. **Dictionary Translator**: 词典批量映射替换，支持 JSON 或 Key=Value 格式。

### 🔧 安装方法

1.  **克隆仓库**
    -   打开您的终端。
    -   导航到您的 ComfyUI `custom_nodes` 文件夹：
        ```bash
        cd path/to/your/ComfyUI/custom_nodes/
        ```
    -   克隆此仓库：
        ```bash
        git clone https://github.com/FeiMao-326/Comfyui-General-API-Node.git
        ```

2.  **安装依赖**
    -   导航到刚刚克隆下来的节点文件夹：
        ```bash
        cd Comfyui-General-API-Node
        ```
    -   安装所需的依赖项：
        ```bash
        pip install -r requirements.txt
        ```

3.  **重启 ComfyUI**
    -   完成以上步骤后，请完全重启 ComfyUI。

### 💡 如何使用

#### General API Node
1.  **找到节点**: 在 ComfyUI 中，您可以通过右键菜单 -> `Add Node` -> `FeiMao-326` -> `FeiMao-326 General API Node` 找到它。

    ![FeiMao-326 节点界面](./assets/node_interface.png)

2.  **设置种子控制**: 若要启用自动种子变更（例如 `randomize`），请将节点的 `seed` **输出**端口连接回它自身的 `seed` **输入**端口。这个“循环”连接会在每次运行后自动更新种子值。

3.  **使用场景**:
    -   **📝 纯文本生成**: 将 `image_1` 和 `image_2` 保持断开。
    -   **🖼️ 单图描述**: 连接一张图片到 `image_1` 接口。
    -   **🎬 双图视频转场**: 连接**起始帧**到 `image_1`，连接**结束帧**到 `image_2`。
    -   **📸 多图分析**: 您最多可以连接多张图片 (`image_1`, `image_2`, `image_3...等`) 进行复杂的分析任务。
4.  **API 连接示例**:
    -   **NVIDIA NIM (英伟达官方/私有化部署)**:
        -   `api_baseurl`: `https://integrate.api.nvidia.com/v1` (或私有 NIM 地址)
        -   `api_key`: 填入您的 NVIDIA API 密钥 (`nvapi-xxxxxxxx`)
        -   `model`: `meta/llama-4-maverick` 或 `nvidia/nemotron-3-ultra`
    -   **OpenAI GPT-5 (最新版)**:
        -   `api_baseurl`: `https://api.openai.com/v1`
        -   `api_key`: 填入您的 OpenAI 密钥
        -   `model`: `gpt-5.4-thinking` 或 `o3-pro` (旗舰推理模型)
    -   **本地 Ollama**:
        -   `api_baseurl`: `http://127.0.0.1:11434/v1`
        -   `api_key`: `ollama`
        -   `model`: `gemma4:e4b` (当前默认模型，支持图像分析)
        -   `cleanup_local_gpu`: 保持勾选 (True)。
    -   **外部 API (以 OpenAI 为例)**:
        -   `api_baseurl`: `https://api.openai.com/v1`
        -   `api_key`: 填入您的 OpenAI 密钥 (`sk-xxxxxxxx`)
        -   `model`: `gpt-4o`
    -   **Google Gemini (原生)**:
        -   `api_baseurl`: `https://generativelanguage.googleapis.com/v1beta/`
        -   `api_key`: 填入您的 Google AI Studio 密钥
        -   `model`: `gemini-3.1-pro` (对话/读图) 或 `gemini-3.1-pro-image-preview` (生图)
        -   > [!TIP]
        -   > **重要提示**: 若要使用 Gemini 的 **生图功能**，模型名称必须包含 `image-` 关键词（例如 `gemini-3.1-pro-image-preview`）。单纯的对话或读图分析请使用 `gemini-3.1-pro`。
    下面是一个完整的双图转场任务的示例工作流：

![General API Node 工作流示例](./assets/workflow_example.png)

#### Text Batch Replace
-   在 `text` 字段中输入任意文本。
-   填写 `find_x` 和 `replace_x` 字段以执行顺序替换。
![Text Batch Replace 界面](./assets/text_batch_replace.png)

#### JSON Parser
-   将您的复杂JSON粘贴到 `json_payload` 字段中。
-   在 `keys_to_extract` 字段中，输入您想提取的关键字，用逗号分隔（例如 `shot, subject, audio`）。
-   节点会在JSON的任何位置找到这些关键字，将其合并后的值输出到对应的 `output_x` 端口，并在节点内显示预览。
![JSON Parser 界面](./assets/json_parser.png)

#### Show Text
-   将任何字符串输出连接到 `text` 输入。
-   文本将直接显示在节点上。

#### Simple Text
-   在文本框中输入您的文本。
-   将 `text` 输出连接到任何需要字符串输入的节点。

#### Text Split By Delimiter
-   输入文本和分隔符（默认为逗号）。
-   输出一个 `LIST` 类型，可与 `Get List Element` 配合使用。
![Text Split By Delimiter](./assets/text_split.png)

#### Get List Element
-   连接 `LIST` 输入。
-   指定索引（从0开始）以检索特定字符串。

#### Text Iterator
-   输入文本和分隔符。
-   将每个分割项作为单独 monocle 批次项输出。
-   用于迭代提示词列表或参数列表。
![Text Iterator 界面](./assets/Text_Iterator.png)

#### Markdown Extractor
- LLM 经常会话多，输出类似 ```json ... ``` 这种带格式的内容。
- 核心功能：自动识别并提取 Markdown 代码块中的纯净内容（如 JSON, Python, CSV）。
- 实用场景：LLM 生成了 JSON 结构，你的 JsonParser，多出的 ```json 字符会导致报错。有了这个节点，对接会变得“丝滑”。
![Markdown Extractor](./assets/Markdown_Extractor.png)

#### Text Template
- 核心功能：允许用户写一段带变量的模板，如 A {subject} in {style} lighting, {mood} background。节点会自动产生 subject、style、mood 三个输入插槽。
- **注意**: 在 Nodes 2.0 (Vue UI) 中，修改变量后建议右键点击节点并选择“刷新”。
![Text Template](./assets/Text_Template.png)

#### Prompt Cleaner
- 核心功能：自动移除重复的关键词，合并多余的逗号，清理不规范的空格。
- 实用场景：多节点的 Prompt 拼接经常会出现 , , 这种多余标点，这个节点可以作为发送给 KSampler 之前的“最后润色”。
![Prompt Cleaner](./assets/Prompt_Cleaner.png)

#### Text Logic Switch
- 核心功能：输入文本 A，如果其中包含某个关键词（或满足正则匹配），就把文本传给“真”输出口，否则传给“假”输出口。
- 实用场景：判断 LLM 的输出是否包含“错误”字样，如果有，就自动停止生图流，或者切换到另一个修正模型。
#### Regex Extractor Pro
- 核心功能：通过正则捕获组提取特定信息。比如从一堆描述中提取出所有括号里的十六进制颜色代码（#FFFFFF）。
- 实用场景：从长篇大论的 LLM 描述中，精准抓取颜色、光影强度、材质名称等参数，传给下方的 ControlNet 权重。

#### Dictionary Translator
- 核心功能：支持用户输入一个映射表（JSON 或简单的文本对），一键将 Prompt 中的关键词批量替换。
- 实用场景：把中文通俗词批量映射成专业的生图词库（例如：把“电影感”自动替换成 cinematic lighting, 8k, highly detailed 这一长串）。

### 📜 许可证

本项目采用 Apache 2.0 许可证。详情请参阅 [LICENSE](LICENSE) 和 [NOTICE](NOTICE) 文件。
