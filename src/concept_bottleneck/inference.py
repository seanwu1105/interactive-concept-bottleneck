import urllib.parse

import torch
from torchvision.datasets.folder import pil_loader

from src.concept_bottleneck.dataset import (
    DEFAULT_IMAGE_TRANSFORM,
    load_attribute_names,
    load_class_names,
)
from src.concept_bottleneck.networks import get_inception, get_mlp
from src.concept_bottleneck.train import MODEL_PATH

INDEPENDENT_IMAGE_TO_ATTRIBUTES_MODEL_NAME = "independent_image_to_attributes.pth"
INDEPENDENT_ATTRIBUTES_TO_CLASS_MODEL_NAME = "independent_attributes_to_class.pth"
SEQUENTIAL_ATTRIBUTES_TO_CLASS_MODEL_NAME = "sequential_attributes_to_class.pth"
JOINT_IMAGE_TO_ATTRIBUTES_MODEL_NAME = "joint_image_to_attributes.pth"
JOINT_ATTRIBUTES_TO_CLASS_MODEL_NAME = "joint_attributes_to_class.pth"


class ImageToAttributesModel:
    def __init__(self):
        self.model_name: str | None = None
        self.model: torch.nn.Module | None = None

    def predict(self, model_name: str, image_uri: str) -> dict[str, float]:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.model is None or self.model_name != model_name:
            self.model_name = model_name
            self.model = load_image_to_attributes_model(model_name, device)

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


def load_image_to_attributes_model(name: str, device: str) -> torch.nn.Module:
    model = get_inception()

    model.load_state_dict(torch.load(MODEL_PATH / name))

    model = model.to(device)
    model.eval()
    return model


class AttributesToClassModel:
    def __init__(self):
        self.model_name: str | None = None
        self.model: torch.nn.Module | None = None

    def predict(self, model_name: str, attributes: list[float]):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.model is None or self.model_name != model_name:
            self.model_name = model_name
            self.model = load_attributes_to_class_model(model_name, device)

        class_batch = torch.tensor([attributes]).to(device)
        logits = self.model(class_batch)  # pylint: disable=not-callable
        probabilities = torch.softmax(logits, dim=1)[0]
        class_names = load_class_names()

        return {
            class_name: probability.item()
            for class_name, probability in zip(class_names, probabilities)
        }


def load_attributes_to_class_model(name: str, device: str) -> torch.nn.Module:
    model = get_mlp()

    model.load_state_dict(torch.load(MODEL_PATH / name))

    model = model.to(device)
    model.eval()
    return model
