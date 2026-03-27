---
name: ml-deep-learning
description: Use for training and fine-tuning deep learning models, including LLMs, Vision, and Audio transformers. Unified guide for PyTorch Lightning (scalable training) and Transformers (Hugging Face). CRITICAL: Run `get-available-resources` first to detect GPUs and CUDA availability.
---
# Deep Learning & Transformers (Consolidated)

Unified expert guide for scalable deep learning and foundation model fine-tuning.

## ⚠️ Mandatory Pre-flight: Compute & Precision

1. **GPU Detection**: Check CUDA availability and VRAM size before training.
2. **Mixed Precision**: Use `fp16` or `bf16` to reduce memory and speed up training on modern GPUs.
3. **Reproducibility**: Set seeds for PyTorch, NumPy, and Transformers.

---

## 1. PyTorch Lightning (Scalable Training)

Use for organizing PyTorch code into scalable, reproducible modules.

### Core Idioms
- **LightningModule**: Decouple the model architecture from the training loop.
- **Callbacks**: Use built-in callbacks for checkpointing, early stopping, and logging.
- **DataModule**: Encapsulate all data-related logic (loading, splitting, transforms).

```python
import lightning as L
from torch import nn

class MyModel(L.LightningModule):
    def __init__(self, model):
        super().__init__()
        self.model = model
    def training_step(self, batch, batch_idx):
        # Training logic here...
        return loss
```

---

## 2. Transformers (Hugging Face)

Use for working with state-of-the-art NLP, Vision, and Audio transformer models.

### Core Tools
- **AutoModel/AutoTokenizer**: Use the "Auto" classes for flexible model loading.
- **PEFT/LoRA**: Use Parameter-Efficient Fine-Tuning for LLMs with limited VRAM.
- **Datasets**: Use the `datasets` library for efficient data streaming and mapping.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

---

## 🛠️ Common Pitfalls (The "Wall of Shame")

1. **OOM (Out of Memory)**: Setting a batch size that exceeds VRAM; use gradient accumulation instead.
2. **Untrained Tokenizer**: Forgetting to add special tokens or resize the embedding layer.
3. **Silently Catching CUDA Errors**: Not properly handling device errors, leading to hung processes.

## References
- `skills/machine-learning/ml-deep-learning/references/pytorch-lightning/` — Distributed training and callbacks.
- `skills/machine-learning/ml-deep-learning/references/transformers/` — Tokenization and model architecture.
