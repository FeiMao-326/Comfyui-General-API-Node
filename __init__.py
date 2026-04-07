# Copyright 2025 FeiMao-326
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__version__ = "1.0.7"

from .general_api_node import FeiMao_326_GeneralAPINode
from .text_utils_node import FeiMao_326_TextBatchReplace, FeiMao_326_MarkdownExtractor, FeiMao_326_TextTemplate, FeiMao_326_PromptCleaner, FeiMao_326_TextLogicSwitch, FeiMao_326_RegexExtractor, FeiMao_326_DictionaryReplace
from .json_parser_node import FeiMao_326_JsonParser
from .ShowTextNode import FeiMao_326_ShowTextNode
from .SimpleTextNode import FeiMao_326_SimpleTextNode
from .list_utils_node import FeiMao_326_TextSplitByDelimiter, FeiMao_326_GetListElement, FeiMao_326_TextIterator
from .file_io_node import FeiMao_326_SaveText, FeiMao_326_LoadText


NODE_CLASS_MAPPINGS = {
    "FeiMao_326_GeneralAPINode": FeiMao_326_GeneralAPINode,
    "FeiMao_326_TextBatchReplace": FeiMao_326_TextBatchReplace,
    "FeiMao_326_JsonParser": FeiMao_326_JsonParser,
    "FeiMao_326_ShowTextNode": FeiMao_326_ShowTextNode,
    "FeiMao_326_SimpleTextNode": FeiMao_326_SimpleTextNode,
    "FeiMao_326_TextSplitByDelimiter": FeiMao_326_TextSplitByDelimiter,
    "FeiMao_326_GetListElement": FeiMao_326_GetListElement,
    "FeiMao_326_TextIterator": FeiMao_326_TextIterator,
    "FeiMao_326_MarkdownExtractor": FeiMao_326_MarkdownExtractor,
    "FeiMao_326_TextTemplate": FeiMao_326_TextTemplate,
    "FeiMao_326_PromptCleaner": FeiMao_326_PromptCleaner,
    "FeiMao_326_TextLogicSwitch": FeiMao_326_TextLogicSwitch,
    "FeiMao_326_RegexExtractor": FeiMao_326_RegexExtractor,
    "FeiMao_326_DictionaryReplace": FeiMao_326_DictionaryReplace,
    "FeiMao_326_SaveText": FeiMao_326_SaveText,
    "FeiMao_326_LoadText": FeiMao_326_LoadText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FeiMao_326_GeneralAPINode": f"General API Node v{__version__} (FeiMao-326)",
    "FeiMao_326_TextBatchReplace": f"Text Batch Replace (FeiMao-326)",
    "FeiMao_326_JsonParser": f"JSON Parser (FeiMao-326)",
    "FeiMao_326_ShowTextNode": "Show Text (FeiMao-326)",
    "FeiMao_326_SimpleTextNode": "Simple Text (FeiMao-326)",
    "FeiMao_326_TextSplitByDelimiter": "Text Split By Delimiter (Array) (FeiMao-326)",
    "FeiMao_326_GetListElement": "Get List Element (List) (FeiMao-326)",
    "FeiMao_326_TextIterator": "Text Iterator (FeiMao-326)",
    "FeiMao_326_MarkdownExtractor": "Markdown Extractor (FeiMao-326)",
    "FeiMao_326_TextTemplate": "Text Template (FeiMao-326)",
    "FeiMao_326_PromptCleaner": "Prompt Cleaner (FeiMao-326)",
    "FeiMao_326_TextLogicSwitch": "Text Logic Switch (FeiMao-326)",
    "FeiMao_326_RegexExtractor": "Regex Extractor Pro (FeiMao-326)",
    "FeiMao_326_DictionaryReplace": "Dictionary Translator (FeiMao-326)",
    "FeiMao_326_SaveText": "Save Text (FeiMao-326)",
    "FeiMao_326_LoadText": "Load Text (FeiMao-326)",
}

WEB_DIRECTORY = "./js"

print(f"✅ FeiMao-326 Custom Nodes (Version: {__version__}) loaded successfully.")