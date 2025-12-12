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
    @classmethod
    def INPUT_TYPES(s):
        inputs = {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""})
            },
            "optional": {}
        }
        
        for i in range(1, 9):
            inputs["optional"][f"find_{i}"] = ("STRING", {"multiline": False, "default": ""})
            inputs["optional"][f"replace_{i}"] = ("STRING", {"multiline": False, "default": ""})
            
        return inputs

    RETURN_TYPES = ("STRING",); RETURN_NAMES = ("text",); FUNCTION = "execute"; CATEGORY = "FeiMao-326"
    def execute(self, text, **kwargs):
        modified_text = text
        
        all_pairs = []
        for key, value in kwargs.items():
            if key.startswith("find_"):
                try:
                    idx = int(key.split("_")[1])
                    all_pairs.append((idx, value, kwargs.get(f"replace_{idx}", "")))
                except ValueError:
                    pass
        
        # Sort by index
        all_pairs.sort(key=lambda x: x[0])
        
        # Re-apply based on sorted list
        for _, find_s, replace_s in all_pairs:
            if find_s:
                modified_text = modified_text.replace(find_s, replace_s)
                
        return (modified_text,)