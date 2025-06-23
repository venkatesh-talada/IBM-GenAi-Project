from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv
from huggingface_hub import login
from datetime import datetime

# Load environment variables
load_dotenv()

# Flask App
app = Flask(__name__)
CORS(app)

# Global model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the IBM Granite model"""
    global model, tokenizer

    try:
        print("Logging into Hugging Face Hub...")
        login(os.getenv("HUGGINGFACE_API_TOKEN"))

        model_name = "ibm-granite/granite-3.3-2b-instruct"
        print("Loading model:", model_name)

        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )

        print("Model loaded successfully.")
        return True

    except Exception as e:
        print("Error loading model:", e)
        return False

def generate_response(prompt, max_length=2048, temperature=0.7):
    if model is None or tokenizer is None:
        return {"error": "Model not loaded."}

    try:
        formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
        inputs = tokenizer(formatted_prompt, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("<|assistant|>\n")[-1].strip()

        if not response:
            return {"error": "Empty response from model."}

        return {"response": response}

    except Exception as e:
        return {"error": f"Generation error: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        language = data.get("language", "python")
        max_length = int(data.get("max_length", 1024))
        temperature = float(data.get("temperature", 0.7))

        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400

        final_prompt = f"""Generate {language} code based on the following requirements:\n\n{prompt}\n\nPlease provide:\n1. Complete, working code\n2. Comments\n3. Imports\n4. Example usage"""

        result = generate_response(final_prompt, max_length, temperature)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500

@app.route('/api/debug', methods=['POST'])
def debug_code():
    try:
        data = request.get_json()
        code = data.get("code", "")
        language = data.get("language", "python")

        if not code:
            return jsonify({"error": "Code is required."}), 400

        prompt = f"""Analyze the following {language} code for bugs and improvements:\n```{language}\n{code}\n```\nGive syntax errors, logic issues, and suggestions."""

        result = generate_response(prompt, max_length=1024, temperature=0.3)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Debug error: {str(e)}"}), 500

@app.route('/api/explain', methods=['POST'])
def explain_code():
    try:
        data = request.get_json()
        code = data.get("code", "")
        language = data.get("language", "python")

        if not code:
            return jsonify({"error": "Code is required."}), 400

        prompt = f"""Explain this {language} code step by step:\n```{language}\n{code}\n```"""

        result = generate_response(prompt, max_length=1024, temperature=0.3)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Explain error: {str(e)}"}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_code():
    try:
        data = request.get_json()
        code = data.get("code", "")
        language = data.get("language", "python")

        if not code:
            return jsonify({"error": "Code is required."}), 400

        prompt = f"""Optimize the following {language} code:\n```{language}\n{code}\n```\nGive performance improvements and a better version."""

        result = generate_response(prompt, max_length=1024, temperature=0.3)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Optimize error: {str(e)}"}), 500

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "tokenizer_loaded": tokenizer is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    if load_model():
        print("Starting Flask server on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model.")
