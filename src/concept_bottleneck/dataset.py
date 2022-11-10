import os
import pathlib

import numpy as np
from torchvision.datasets.utils import download_and_extract_archive

URL = "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"
MD5 = "97eceeb196236b17998738112f37df78"
ROOT = pathlib.Path(__file__).parent.resolve() / "data"


def download_and_extract():
    if not (ROOT / os.path.basename(URL)).exists():
        download_and_extract_archive(url=URL, download_root=str(ROOT), md5=MD5)


def load_train_test_split():
    filepath = ROOT / "CUB_200_2011" / "train_test_split.txt"
    data = np.loadtxt(filepath, dtype=np.int_)
    print(data)
