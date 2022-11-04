import random

from src.concept_bottleneck.dataset import CUB200_2011

dataset = CUB200_2011()


def test_dataset_has_11788_images():
    assert len(dataset) == 11788


def test_dataset_has_312_attributes_per_image():
    concept, _ = dataset[random.randint(0, len(dataset) - 1)]
    assert len(concept) == 312
