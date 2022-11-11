import numpy as np
import numpy.typing as npt
import pytest

from src.concept_bottleneck.dataset import (
    DATA_PATH,
    NUM_ATTRIBUTES,
    NUM_CLASSES,
    NUM_IMAGES,
    CUB200AttributesToClass,
    CUB200ImageToAttributes,
    calibrate_image_attribute_labels,
    download_and_extract,
    load_image_attribute_labels,
    load_image_class_labels,
    load_image_paths,
    load_train_test_split,
)

download_and_extract()


def test_download_and_extract():
    download_and_extract()
    assert DATA_PATH.exists()


class TestCUB200ImageToAttributes:
    class TestTrainingDataset:
        @pytest.fixture
        def dataset(self):
            return CUB200ImageToAttributes(train=True)

        def test_len(self, dataset: CUB200ImageToAttributes):
            assert len(dataset) == 5994

        def test_getitem(self, dataset: CUB200ImageToAttributes):
            image, attributes = dataset[0]
            assert image.shape == (3, 299, 299)
            assert attributes.shape == (NUM_ATTRIBUTES,)

    class TestTestDataset:
        @pytest.fixture
        def dataset(self):
            return CUB200ImageToAttributes(train=False)

        def test_len(self, dataset: CUB200ImageToAttributes):
            assert len(dataset) == 5794

        def test_getitem(self, dataset: CUB200ImageToAttributes):
            image, attributes = dataset[0]
            assert image.shape == (3, 299, 299)
            assert attributes.shape == (NUM_ATTRIBUTES,)


class TestCUB200AttributesToClass:
    class TestTrainingDataset:
        @pytest.fixture
        def dataset(self):
            return CUB200AttributesToClass(train=True)

        def test_len(self, dataset: CUB200AttributesToClass):
            assert len(dataset) == 5994

        def test_getitem(self, dataset: CUB200AttributesToClass):
            attributes, class_label = dataset[0]
            assert attributes.shape == (NUM_ATTRIBUTES,)
            assert attributes.dtype == np.float32
            assert np.all((attributes >= 0) & (attributes <= 1))
            assert class_label == 1 - 1

    class TestTestDataset:
        @pytest.fixture
        def dataset(self):
            return CUB200AttributesToClass(train=False)

        def test_len(self, dataset: CUB200AttributesToClass):
            assert len(dataset) == 5794

        def test_getitem(self, dataset: CUB200AttributesToClass):
            attributes, class_label = dataset[0]
            assert attributes.shape == (NUM_ATTRIBUTES,)
            assert attributes.dtype == np.float32
            assert np.all((attributes >= 0) & (attributes <= 1))
            assert class_label == 1 - 1


