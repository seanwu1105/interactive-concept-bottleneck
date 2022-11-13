import urllib.parse

import torch
from torchvision.datasets.folder import pil_loader

from src.concept_bottleneck.dataset import (
    DEFAULT_IMAGE_TRANSFORM,
    NUM_ATTRIBUTES,
    load_attribute_names,
)
from src.concept_bottleneck.train import MODEL_PATH


class ImageToAttributesModel:
    def __init__(self):
        self.model: torch.nn.Module | None = None

    def predict(self, image_uri: str) -> dict[str, float]:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.model is None:
            self.model = load_image_to_attributes_model(device)

        path = urllib.parse.unquote(urllib.parse.urlparse(image_uri).path)

        image: torch.Tensor = DEFAULT_IMAGE_TRANSFORM(pil_loader(path))  # type: ignore
        image_batch = image.unsqueeze(0)
        logits = self.model(image_batch.to(device))
        probabilities = torch.sigmoid(logits)[0]
        attribute_names = load_attribute_names()

        return {
            attribute_name: probability.item()
            for attribute_name, probability in zip(attribute_names, probabilities)
        }


def load_image_to_attributes_model(device: str) -> torch.nn.Module:
    model: torch.nn.Module = torch.hub.load(
        "pytorch/vision:v0.10.0",
        "inception_v3",
        init_weights=False,
        num_classes=NUM_ATTRIBUTES,
    )

    model.load_state_dict(torch.load(MODEL_PATH / "image-to-attributes.pth"))

    model = model.to(device)
    model.eval()
    return model
