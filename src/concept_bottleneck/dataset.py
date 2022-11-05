import pathlib
import typing

import numpy as np
import numpy.typing as npt
from PIL import Image
from torch.utils.data import Dataset
from torchvision.datasets.folder import pil_loader
from torchvision.datasets.utils import download_and_extract_archive


class CUB200_2011(
    Dataset[tuple[npt.NDArray[np.int_], Image.Image]]
):  # pylint: disable=invalid-name
    url = "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"
    md5 = "97eceeb196236b17998738112f37df78"
    root = pathlib.Path(__file__).parent.resolve() / "data"

    def __init__(self, train: bool = True, download: bool = True):
        super().__init__()

        if download:
            download_and_extract_archive(
                url=self.url, download_root=str(self.root), md5=self.md5
            )

        self._train_test_split = self._load_train_test_split()
        self._attributes = self._load_image_attribute_labels(train)
        self._image_paths = self._load_image_paths()

    def _load_train_test_split(self):
        filepath = self.root / "CUB_200_2011" / "train_test_split.txt"
        return np.loadtxt(filepath, usecols=1, dtype=np.int_)

    def _load_image_attribute_labels(self, train: bool) -> npt.NDArray[np.int_]:
        filepath = (
            self.root / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"
        )

        attributes = np.loadtxt(filepath, usecols=(0, 2), dtype=np.int_)
        grouped = groupby(attributes, col=0)
        return grouped[np.nonzero(self._train_test_split == train)]

    def _load_image_paths(self):
        filepath = self.root / "CUB_200_2011" / "images.txt"
        with open(filepath, encoding="utf-8") as f:
            image_paths = tuple(line.split()[1] for line in f.readlines())
        return image_paths

    def __len__(self):
        return len(self._attributes)

    def __getitem__(self, idx: int) -> tuple[npt.NDArray[np.int_], Image.Image]:
        image_path = self.root / "CUB_200_2011" / "images" / self._image_paths[idx]
        return (self._attributes[idx], pil_loader(str(image_path)))


ScalarTypeT = typing.TypeVar("ScalarTypeT", bound=np.generic)


def groupby(arr: npt.NDArray[ScalarTypeT], col: int) -> npt.NDArray[ScalarTypeT]:
    return np.stack(
        np.split(arr[:, 1], np.unique(arr[:, col], return_index=True)[1][1:])
    )
