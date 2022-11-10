import os
import pathlib

import numpy as np
import numpy.typing as npt
from torch.utils.data import Dataset
from torchvision.datasets.utils import download_and_extract_archive

URL = "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"
MD5 = "97eceeb196236b17998738112f37df78"
ROOT = pathlib.Path(__file__).parent.resolve() / "data"
DATA_PATH = ROOT / pathlib.Path(os.path.basename(URL)).stem

NUM_IMAGES = 11788
NUM_ATTRIBUTES = 312
NUM_CLASSES = 200


class CUB200AttributesToClass(Dataset[tuple[npt.NDArray[np.int_], np.int_]]):
    def __init__(self, train: bool, download: bool = True):
        super().__init__()
        if download:
            download_and_extract()

        train_test_split = load_train_test_split()
        self.image_class_labels = load_image_class_labels()[train_test_split == train]
        self.image_attribute_labels = load_image_attribute_labels()[
            train_test_split == train
        ]

    def __len__(self):
        return len(self.image_class_labels)

    def __getitem__(self, idx: int) -> tuple[npt.NDArray[np.int_], np.int_]:
        return (
            self.image_attribute_labels[idx],
            self.image_class_labels[idx],
        )


def download_and_extract():
    if not DATA_PATH.exists():
        download_and_extract_archive(url=URL, download_root=str(ROOT), md5=MD5)


def load_train_test_split():
    filepath = DATA_PATH / "train_test_split.txt"
    return np.loadtxt(filepath, usecols=1, dtype=np.int_)


def load_image_attribute_labels():
    filepath = DATA_PATH / "attributes" / "image_attribute_labels.txt"
    labels = np.loadtxt(filepath, usecols=2, dtype=np.int_)
    return labels.reshape((NUM_IMAGES, NUM_ATTRIBUTES))


def load_image_class_labels():
    filepath = DATA_PATH / "image_class_labels.txt"
    return np.loadtxt(filepath, usecols=1, dtype=np.int_)