class TestTrainTestSplit:
    class TestImageIds:
        def test_sorted(self, image_ids: npt.NDArray[np.int_]):
            assert np.all(np.diff(image_ids) == 1)

        def test_start_at(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids[0] == 1

        def test_end_at(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids[-1] == NUM_IMAGES

        @pytest.fixture
        def image_ids(self, train_test_split: npt.NDArray[np.int_]):
            return train_test_split[:, 0]

    class TestSplits:
        def test_contain_binary_only(self, splits: npt.NDArray[np.int_]):
            assert np.all(np.isin(splits, (0, 1)))

        @pytest.fixture
        def splits(self, train_test_split: npt.NDArray[np.int_]):
            return train_test_split[:, 1]

    def test_shape(self, train_test_split: npt.NDArray[np.int_]):
        assert train_test_split.shape == (NUM_IMAGES, 2)

    @pytest.fixture
    def train_test_split(self):
        filepath = DATA_PATH / "train_test_split.txt"
        return np.loadtxt(filepath, dtype=np.int_)


def test_load_train_test_split():
    train_test_split = load_train_test_split()
    assert train_test_split.shape == (NUM_IMAGES,)
    assert train_test_split.dtype == np.int_
    assert np.all(np.isin(train_test_split, (0, 1)))


class TestImageAttributeLabels:
    class TestImageIds:
        def test_sorted(self, image_ids: npt.NDArray[np.int_]):
            for image_id in range(1, NUM_IMAGES + 1):
                for attribute_id in range(1, NUM_ATTRIBUTES + 1):
                    assert (
                        image_ids[(image_id - 1) * NUM_ATTRIBUTES + (attribute_id - 1)]
                        == image_id
                    )

        def test_shape(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids.shape == (NUM_IMAGES * NUM_ATTRIBUTES,)

        @pytest.fixture
        def image_ids(self, image_attribute_labels: npt.NDArray[np.int_]):
            return image_attribute_labels[:, 0]

    class TestAttributeIds:
        def test_sorted(self, attribute_ids: npt.NDArray[np.int_]):
            for image_id in range(1, NUM_IMAGES + 1):
                for attribute_id in range(1, NUM_ATTRIBUTES + 1):
                    assert (
                        attribute_ids[
                            (image_id - 1) * NUM_ATTRIBUTES + (attribute_id - 1)
                        ]
                        == attribute_id
                    )

        def test_shape(self, attribute_ids: npt.NDArray[np.int_]):
            assert attribute_ids.shape == (NUM_IMAGES * NUM_ATTRIBUTES,)

        @pytest.fixture
        def attribute_ids(self, image_attribute_labels: npt.NDArray[np.int_]):
            return image_attribute_labels[:, 1]

    class TestLabels:
        def test_contain_binary_only(self, labels: npt.NDArray[np.int_]):
            assert np.all(np.isin(labels, (0, 1)))

        def test_shape(self, labels: npt.NDArray[np.int_]):
            assert labels.shape == (NUM_IMAGES * NUM_ATTRIBUTES,)

        @pytest.fixture
        def labels(self, image_attribute_labels: npt.NDArray[np.int_]):
            return image_attribute_labels[:, 2]

    class TestCertainties:
        def test_contain_certainty_only(self, certainty: npt.NDArray[np.int_]):
            assert np.all(np.isin(certainty, (1, 2, 3, 4)))

        def test_shape(self, certainty: npt.NDArray[np.int_]):
            assert certainty.shape == (NUM_IMAGES * NUM_ATTRIBUTES,)

        @pytest.fixture
        def certainty(self, image_attribute_labels: npt.NDArray[np.int_]):
            return image_attribute_labels[:, 3]

    def test_shape(self, image_attribute_labels: npt.NDArray[np.int_]):
        assert image_attribute_labels.shape == (NUM_IMAGES * NUM_ATTRIBUTES, 4)

    @pytest.fixture
    def image_attribute_labels(self):
        filepath = DATA_PATH / "attributes" / "image_attribute_labels.txt"
        return np.loadtxt(filepath, usecols=(0, 1, 2, 3), dtype=np.int_)


def test_calibrate_image_attribute_labels():
    arr = np.array([[0, 1], [0, 2], [0, 3], [0, 4], [1, 1], [1, 2], [1, 3], [1, 4]])
    calibrated = calibrate_image_attribute_labels(arr[:, 0], arr[:, 1])
    assert np.all(calibrated == np.array([0.5, 0.25, 0, 0, 0.5, 0.75, 1, 1]))


def test_load_image_attribute_labels():
    image_attribute_labels = load_image_attribute_labels()
    assert image_attribute_labels.shape == (NUM_IMAGES, NUM_ATTRIBUTES)
    assert image_attribute_labels.dtype == np.float32
    assert np.all((image_attribute_labels >= 0) & (image_attribute_labels <= 1))

    # Pick some random images and attributes to check that the labels are correct.
    assert image_attribute_labels[(2410 - 1), (30 - 1)] == 1
    assert image_attribute_labels[(9487 - 1), (245 - 1)] == 1
    assert image_attribute_labels[(11662 - 1), (26 - 1)] == 1


class TestImageClassLabels:
    class TestImageIds:
        def test_sorted(self, image_ids: npt.NDArray[np.int_]):
            assert np.all(np.diff(image_ids) == 1)

        def test_start_at(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids[0] == 1

        def test_end_at(self, image_ids: npt.NDArray[np.int_]):
            assert image_ids[-1] == NUM_IMAGES

        @pytest.fixture
        def image_ids(self, image_class_labels: npt.NDArray[np.int_]):
            return image_class_labels[:, 0]

    class TestClasses:
        def test_contain_class_only(self, classes: npt.NDArray[np.int_]):
            assert np.all((classes >= 1) & (classes <= NUM_CLASSES))

        @pytest.fixture
        def classes(self, image_class_labels: npt.NDArray[np.int_]):
            return image_class_labels[:, 1]

    def test_shape(self, image_class_labels: npt.NDArray[np.int_]):
        assert image_class_labels.shape == (NUM_IMAGES, 2)

    @pytest.fixture
    def image_class_labels(self):
        filepath = DATA_PATH / "image_class_labels.txt"
        return np.loadtxt(filepath, dtype=np.int_)


def test_load_image_class_labels():
    image_class_labels = load_image_class_labels()
    assert image_class_labels.shape == (NUM_IMAGES,)
    assert image_class_labels.dtype == np.int_
    assert np.all((image_class_labels >= 1) & (image_class_labels <= NUM_CLASSES))


class TestImagePaths:
    class TestImageIds:
        def test_sorted(self, image_ids: list[int]):
            assert np.all(np.diff(image_ids) == 1)

        def test_start_at(self, image_ids: list[int]):
            assert image_ids[0] == 1

        def test_end_at(self, image_ids: list[int]):
            assert image_ids[-1] == NUM_IMAGES

        @pytest.fixture
        def image_ids(self, image_paths: list[tuple[int, str]]):
            return [image_id for image_id, _ in image_paths]

    def test_shape(self, image_paths: list[tuple[int, str]]):
        assert len(image_paths) == NUM_IMAGES

    @pytest.fixture
    def image_paths(self):
        filepath = DATA_PATH / "images.txt"

        paths: list[tuple[int, str]] = []
        with open(filepath, encoding="utf-8") as f:
            for line in f.readlines():
                image_id, path = line.split()
                paths.append((int(image_id), path))
        return paths


def test_load_image_paths():
    image_paths = load_image_paths()
    assert len(image_paths) == NUM_IMAGES
    assert (
        image_paths[0]
        == "001.Black_footed_Albatross/Black_Footed_Albatross_0046_18.jpg"
    )
