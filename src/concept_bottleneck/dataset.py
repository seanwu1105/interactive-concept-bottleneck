import pathlib

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

    def __init__(self, root: str = "data"):
        super().__init__()
        self.root = pathlib.Path(__file__).parent.resolve() / root
        self.attribute_data: npt.NDArray[np.int_]
        self.image_paths: dict[int, str]

        download_and_extract_archive(url=self.url, download_root=str(self.root))

        self._load_image_attribute_labels()
        self._load_image_paths()

    def _load_image_attribute_labels(self):
        filepath = (
            self.root / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"
        )

        # Only load the image ID, attribute ID and whether the attribute is present.
        self.attribute_data = np.loadtxt(filepath, usecols=(0, 2), dtype=np.int_)

    def _load_image_paths(self):
        filepath = self.root / "CUB_200_2011" / "images.txt"
        with open(filepath, encoding="utf-8") as f:
            self.image_paths = {
                int(line.split()[0]): line.split()[1] for line in f.readlines()
            }

    def __len__(self):
        return len(np.unique(self.attribute_data[:, 0]))  # type: ignore

    def __getitem__(self, idx: int):
        image_id = idx + 1

        # Assume the attribute ID is sorted.
        concept: npt.NDArray[np.int_] = self.attribute_data[
            self.attribute_data[:, 0] == image_id, 1
        ]

        image_path = self.root / "CUB_200_2011" / "images" / self.image_paths[image_id]

        return (concept, pil_loader(str(image_path)))
