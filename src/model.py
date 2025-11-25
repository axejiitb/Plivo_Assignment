from transformers import AutoModelForTokenClassification, AutoConfig
from labels import LABEL2ID, ID2LABEL
import torch


def create_model(
    model_name: str,
    freeze_layers: int = 0,
    dropout: float = 0.1,
    quantize: bool = False
):
    """
    model_name   – HF model
    freeze_layers – number of encoder layers to freeze (0–4)
    dropout      – classifier + encoder dropout
    quantize     – dynamic quantization (CPU only)
    """

    # Add dropout + label mapping
    config = AutoConfig.from_pretrained(
        model_name,
        num_labels=len(LABEL2ID),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
        hidden_dropout_prob=dropout,
        attention_probs_dropout_prob=dropout,
    )

    model = AutoModelForTokenClassification.from_pretrained(model_name, config=config)

    if freeze_layers > 0:
        if hasattr(model, "distilbert"):
            for i in range(min(freeze_layers, len(model.distilbert.transformer.layer))):
                for p in model.distilbert.transformer.layer[i].parameters():
                    p.requires_grad = False

    if quantize:
        model = torch.quantization.quantize_dynamic(
            model,
            {torch.nn.Linear},
            dtype=torch.qint8,
        )

    return model
