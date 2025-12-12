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

class FeiMao_326_TextSplitByDelimiter:
    """
    Splits a text string into a list based on a delimiter.
    Returns a custom LIST type that can be passed to GetListElement.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "delimiter": ("STRING", {"multiline": False, "default": ","}),
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("array",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, delimiter):
        if not delimiter:
            # If delimiter is empty, split by lines or just return the whole text as one item?
            # Standard behavior for split with empty string is error, so let's default to newline if empty or just list of chars?
            # Let's assume user wants to split by newline if delimiter is literally empty string, or just return [text]
            # But usually delimiter is specified. Let's stick to strict split.
            # If delimiter is empty, we can't split. Let's return [text].
            return ([text],)
        
        # Handle escaped newlines if user types \n
        delimiter = delimiter.replace("\\n", "\n")
        
        arr = text.split(delimiter)
        # Strip whitespace from items? Maybe optional? For now let's keep it raw or maybe strip?
        # The screenshot shows "Keep this exact car..." which looks like prompts. 
        # Usually we want to strip leading/trailing whitespace.
        arr = [item.strip() for item in arr]
        return (arr,)

class FeiMao_326_GetListElement:
    """
    Retrieves a specific element from a list by index.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "list_input": ("LIST",),
                "index": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("item",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, list_input, index):
        if not isinstance(list_input, list):
            return ("",)
        
        if index < 0 or index >= len(list_input):
            print(f"Warning: Index {index} out of bounds for list of length {len(list_input)}. Returning empty string.")
            return ("",)
            
        return (list_input[index],)

class FeiMao_326_TextIterator:
    """
    Splits text by delimiter and outputs it as a batch (list).
    This triggers ComfyUI's batch execution for downstream nodes.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "delimiter": ("STRING", {"multiline": False, "default": ","}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, delimiter):
        if not delimiter:
            return ([text],)
            
        delimiter = delimiter.replace("\\n", "\n")
        arr = text.split(delimiter)
        arr = [item.strip() for item in arr]
        return (arr,)
