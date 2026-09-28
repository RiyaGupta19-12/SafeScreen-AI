from transformers import AutoTokenizer
from huggingface_hub import snapshot_download
import onnxruntime as ort
import numpy as np
import os

MODEL_NAME = "onnx-community/bert-small-phishing-ONNX"

# Download model files if they are not already downloaded
model_path = snapshot_download(
    repo_id=MODEL_NAME,
    allow_patterns=[
        "onnx/model_quantized.onnx",
        "tokenizer.json",
        "tokenizer_config.json",
        "config.json",
        "special_tokens_map.json",
        "vocab.txt"
    ]
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Locate ONNX model
onnx_file = os.path.join(
    model_path,
    "onnx",
    "model_quantized.onnx"
)
available = ort.get_available_providers()

if "QNNExecutionProvider" in available:
    providers = ["QNNExecutionProvider", "CPUExecutionProvider"]
else:
    providers = ["CPUExecutionProvider"]

print(providers)

# Load ONNX model
session = ort.InferenceSession(
    onnx_file,
    providers=providers
    )

def predict_phishing(text):

    inputs = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
        max_length=512
    )

    model_inputs = {}

    for inp in session.get_inputs():
        if inp.name in inputs:
            model_inputs[inp.name] = inputs[inp.name]

    outputs = session.run(None, model_inputs)

    logits = outputs[0][0]

    # Convert logits to probabilities
    exp_values = np.exp(logits - np.max(logits))
    probabilities = exp_values / exp_values.sum()

    safe_probability = float(probabilities[0])
    phishing_probability = float(probabilities[1])

    if phishing_probability > safe_probability:
        prediction = "PHISHING"
    else:
        prediction = "SAFE"

    return prediction, safe_probability, phishing_probability