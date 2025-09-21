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

import json

class FeiMao_326_JsonParser:
    MAX_OUTPUTS = 8
    @classmethod
    def INPUT_TYPES(s):
        default_json = {"shot": {"composition": "central low-angle wide"}, "subject": {"description": "CBR 150 assembling"}, "scene": {"location": "desert basin"}, "audio": {"music": "trailer score"}}
        return {"required": {"json_payload": ("STRING", {"multiline": True, "default": json.dumps(default_json, indent=4)}), "keys_to_extract": ("STRING", {"multiline": False, "default": "shot, subject, scene, audio"})}}
    RETURN_TYPES = tuple(["STRING"] * 8); RETURN_NAMES = tuple([f"output_{i}" for i in range(1, 9)]); FUNCTION = "execute"; CATEGORY = "FeiMao-326"
    def _find_and_combine_values(self, data, target_key):
        found_values = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    if isinstance(value, dict): found_values.append(", ".join(filter(None, [str(v) for v in value.values() if v])))
                    elif isinstance(value, list): found_values.append(", ".join(filter(None, [str(v) for v in value if v])))
                    elif value: found_values.append(str(value))
                else: found_values.extend(self._find_and_combine_values(value, target_key))
        elif isinstance(data, list):
            for item in data: found_values.extend(self._find_and_combine_values(item, target_key))
        return found_values
    def execute(self, json_payload, keys_to_extract):
        output_keys = [key.strip() for key in keys_to_extract.split(',') if key.strip()]
        try: data = json.loads(json_payload)
        except json.JSONDecodeError as e:
            error_message = f"ERROR: Invalid JSON format. {e}"; print(f"❌ [FeiMao-326 JSON Parser] {error_message}")
            return tuple([error_message] + [""] * 7)
        results = []
        for i in range(self.MAX_OUTPUTS):
            if i < len(output_keys):
                key = output_keys[i]; found = self._find_and_combine_values(data, key); results.append(", ".join(found))
            else: results.append("")
        return tuple(results)