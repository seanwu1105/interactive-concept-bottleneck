import pytest
import torch


def test_is_torch_installed():
    x = torch.rand(5, 3)
    assert x.shape == (5, 3)


@pytest.mark.skip(reason="CI environment does not have CUDA")
def test_is_cuda_available():
    assert torch.cuda.is_available()
