import numpy as np
import numpy.typing as npt
import pytest

from src.concept_bottleneck.dataset import ROOT, download_and_extract

download_and_extract()


class TestTrainTestSplit:
    class TestImageIds:
        def test_sorted(self, image_ids: npt.NDArray[np.int_]):
            assert np.all(np.diff(image_ids) == 1)

        def test_start_at_1(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids[0] == 1

        def test_end_at_11788(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids[-1] == 11788

        @pytest.fixture
        def image_ids(self, train_test_split: npt.NDArray[np.int_]):
            return train_test_split[:, 0]

    class TestSplits:
        def test_contain_binary_only(self, splits: npt.NDArray[np.int_]):
            assert np.all(np.isin(splits, (0, 1)))

        @pytest.fixture
        def splits(self, train_test_split: npt.NDArray[np.int_]):
            return train_test_split[:, 1]

    @pytest.fixture
    def train_test_split(self):
        filepath = ROOT / "CUB_200_2011" / "train_test_split.txt"
        return np.loadtxt(filepath, dtype=np.int_)
