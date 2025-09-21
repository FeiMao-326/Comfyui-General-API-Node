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

class FeiMao_326_TextBatchReplace:
    MAX_PAIRS = 10
    @classmethod
    def INPUT_TYPES(s):
        inputs = {"required": {"text": ("STRING", {"multiline": True, "default": ""})}, "optional": {}}
        for i in range(1, s.MAX_PAIRS + 1):
            inputs["optional"][f"find_{i}"] = ("STRING", {"multiline": False, "default": ""})
            inputs["optional"][f"replace_{i}"] = ("STRING", {"multiline": False, "default": ""})
        return inputs
    RETURN_TYPES = ("STRING",); RETURN_NAMES = ("text",); FUNCTION = "execute"; CATEGORY = "FeiMao-326"
    def execute(self, text, **kwargs):
        modified_text = text
        for i in range(1, self.MAX_PAIRS + 1):
            find_str = kwargs.get(f"find_{i}", ""); replace_str = kwargs.get(f"replace_{i}", "")
            if find_str: modified_text = modified_text.replace(find_str, replace_str)
        return (modified_text,)