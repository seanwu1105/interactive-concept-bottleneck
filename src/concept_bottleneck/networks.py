import torch
from torchvision.ops import MLP

from src.concept_bottleneck.dataset import NUM_ATTRIBUTES, NUM_CLASSES


def get_inception() -> torch.nn.Module:
    model = torch.hub.load(
        "pytorch/vision:v0.10.0",
        "inception_v3",
        weights="IMAGENET1K_V1",
    )

    model.AuxLogits.fc = torch.nn.Linear(in_features=768, out_features=NUM_ATTRIBUTES)
    model.fc = torch.nn.Linear(in_features=2048, out_features=NUM_ATTRIBUTES)

    return model


def get_mlp() -> torch.nn.Module:
    return MLP(in_channels=NUM_ATTRIBUTES, hidden_channels=[NUM_CLASSES])
