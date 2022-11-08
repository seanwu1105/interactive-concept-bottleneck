import random

import numpy as np

from src.concept_bottleneck.dataset import (
    ROOT,
    CUB200AttributesToClass,
    CUB200ImageToAttributes,
)

CUB200AttributesToClass(train=True)  # download the dataset


def test_cub200_2011_attributes_image_ids_are_sorted():
    filepath = ROOT / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"

    attributes = np.loadtxt(filepath, usecols=0, dtype=np.int_)
    assert np.all(np.diff(attributes) >= 0)


def test_cub200_2011_attributes_ids_are_sorted():
    filepath = ROOT / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"

    attributes = np.loadtxt(filepath, usecols=(0, 1), dtype=np.int_)
    image_ids = np.unique(attributes[:, 0])

    # Randomly select some image IDs for performance reasons.
    for image_id in np.random.choice(image_ids, size=100, replace=False):
        attribute_ids = attributes[attributes[:, 0] == image_id, 1]
        assert np.all(np.diff(attribute_ids) >= 0)


def test_cub200_2011_train_test_split_image_ids_are_sorted():
    filepath = ROOT / "CUB_200_2011" / "train_test_split.txt"
    train_test_split = np.loadtxt(filepath, usecols=0, dtype=np.int_)
    assert np.all(np.diff(train_test_split) >= 0)


def test_cub200_2011_image_class_labels_image_ids_are_sorted():
    filepath = ROOT / "CUB_200_2011" / "image_class_labels.txt"
    image_class_labels = np.loadtxt(filepath, usecols=0, dtype=np.int_)
    assert np.all(np.diff(image_class_labels) >= 0)


def test_cub200_2011_train_size():
    assert (
        len(CUB200ImageToAttributes(train=True))
        == len(CUB200AttributesToClass(train=True))
        == 5994
    )


def test_cub200_2011_test_size():
    assert (
        len(CUB200ImageToAttributes(train=False))
        == len(CUB200AttributesToClass(train=False))
        == 5794
    )


def test_cub200_2011_num_classes():
    assert (
        CUB200AttributesToClass(train=True).num_classes
        == CUB200AttributesToClass(train=False).num_classes
        == 200
    )


def test_cub200_image_to_attributes_getitem():
    dataset = CUB200ImageToAttributes(train=True)

    for _ in range(100):
        idx = random.randint(0, len(dataset) - 1)
        image, attributes = dataset[idx]
        assert attributes.shape == (312,)
        assert image is not None


def test_cub200_attributes_to_class_getitem():
    dataset = CUB200AttributesToClass(train=True)

    for _ in range(500):
        idx = random.randint(0, len(dataset) - 1)
        attributes, label = dataset[idx]
        assert attributes.shape == (312,)
        assert 1 <= label <= 200
