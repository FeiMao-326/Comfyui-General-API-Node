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
                
<<<<<<< HEAD
        return (modified_text,)
=======
        return (modified_text,)

class FeiMao_326_MarkdownExtractor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "remove_artifacts": ("BOOLEAN", {"default": True}),
                "first_block_only": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, remove_artifacts, first_block_only):
        import re
        # Find all ```blocks```
        pattern = re.compile(r'```(?:\w+)?\n?(.*?)```', re.DOTALL)
        matches = pattern.findall(text)
        
        if not matches:
            result = text
        else:
            if first_block_only:
                result = matches[0].strip()
            else:
                result = "\n\n".join([m.strip() for m in matches])
        
        if remove_artifacts:
            # Strip common markdown signs if they are lingering
            result = re.sub(r'(\*\*|__)', '', result)
            result = re.sub(r'^#+\s+', '', result, flags=re.MULTILINE)
            
        return (result,)

class FeiMao_326_TextTemplate:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "template": ("STRING", {"multiline": True, "placeholder": "Example: A {subject} in {style} style."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, template, **kwargs):
        # Result string will be formatted using dynamic inputs
        # ComfyUI passing dynamic inputs via **kwargs
        import re
        result = template
        
        # We find all matches to avoid KeyErrors
        # Support for all languages (Unicode) in variables
        found_vars = re.findall(r'\{([^{}\s]+)\}', template)
        
        for var in found_vars:
            if var in kwargs:
                val = str(kwargs[var])
                result = result.replace(f"{{{var}}}", val)
            else:
                # Keep as is or replace with empty if not connected? 
                # Better keep as is to allow nested templates or partial fills
                pass
                
        return (result,)

class FeiMao_326_PromptCleaner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "remove_duplicate_tags": ("BOOLEAN", {"default": True}),
                "clean_brackets": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, remove_duplicate_tags, clean_brackets):
        import re
        # 1. Normalize commas and spaces
        cleaned = text.replace("\n", ", ")
        cleaned = re.sub(r',\s*,', ',', cleaned) # Multi commas
        
        # 2. Split by comma
        tags = [t.strip() for t in cleaned.split(",")]
        
        # 3. Remove duplicates while keeping order
        if remove_duplicate_tags:
            seen = set()
            new_tags = []
            for t in tags:
                if t and t.lower() not in seen:
                    new_tags.append(t)
                    seen.add(t.lower())
            tags = new_tags
        else:
            tags = [t for t in tags if t]
            
        result = ", ".join(tags)
        
        if clean_brackets:
            # Remove empty brackets like (), ( ), [], [ ]
            result = re.sub(r'\(\s*\)', '', result)
            result = re.sub(r'\[\s*\]', '', result)
            # Remove trailing/leading commas again after bracket cleanup
            result = re.sub(r',\s*,', ',', result)
            
        return (result.strip(", "),)

class FeiMao_326_TextLogicSwitch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "pattern": ("STRING", {"default": ""}),
                "mode": (["contains", "not_contains", "regex", "exactly", "starts_with", "ends_with"], {"default": "contains"}),
                "on_true": ("STRING", {"multiline": True, "default": "True"}),
                "on_false": ("STRING", {"multiline": True, "default": "False"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, pattern, mode, on_true, on_false):
        import re
        is_true = False
        
        if mode == "contains":
            is_true = pattern in text
        elif mode == "not_contains":
            is_true = pattern not in text
        elif mode == "exactly":
            is_true = text == pattern
        elif mode == "starts_with":
            is_true = text.startswith(pattern)
        elif mode == "ends_with":
            is_true = text.endswith(pattern)
        elif mode == "regex":
            try:
                is_true = bool(re.search(pattern, text))
            except:
                is_true = False
                
        return (on_true if is_true else on_false,)

class FeiMao_326_RegexExtractor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "regex": ("STRING", {"default": r"(\d+)"}),
                "group_index": ("INT", {"default": 1, "min": 0, "max": 99}),
                "all_matches": ("BOOLEAN", {"default": False}),
                "delimiter": ("STRING", {"default": ", "}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, regex, group_index, all_matches, delimiter):
        import re
        try:
            pattern = re.compile(regex)
            if all_matches:
                matches = pattern.finditer(text)
                results = []
                for m in matches:
                    try:
                        results.append(m.group(group_index))
                    except IndexError:
                        pass
                return (delimiter.join(results),)
            else:
                match = pattern.search(text)
                if match:
                    try:
                        return (match.group(group_index),)
                    except IndexError:
                        return ("",)
                return ("",)
        except Exception as e:
            return (f"Regex Error: {str(e)}",)

class FeiMao_326_DictionaryReplace:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "dictionary_data": ("STRING", {"multiline": True, "placeholder": "key=value or JSON {\"key\": \"value\"}"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326"

    def execute(self, text, dictionary_data):
        import json
        
        mapping = {}
        # 1. Try JSON
        try:
            mapping = json.loads(dictionary_data)
        except:
            # 2. Try Key=Value lines
            lines = dictionary_data.strip().split("\n")
            for line in lines:
                if "=" in line:
                    k, v = line.split("=", 1)
                    mapping[k.strip()] = v.strip()
                elif ":" in line:
                    k, v = line.split(":", 1)
                    mapping[k.strip()] = v.strip()

        if not mapping:
            return (text,)
            
        result = text
        # To avoid partial replacements causing issues, 
        # we sort keys by length (longest first)
        sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
        
        for k in sorted_keys:
            if k:
                result = result.replace(k, mapping[k])
                
        return (result,)
>>>>>>> e9ec5ee (feat: Release v1.0.6 with 6 new advanced text nodes and Nodes 2.0 (Vue UI) optimization)
