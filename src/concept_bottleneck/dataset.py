import pathlib
import typing

import numpy as np
import numpy.typing as npt
from PIL import Image
from torch.utils.data import Dataset
from torchvision.datasets.folder import pil_loader
from torchvision.datasets.utils import download_and_extract_archive

TransformedT = typing.TypeVar("TransformedT")
TargetTransformedT = typing.TypeVar("TargetTransformedT")


URL = "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"
MD5 = "97eceeb196236b17998738112f37df78"
ROOT = pathlib.Path(__file__).parent.resolve() / "data"


class CUB200ImageToAttributes(Dataset[tuple[TransformedT, TargetTransformedT]]):
    def __init__(
        self,
        train: bool,
        download: bool = False,
        transform: typing.Callable[[Image.Image], TransformedT] = lambda x: x,
        target_transform: typing.Callable[
            [npt.NDArray[np.int_]], TargetTransformedT
        ] = lambda x: x,
    ):
        super().__init__()
        self._transform = transform
        self._target_transform = target_transform

        if download:
            download_and_extract_archive(url=URL, download_root=str(ROOT), md5=MD5)

        self._train_test_split = self._load_train_test_split()
        self._attributes = self._load_image_attribute_labels(train)
        self._image_paths = self._load_image_paths()

    def _load_train_test_split(self):
        filepath = ROOT / "CUB_200_2011" / "train_test_split.txt"
        return np.loadtxt(filepath, usecols=1, dtype=np.int_)

    def _load_image_attribute_labels(self, train: bool) -> npt.NDArray[np.int_]:
        filepath = ROOT / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"

        attributes = np.loadtxt(filepath, usecols=(0, 2), dtype=np.int_)
        grouped = groupby(attributes, col=0)
        return grouped[np.nonzero(self._train_test_split == train)]

    def _load_image_paths(self):
        filepath = ROOT / "CUB_200_2011" / "images.txt"
        with open(filepath, encoding="utf-8") as f:
            image_paths = tuple(line.split()[1] for line in f.readlines())
        return image_paths

    def __len__(self):
        return len(self._attributes)

    def __getitem__(self, idx: int) -> tuple[TransformedT, TargetTransformedT]:
        image_path = ROOT / "CUB_200_2011" / "images" / self._image_paths[idx]
        return (
            self._transform(pil_loader(str(image_path))),
            self._target_transform(self._attributes[idx]),
        )

    @property
    def num_attributes(self) -> int:
        return self._attributes.shape[1]


class CUB200AttributesToClass(Dataset[tuple[TransformedT, TargetTransformedT]]):
    def __init__(
        self,
        train: bool,
        download: bool = False,
        transform: typing.Callable[[npt.NDArray[np.int_]], TransformedT] = lambda x: x,
        target_transform: typing.Callable[
            [npt.NDArray[np.int_]], TargetTransformedT
        ] = lambda x: x,
    ):
        super().__init__()
        self._transform = transform
        self._target_transform = target_transform

        if download:
            download_and_extract_archive(url=URL, download_root=str(ROOT), md5=MD5)

        self._train_test_split = self._load_train_test_split()
        self._attributes = self._load_image_attribute_labels(train)
        self._classes = self._load_classes()

    def _load_train_test_split(self):
        filepath = ROOT / "CUB_200_2011" / "train_test_split.txt"
        return np.loadtxt(filepath, usecols=1, dtype=np.int_)

    def _load_image_attribute_labels(self, train: bool) -> npt.NDArray[np.int_]:
        filepath = ROOT / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"

        attributes = np.loadtxt(filepath, usecols=(0, 2), dtype=np.int_)
        grouped = groupby(attributes, col=0)
        return grouped[np.nonzero(self._train_test_split == train)]

    def _load_classes(self):
        filepath = ROOT / "CUB_200_2011" / "image_class_labels.txt"
        return np.loadtxt(filepath, usecols=1, dtype=np.int_)

    def __len__(self):
        return len(self._attributes)

    def __getitem__(self, idx: int) -> tuple[TransformedT, TargetTransformedT]:
        return (
            self._transform(self._attributes[idx]),
            self._target_transform(self._classes[idx]),
        )

    @property
    def num_attributes(self) -> int:
        return self._attributes.shape[1]


ScalarTypeT = typing.TypeVar("ScalarTypeT", bound=np.generic)


def groupby(arr: npt.NDArray[ScalarTypeT], col: int) -> npt.NDArray[ScalarTypeT]:
    return np.stack(
        np.split(arr[:, 1], np.unique(arr[:, col], return_index=True)[1][1:])
    )
