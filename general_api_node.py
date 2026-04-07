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
import locale
import requests  # [NEW] Added for direct API calls (e.g. Google Imagen)

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
    - Supports single or multiple image inputs for any compatible API (OpenAI-compatible).
    - Supports native Google Gemini URLs (auto-converts for Chat, handles direct for Imagen).
    - Supports Image Generation (DALL-E, Imagen).
    - Automatically detects local Ollama instances and cleans up GPU memory.
    """
    
    MAX_SEED = 0xffffffffffffffff

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_baseurl": ("STRING", {"multiline": False, "default": "http://127.0.0.1:11434/v1"}),
                "api_key": ("STRING", {"multiline": False, "default": "ollama"}),
                "model": ("STRING", {"multiline": False, "default": "gemma4:e4b"}),
                "role": ("STRING", {"multiline": True, "default": "You are a helpful assistant. Follow the user's instructions exactly. Output only the requested content without conversational filler, markdown formatting, or explanations."}),
                "prompt": ("STRING", {"multiline": True, "default": "Describe this image in detail."}),
                
                "seed": ("INT", {"default": 0, "min": 0, "max": s.MAX_SEED}),
                "temperature": ("FLOAT", {"default": 0.6, "min": 0.0, "max": 2.0, "step": 0.01}),
                "max_tokens": ("INT", {"default": 4096, "min": 64, "max": 131072, "step": 512}),
                "control_after_generate": (["fixed", "increment", "decrement", "randomize"],),
                "cleanup_local_gpu": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "system_proxy": ("STRING", {"multiline": False, "default": ""}),
                "force_json_format": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "IMAGE")  # [MODIFIED] Added IMAGE output
    RETURN_NAMES = ("describe", "seed", "image") # [MODIFIED] Added image output name
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
    
    def base64_to_tensor(self, base64_str):
        """Converts base64 string to torch tensor (BHWC float32)"""
        try:
            image_data = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            image_np = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np).unsqueeze(0) # Add batch dimension -> (1, H, W, 3)
            return image_tensor
        except Exception as e:
            print(f"❌ [FeiMao-326 API Node] Internal Error converting Base64 to Tensor: {e}")
            return self.get_empty_image()

    def get_empty_image(self):
        """Returns a 1x1x3 black image tensor"""
        return torch.zeros((1, 1, 1, 3), dtype=torch.float32)


    def cleanup_ollama_model(self, api_baseurl, model):
        """
        Unloads an Ollama model from memory.
        1. Primary attempt: Native REST API with keep_alive: 0 (No environment variables required).
        2. Fallback: CLI 'ollama stop' command (Depends on system PATH).
        """
        model_unloaded = False
        
        # --- 1. PRIMARY: REST API UNLOAD ---
        try:
            # Construct Ollama native generate URL (usually /v1 -> /api/generate)
            # Example: http://127.0.0.1:11434/v1 -> http://127.0.0.1:11434/api/generate
            if "/v1" in api_baseurl:
                unload_url = api_baseurl.replace("/v1", "/api/generate").rstrip("/")
            else:
                # If it's a custom URL, try to guess the root
                from urllib.parse import urlparse
                parsed = urlparse(api_baseurl)
                unload_url = f"{parsed.scheme}://{parsed.netloc}/api/generate"

            print(f"🔵 [FeiMao-326 API Node] Attempting to unload model '{model}' via REST API...")
            payload = {
                "model": model,
                "keep_alive": 0 # Unload immediately
            }
            response = requests.post(unload_url, json=payload, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ [FeiMao-326 API Node] Model '{model}' successfully unloaded via API.")
                model_unloaded = True
            else:
                print(f"⚠️ [FeiMao-326 API Node] API unload status: {response.status_code}. Falling back to CLI.")
                
        except Exception as e:
            print(f"⚠️ [FeiMao-326 API Node] REST API unload failed ({type(e).__name__}). Falling back to CLI.")

        # --- 2. FALLBACK: CLI COMMAND ---
        if not model_unloaded:
            command = ['ollama', 'stop', model]
            print(f"🔵 [FeiMao-326 API Node] Attempting to unload via CLI: {' '.join(command)}")
            try:
                result = subprocess.run(command, capture_output=True, timeout=10, check=False)
                
                if result.returncode == 0:
                    print(f"✅ [FeiMao-326 API Node] Model '{model}' successfully stopped via CLI.")
                else:
                    stderr_output = result.stderr.decode(locale.getpreferredencoding(), errors='replace')
                    print(f"❌ [FeiMao-326 API Node] CLI stop failed: {stderr_output.strip()}")
            except FileNotFoundError:
                print("❌ [FeiMao-326 API Node] Error: 'ollama' command not found. Environment variable may not be configured.")
            except Exception as e:
                print(f"⚠️ [FeiMao-326 API Node] CLI stop error: {str(e)}")

    def execute(self, api_baseurl, api_key, model, role, prompt, seed, temperature, max_tokens, control_after_generate,
                cleanup_local_gpu=True, system_proxy="", force_json_format=False, image_1=None, image_2=None, image_3=None, **kwargs):
        
        current_seed = self._normalize_seed(seed)
        generated_image_tensor = self.get_empty_image() # Default empty image
        

        # --- 0. AUTO-MAPPING DEPRECATED MODELS ---
        if "gemini-3-pro-preview" in model.lower():
            print(f"⚠️ [FeiMao_326 API Node] Model 'gemini-3-pro-preview' is deprecated. Auto-redirecting to 'gemini-3.1-pro'.")
            model = model.replace("gemini-3-pro-preview", "gemini-3.1-pro")
        

        # Enforce silent role if empty or default
        if not role or not role.strip():
            role = "You are a helpful assistant. Follow the user's instructions exactly. Output only the requested content without conversational filler."

        if not OPENAI_AVAILABLE: 
            return ("Error: The 'openai' library is not installed. Please run: pip install -r requirements.txt", current_seed, generated_image_tensor)
        if not api_baseurl or not model: 
            return ("Error: 'api_baseurl' and 'model' are required fields.", current_seed, generated_image_tensor)

        # --- 1. HANDLE GEMINI NATIVE URLS & IMAGE GENERATION DETECTION ---
        is_gemini_native = "generativelanguage.googleapis.com" in api_baseurl
        lower_model = model.lower()
        is_imagen_model = "imagen" in lower_model
        is_gemini_image_model = "gemini" in lower_model and "image-" in lower_model
        is_dalle_model = "dall-e" in lower_model
        is_vision_generation = is_imagen_model or is_gemini_image_model or is_dalle_model

        # Auto-correct Gemini base URL for Chat Completions if needed
        # Native: https://generativelanguage.googleapis.com/v1beta/
        # OpenAI Compatible: https://generativelanguage.googleapis.com/v1beta/openai/
        if is_gemini_native and not "openai" in api_baseurl and not is_vision_generation:
            if api_baseurl.endswith("/"):
                api_baseurl += "openai/"
            else:
                api_baseurl += "/openai/"
            print(f"🔵 [FeiMao-326 API Node] Auto-corrected Gemini URL to OpenAI-compatible endpoint: {api_baseurl}")

        # Initialize Client (only needed for Chat or DALL-E, not for Gemini native Rest)
        client = None
        if not (is_gemini_native and is_imagen_model):
            client_params = {"api_key": api_key, "base_url": api_baseurl}
            if system_proxy and system_proxy.strip():
                try:
                    import httpx
                    proxies = {"http://": system_proxy.strip(), "https://": system_proxy.strip()}
                    client_params["http_client"] = httpx.Client(proxies=proxies)
                    print(f"🌐 [FeiMao-326 API Node] Enabled System Proxy: {system_proxy.strip()}")
                except ImportError:
                    print("⚠️ [FeiMao-326 API Node] 'httpx' is required for proxy support. Please run 'pip install httpx'.")

            try: 
                client = openai.OpenAI(**client_params)
            except Exception as e: 
                return (f"Failed to initialize the API client: {type(e).__name__}: {str(e)}", current_seed, generated_image_tensor)

        # --- 2. EXECUTION BRANCHING ---
        
        # BRANCH A: Gemini Native Image Generation (via REST API)
        if is_gemini_native and (is_imagen_model or is_gemini_image_model):
            print(f"🎨 [FeiMao-326 API Node] Detected Google generation task...")
            
            # Remove trailing slash and openai part if mistakenly present for REST call
            clean_base_url = api_baseurl.replace("/openai/", "/").rstrip("/")
            
            req_proxies = None
            if system_proxy and system_proxy.strip():
                req_proxies = {"http": system_proxy.strip(), "https": system_proxy.strip()}

            
            try:
                # Sub-branch A1: Imagen Models (use :predict)
                if is_imagen_model:
                    print(f"🔹 Using 'predict' endpoint for Imagen model: {model}")
                    url = f"{clean_base_url}/models/{model}:predict?key={api_key}"
                    payload = {
                        "instances": [{"prompt": prompt}],
                        "parameters": {"sampleCount": 1}
                    }
                    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, proxies=req_proxies)
                    
                    if response.status_code != 200:
                        raise Exception(f"Google API Error {response.status_code}: {response.text}")
                    
                    data = response.json()
                    if "predictions" in data and len(data["predictions"]) > 0:
                        b64_img = data["predictions"][0]["bytesBase64Encoded"]
                        generated_image_tensor = self.base64_to_tensor(b64_img)
                        response_text = "Image generated successfully via Google Imagen."
                    else:
                        raise Exception("No image data found in Google Imagen response.")

                # Sub-branch A2: Gemini Image Models (use :generateContent)
                # This covers 'gemini-3-pro-image-preview' etc.
                else: 
                    print(f"🔹 Using 'generateContent' endpoint for Gemini Image model: {model}")
                    url = f"{clean_base_url}/models/{model}:generateContent?key={api_key}"
                    
                    # Prepare parts with text prompt first
                    parts = [{"text": prompt}]

                    # Collect and append images if present
                    image_inputs = []
                    if image_1 is not None: image_inputs.append(("image_1", image_1))
                    if image_2 is not None: image_inputs.append(("image_2", image_2))
                    if image_3 is not None: image_inputs.append(("image_3", image_3))
                    
                    for key, value in kwargs.items():
                        if key.startswith("image_") and value is not None:
                            image_inputs.append((key, value))
                    
                    # Sort images by index
                    image_inputs.sort(key=lambda x: int(x[0].split("_")[1]) if "_" in x[0] else 999)

                    for name, img_tensor in image_inputs:
                        print(f"🖼️ [FeiMao-326 API Node] Adding {name} to payload...")
                        b64_img = self.tensor_to_base64_image(img_tensor)
                        parts.append({
                            "inline_data": {
                                "mime_type": "image/png",
                                "data": b64_img
                            }
                        })

                    payload = {
                        "contents": [{
                            "parts": parts
                        }]
                    }
                    
                    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, proxies=req_proxies)
                    
                    if response.status_code != 200:
                        raise Exception(f"Google API Error {response.status_code}: {response.text}")
                    
                    data = response.json()
                    # Parse structure: candidates[0].content.parts[0].inlineData.data
                    try:
                        # Gemini might return text + image or just image. We look for the image part.
                        cand_parts = data["candidates"][0]["content"]["parts"]
                        b64_img = None
                        
                        for p in cand_parts:
                            if "inlineData" in p:
                                b64_img = p["inlineData"]["data"]
                                break
                        
                        if b64_img:
                            generated_image_tensor = self.base64_to_tensor(b64_img)
                            response_text = "Image generated successfully via Google Gemini."
                        else:
                            raise Exception(f"No inlineData found in response parts. Parts keys: {[list(p.keys()) for p in cand_parts]}")
                            
                    except (KeyError, IndexError) as e:
                        raise Exception(f"Failed to parse Gemini image response: {str(e)}. Raw data: {str(data)[:200]}...")

            except Exception as e:
                return (f"Google Generation failed: {str(e)}", current_seed, generated_image_tensor)

        # BRANCH B: DALL-E Image Generation (via OpenAI API)
        elif is_dalle_model:
            print(f"🎨 [FeiMao-326 API Node] Detected DALL-E generation task...")
            try:
                response = client.images.generate(
                    model=model,
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                    response_format="b64_json"
                )
                
                if response.data:
                    b64_img = response.data[0].b64_json
                    generated_image_tensor = self.base64_to_tensor(b64_img)
                    response_text = response.data[0].revised_prompt or "Image generated successfully via DALL-E."
                else:
                     raise Exception("No data in DALL-E response.")
                     
            except Exception as e:
                 return (f"DALL-E Generation failed: {str(e)}", current_seed, generated_image_tensor)

        # BRANCH C: Chat Completion (Text-to-Text / Vision-to-Text)
        else:
            messages = [{"role": "system", "content": role}]
            user_content = [{"type": "text", "text": prompt}]
            
            has_images = False
            
            # Collect all image inputs
            image_inputs = []
            if image_1 is not None: image_inputs.append(("image_1", image_1))
            if image_2 is not None: image_inputs.append(("image_2", image_2))
            if image_3 is not None: image_inputs.append(("image_3", image_3))
            
            for key, value in kwargs.items():
                if key.startswith("image_") and value is not None:
                    image_inputs.append((key, value))
            
            # Sort images by index
            def get_image_index(name):
                try:
                    return int(name.split("_")[1])
                except (IndexError, ValueError):
                    return 999999
            
            image_inputs.sort(key=lambda x: get_image_index(x[0]))
            
            for name, img_tensor in image_inputs:
                try:
                    print(f"🖼️ [FeiMao-326 API Node] Processing {name}...")
                    base64_image = self.tensor_to_base64_image(img_tensor)
                    user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})
                    has_images = True
                except Exception as e:
                    return (f"Failed to process {name}: {type(e).__name__}: {str(e)}", current_seed, generated_image_tensor)
            
            messages.append({"role": "user", "content": user_content if has_images else prompt})
            
            response_text = ""
            try:
                print(f"🔵 [FeiMao-326 API Node] Calling model '{model}' at '{api_baseurl}'...")
                
                api_params = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }

                # Gemini's OpenAI compatibility layer does not support the 'seed' parameter
                if not is_gemini_native:
                    api_params["seed"] = current_seed
                
                if force_json_format:
                    api_params["response_format"] = { "type": "json_object" }
                
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
                    self.cleanup_ollama_model(api_baseurl, model)

                    if TORCH_AVAILABLE and torch.cuda.is_available():
                        print(f"🔵 [FeiMao-326 API Node] Clearing PyTorch GPU cache...")
                        torch.cuda.empty_cache()
                        torch.cuda.ipc_collect()
                        print(f"✅ [FeiMao-326 API Node] PyTorch GPU cache cleared.")
                elif cleanup_local_gpu and not is_local_ollama:
                    pass

        # --- 3. SEED CONTROL ---
        if control_after_generate == "increment":
            next_seed = current_seed + 1
        elif control_after_generate == "decrement":
            next_seed = current_seed - 1
        elif control_after_generate == "randomize":
            next_seed = secrets.randbits(64)
        else:
            next_seed = current_seed
            
        return (response_text, self._normalize_seed(next_seed), generated_image_tensor)
