import torch
from torchvision.ops import MLP

from src.concept_bottleneck.dataset import NUM_ATTRIBUTES, NUM_CLASSES


def get_inception() -> torch.nn.Module:
    return torch.hub.load(
        "pytorch/vision:v0.10.0",
        "inception_v3",
        init_weights=False,
        num_classes=NUM_ATTRIBUTES,
    )


def get_mlp() -> torch.nn.Module:
    return MLP(in_channels=NUM_ATTRIBUTES, hidden_channels=[NUM_CLASSES])
