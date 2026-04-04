<div align="center">

# ComfyUI General API Node Pack
*Created by FeiMao-326*

[**English**](README.md) | [**中文说明**](README_CN.md)

</div>

---

## 🇬🇧 English

A suite of powerful and versatile utility nodes for ComfyUI, designed to streamline complex workflows involving Large Language Models and text manipulation. This pack is created by FeiMao-326 and is modernized for 2026 models.

### ✨ Nodes Included

This pack contains the following nodes available under the **`FeiMao-326`** category:

1.  **General API Node**: **[Core]** The Ultimate Multimodal LLM Engine.
    -   **2026 SOTA Model Support**: Native adaptation for Gemini 3.1 Pro/Flash, GPT-5.4, Llama 4, and Claude 3.5.
    -   **Smart Task Routing**: Automated redirection for Google Gemini. Use standard names like `gemini-3.1-pro` or `gemini-3.1-pro-image-preview` for chat/vision; it automatically switches to Image Gen mode when the model name includes the `image-` keyword.
    -   **Double VRAM Cleanup**: Specialized for local Ollama. When `cleanup_local_gpu` is enabled, the node triggers a REST API `keep_alive: 0` and a CLI fallback to physically purge model data from VRAM immediately after execution.
    -   **Advanced Multimodal Vision**: Supports concurrent parsing and comparison of 2 or more images.
    -   **Seed Logic**: Includes industrial-grade seed control (`fixed`, `increment`, `randomize`).
2.  **Text Batch Replace**: A powerful text utility for performing up to 8 find-and-replace operations in a single node.
3.  **JSON Parser**: Deconstructs complex, nested JSON payloads into multiple separate text outputs with a built-in labeled preview. It deeply searches for user-defined keys, perfect for handling structured prompts.
4.  **Show Text**: Displays input text directly on the node UI.
5.  **Simple Text**: A simple text input node for passing strings to other nodes.
6.  **Text Split By Delimiter**: Splits a text string into a list based on a delimiter.
7.  **Get List Element**: Retrieves a specific element from a list by index.
8.  **Text Iterator**: Splits text by delimiter and outputs it as a batch, triggering batch execution for downstream nodes.
9.  **Markdown Extractor**: Intelligent regex-based extraction of ` ```json ` or code blocks from LLM responses.
10. **Text Template (Dynamic)**: **[Recommended]** Dynamic slot template. `{var}` automatically generates input ports. Supports all languages.
11. **Prompt Cleaner**: Normalizes prompts by removing duplicates, extra commas, and empty brackets.
12. **Text Logic Switch**: Flow control (If-Else) based on content matching (Contains, Regex, Exact, etc.).
13. **Regex Extractor Pro**: Advanced pattern capture with capture group support.
14. **Dictionary Translator**: Bulk mapping/replacement via JSON or Key=Value dictionaries.

### 🔧 Installation

1.  **Clone the Repository**
    -   Open your terminal.
    -   Navigate to your ComfyUI `custom_nodes` directory:
        ```bash
        cd path/to/your/ComfyUI/custom_nodes/
        ```
    -   Clone this repository:
        ```bash
        git clone https://github.com/FeiMao-326/Comfyui-General-API-Node.git
        ```

2.  **Install Dependencies**
    -   Navigate into the newly cloned folder:
        ```bash
        cd Comfyui-General-API-Node
        ```
    -   Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Restart ComfyUI**
    -   After completing the steps above, please restart ComfyUI completely.

### 💡 How to Use

#### General API Node
1.  **Finding the Node**: In ComfyUI, you can find the node by right-clicking -> `Add Node` -> `FeiMao-326` -> `FeiMao-326 General API Node`.

    ![FeiMao-326 Node Interface](./assets/node_interface.png)

2.  **Seed Control Setup**: To enable automatic seed changes (e.g., `randomize`), connect the `seed` output of the node back to its own `seed` input. This creates a loop that updates the seed after each run.

3.  **Usage Scenarios**:
    -   **📝 Text-Only Generation**: Leave both `image_1` and `image_2` disconnected.
    -   **🖼️ Single Image Description**: Connect an image to `image_1`.
    -   **🎬 Dual Image for Video Transitions**: Connect a start frame to `image_1` and an end frame to `image_2`.
    -   **📸 Multi-Image Analysis**: You can connect multiple images (`image_1`, `image_2`, `image_3...etc`) for complex analysis tasks.

4.  **API Connection Examples**:
    -   **NVIDIA NIM (Official/Local)**:
        -   `api_baseurl`: `https://integrate.api.nvidia.com/v1`
        -   `api_key`: Your NVIDIA API Key (`nvapi-xxxxxxxx`)
        -   `model`: `meta/llama-4-maverick`, `nvidia/nemotron-3-ultra`
    -   **OpenAI GPT-5 (Latest)**:
        -   `api_baseurl`: `https://api.openai.com/v1`
        -   `api_key`: Your OpenAI API key
        -   `model`: `gpt-5.4-thinking` or `o3-pro` (Reasoning model)
    -   **Local Ollama**:
        -   `api_baseurl`: `http://127.0.0.1:11434/v1`
        -   `api_key`: `ollama`
        -   `model`: `gemma4:e4b` (Current default, supports vision analysis)
        -   `cleanup_local_gpu`: Keep it checked (True).
    -   **Google Gemini (Native)**:
        -   `api_baseurl`: `https://generativelanguage.googleapis.com/v1beta/`
        -   `api_key`: Your Google AI Studio Key
        -   `model`: `gemini-3.1-pro` (Chat/Vision) or `gemini-3.1-pro-image-preview` (Image Gen)
        -   > [!TIP]
        -   > **Important**: For **Image Generation**, the model name MUST contain the keyword `image-` (e.g., `gemini-3.1-pro-image-preview`). For **Chat/Reasoning**, use standard names like `gemini-3.1-pro`.

    ![General API Node Workflow Example](./assets/workflow_example.png)

