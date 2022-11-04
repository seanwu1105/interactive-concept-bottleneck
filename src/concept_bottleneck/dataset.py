import pathlib

from torch.utils.data import Dataset
from torchvision.datasets.utils import download_and_extract_archive


class CUB200_2011(Dataset[tuple[int, int]]):  # pylint: disable=invalid-name
    url = "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"

    def __init__(self, root: str = "data"):
        super().__init__()
        self.root = pathlib.Path(__file__).parent.resolve() / root

        download_and_extract_archive(url=self.url, download_root=str(self.root))

        self._load_image_attribute_labels()

    def _load_image_attribute_labels(self):
        filepath = (
            self.root / "CUB_200_2011" / "attributes" / "image_attribute_labels.txt"
        )
        print(filepath)

    def __len__(self):
        return 0

    def __getitem__(self, idx: int):
        return (idx, idx)
