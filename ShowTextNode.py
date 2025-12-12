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

class ShowTextNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    CATEGORY = "FeiMao-326"

    def notify(self, text):
        # text is always a list because INPUT_IS_LIST = True
        # If connected to a single string output, it will be a list with one item.
        # If connected to a batch (like Text Iterator), it will be a list of all items.
        
        # Join them for display or pass as list? 
        # The frontend likely expects a list of strings if we want multiple lines/blocks.
        # Let's return the list directly to "text" key.
        return {"ui": {"text": text}, "result": (text,)}