#### Text Batch Replace
- Perform multiple find-and-replace operations sequentially.
![Text Batch Replace Interface](./assets/text_batch_replace.png)

#### JSON Parser
- Automatically parses LLM JSON outputs into independent string slots based on defined keys.
![JSON Parser Interface](./assets/json_parser.png)

#### Simple Text / Show Text
- Basic input and visual display modules.

#### Text Split / Get Element / Iterator
- Essential tools for handling lists and batch execution flows.
![Text Iterator Interface](./assets/Text_Iterator.png)

#### Markdown Extractor
- **Problem**: LLMs often reply with chatter like "Sure! Here is your JSON: ```json ... ```".
- **Solution**: Automatically identifies and extracts clean content from Markdown code blocks.
- **Scenario**: When LLM generates a JSON structure, passing it directly to JsonParser would crash due to Markdown syntax. This node ensures a "smooth" connection.
![Markdown Extractor](./assets/Markdown_Extractor.png)

#### Text Template (Dynamic)
- **Concept**: Write a template with variables: `A {subject} in {style} lighting, {mood} background`.
- **Magic**: The node instantly creates input slots for `subject`, `style`, and `mood`.
- **Note**: In Nodes 2.0 (Vue UI), right-click and "Refresh" the node after modifying variables.
![Text Template](./assets/Text_Template.png)

#### Prompt Cleaner
- **Function**: Removes duplicate keywords, merges extra commas, and cleans inconsistent spaces.
- **Scenario**: Multiple prompt concatenations often result in messy punctuation (e.g., `, ,`). Use this as a "final touch" before KSampler.
![Prompt Cleaner](./assets/Prompt_Cleaner.png)

#### Text Logic Switch
- **Function**: Flow control (If-Else). If input text contains a keyword (or matches regex), output travels to the "True" port, otherwise "False".
- **Scenario**: Check if LLM output contains "Error" to stop the workflow or switch to a fallback model.

#### Regex Extractor Pro
- **Function**: Precise data extraction using Capture Groups.
- **Scenario**: Extract specific info like HEX color codes (#FFFFFF) or numeric coordinates from a long LLM description.

#### Dictionary Translator
- **Function**: Bulk tag replacement using a mapping table (JSON or Simple Text Pairs).
- **Scenario**: Map common Chinese terms to professional SD tags (e.g., replace "Cinematic" with "cinematic lighting, 8k, highly detailed").

---

### 📜 License
This project is licensed under the Apache 2.0 License.
