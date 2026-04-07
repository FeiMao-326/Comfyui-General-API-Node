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

import os
import folder_paths

class FeiMao_326_SaveText:
    """
    Saves the input text string to a file in the ComfyUI output directory.
    Useful for persisting LLM responses, generated prompts, or markdown reports.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True, "multiline": True}),
                "filename": ("STRING", {"default": "output.txt"}),
                "append": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "FeiMao-326"

    def execute(self, text, filename, append):
        output_dir = folder_paths.get_output_directory()
        filepath = os.path.join(output_dir, filename)
        
        # Ensure parent directories exist (e.g. filename="prompts/output.txt")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        mode = "a" if append else "w"
        try:
            with open(filepath, mode, encoding="utf-8") as f:
                f.write(str(text) + ("\n" if append else ""))
            print(f"✅ [FeiMao-326 Save Text] Saved to {filepath}")
        except Exception as e:
            print(f"❌ [FeiMao-326 Save Text] Error saving file: {e}")
            
        return (text,)


class FeiMao_326_LoadText:
    """
    Loads text from a .txt or .json file located in the ComfyUI input directory.
    Useful for injecting long context, templates, or previously saved knowledge into LLM workflows.
    """
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        # Find all text-based files in the input folder
        try:
            files = sorted([f for f in os.listdir(input_dir) if f.endswith((".txt", ".json", ".md", ".csv"))])
        except FileNotFoundError:
            files = []
        if not files:
            files = ["(No .txt / .json found in 'input' folder)"]
            
        return {
            "required": {
                "filename": (files,),
            }
        }
        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, filename):
        input_dir = folder_paths.get_input_directory()
        filepath = os.path.join(input_dir, filename)
        
        if not os.path.exists(filepath):
            error_msg = f"Error: File '{filename}' not found in the input directory."
            print(f"❌ [FeiMao-326 Load Text] {error_msg}")
            return (error_msg,)
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            return (content,)
        except Exception as e:
            error_msg = f"Error reading file '{filename}': {str(e)}"
            print(f"❌ [FeiMao-326 Load Text] {error_msg}")
            return (error_msg,)
