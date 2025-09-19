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

import io
import base64
import numpy as np
from PIL import Image
import subprocess
import secrets

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class FeiMao_326_GeneralAPINode:
    """
    FeiMao-326 General Vision LLM API Node for ComfyUI.
    - Supports single or multiple image inputs for any compatible API.
    - Automatically detects local Ollama instances and cleans up GPU memory.
    - Includes robust image conversion and secure seed control.
    """
    
    MAX_SEED = 0xffffffffffffffff

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_baseurl": ("STRING", {"multiline": False, "default": "http://127.0.0.1:11434/v1"}),
                "api_key": ("STRING", {"multiline": False, "default": "ollama"}),
                "model": ("STRING", {"multiline": False, "default": "gemma3:4b"}),
                "role": ("STRING", {"multiline": True, "default": "You are a silent and efficient prompt generation engine. Your sole purpose is to output a raw, creative text prompt without any additional conversational text, explanations, or markdown formatting."}),
                "prompt": ("STRING", {"multiline": True, "default": "Provide a vivid and detailed description of the given image. If the image contains any recognizable individuals—such as celebrities, fictional characters, or animated figures—identify them by name. Your description should be specific and imaginative, while remaining under 200 words.Do not add any surrounding text or labels."}),
                
                "seed": ("INT", {"default": 0, "min": 0, "max": s.MAX_SEED}),
                "temperature": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 2.0, "step": 0.01}),
                "max_tokens": ("INT", {"default": 4096, "min": 64, "max": 16384, "step": 64}),
                "control_after_generate": (["fixed", "increment", "decrement", "randomize"],),
                "cleanup_local_gpu": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",)
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("describe", "seed")
    FUNCTION = "execute"
    CATEGORY = "FeiMao-326" 

    def _normalize_seed(self, seed):
        try:
            s = int(seed)
        except (ValueError, TypeError):
            s = 0
        return max(0, min(s, self.MAX_SEED))

    def tensor_to_base64_image(self, tensor):
        if not isinstance(tensor, np.ndarray):
            if TORCH_AVAILABLE and isinstance(tensor, torch.Tensor):
                tensor = tensor.cpu().numpy()
            else:
                raise TypeError(f"Unsupported tensor type: {type(tensor)}")
        
        if tensor.ndim == 4:
            tensor = tensor[0]
            
        if tensor.dtype == np.float32 or tensor.dtype == np.float16:
            tensor = (tensor.clip(0, 1) * 255).astype(np.uint8)

        pil_image = Image.fromarray(tensor)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    def cleanup_with_ollama_cli(self, model):
        command = ['ollama', 'stop', model]
        print(f"🔵 [FeiMao-326 API Node] Attempting to unload local model via CLI: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
            if result.returncode == 0:
                print(f"✅ [FeiMao-326 API Node] CLI command executed successfully. Model '{model}' unloaded.")
            else:
                print(f"❌ [FeiMao-326 API Node] CLI command execution failed: {result.stderr.strip()}")
        except FileNotFoundError:
            print("❌ [FeiMao-326 API Node] Error: 'ollama' command not found. Please ensure Ollama is installed correctly.")
        except Exception as e:
            print(f"⚠️ [FeiMao-326 API Node] An error occurred while executing the CLI command: {str(e)}")

    def execute(self, api_baseurl, api_key, model, role, prompt, seed, temperature, max_tokens, control_after_generate,
                cleanup_local_gpu=True, image_1=None, image_2=None):
        
        current_seed = self._normalize_seed(seed)
        
        if not OPENAI_AVAILABLE: 
            return ("Error: The 'openai' library is not installed. Please run: pip install -r requirements.txt", current_seed)
        if not api_baseurl or not model: 
            return ("Error: 'api_baseurl' and 'model' are required fields.", current_seed)

        try: 
            client = openai.OpenAI(api_key=api_key, base_url=api_baseurl)
        except Exception as e: 
            return (f"Failed to initialize the API client: {type(e).__name__}: {str(e)}", current_seed)

        messages = [{"role": "system", "content": role}]
        user_content = [{"type": "text", "text": prompt}]
        
        has_images = False
        if image_1 is not None:
            try:
                print(f"🖼️ [FeiMao-326 API Node] Processing image 1...")
                base64_image = self.tensor_to_base64_image(image_1)
                user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})
                has_images = True
            except Exception as e:
                return (f"Failed to process image 1: {type(e).__name__}: {str(e)}", current_seed)
        
        if image_2 is not None:
            try:
                print(f"🖼️ [FeiMao-326 API Node] Processing image 2...")
                base64_image = self.tensor_to_base64_image(image_2)
                user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})
                has_images = True
            except Exception as e:
                return (f"Failed to process image 2: {type(e).__name__}: {str(e)}", current_seed)
        
        messages.append({"role": "user", "content": user_content if has_images else prompt})
        
        response_text = ""
        try:
            print(f"🔵 [FeiMao-326 API Node] Calling model '{model}' at '{api_baseurl}'...")
            
            api_params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "seed": current_seed,
                "max_tokens": max_tokens
            }
            
            response = client.chat.completions.create(**api_params)
            response_text = response.choices[0].message.content
            print(f"✅ [FeiMao-326 API Node] API call successful.")

        except Exception as e:
            error_message = f"API call failed: {type(e).__name__}: {str(e)}"
            print(f"❌ [FeiMao-326 API Node] {error_message}")
            if "context_length" in str(e).lower() or "token" in str(e).lower():
                error_message += "\n\nHint: The input (especially images) might be too large for the model's context window. Try reducing the image resolution."
            elif has_images and ("invalid" in str(e).lower() or "variant" in str(e).lower()):
                 error_message += f"\n\nHint: The model '{model}' may not support image inputs. Try a vision-capable model like 'llava'."
            response_text = error_message

        finally:
            is_local_ollama = "127.0.0.1" in api_baseurl or "localhost" in api_baseurl
            if cleanup_local_gpu and is_local_ollama:
                self.cleanup_with_ollama_cli(model)
                if TORCH_AVAILABLE and torch.cuda.is_available():
                    print(f"🔵 [FeiMao-326 API Node] Clearing PyTorch GPU cache...")
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()
                    print(f"✅ [FeiMao-326 API Node] PyTorch GPU cache cleared.")
            elif cleanup_local_gpu and not is_local_ollama:
                print(f"🔵 [FeiMao-326 API Node] External API URL detected, skipping local GPU cleanup.")

        if control_after_generate == "increment":
            next_seed = current_seed + 1
        elif control_after_generate == "decrement":
            next_seed = current_seed - 1
        elif control_after_generate == "randomize":
            next_seed = secrets.randbits(64)
        else:
            next_seed = current_seed
            
        return (response_text, self._normalize_seed(next_seed))