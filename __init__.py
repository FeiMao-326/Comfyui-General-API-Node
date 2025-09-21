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

__version__ = "1.0.1"

from .general_api_node import FeiMao_326_GeneralAPINode
from .text_utils_node import FeiMao_326_TextBatchReplace
from .json_parser_node import FeiMao_326_JsonParser

NODE_CLASS_MAPPINGS = {
    "FeiMao_326_GeneralAPINode": FeiMao_326_GeneralAPINode,
    "FeiMao_326_TextBatchReplace": FeiMao_326_TextBatchReplace,
    "FeiMao_326_JsonParser": FeiMao_326_JsonParser,
        "FeiMao_326_JsonParser": FeiMao_326_JsonParser,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FeiMao_326_GeneralAPINode": f"General API Node v{__version__} (FeiMao-326)",
    "FeiMao_326_TextBatchReplace": f"Text Batch Replace (FeiMao-326)",
    "FeiMao_326_JsonParser": f"JSON Parser (FeiMao-326)",
}

print(f"✅ FeiMao-326 Custom Nodes (Version: {__version__}) loaded successfully.")