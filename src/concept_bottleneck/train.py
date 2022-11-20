import pathlib
import typing

import torch
from torch.utils.data import DataLoader

MODEL_PATH = pathlib.Path(__file__).parent.resolve() / "models"

TrainFn = typing.Callable[[torch.nn.Module], None]
TestFn = typing.Callable[[torch.nn.Module, DataLoader[typing.Any]], tuple[float, float]]

M = typing.TypeVar("M", bound=torch.nn.Module)


def run_epochs(  # pylint: disable=too-many-arguments
    epochs: int,
    model: M,
    train: TrainFn,
    test: TestFn,
    training_dataloader: DataLoader[typing.Any],
    test_dataloader: DataLoader[typing.Any],
    on_better_accuracy: typing.Callable[[M, float], None],
):
    best_acc = 0.0
    best_model = None

    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}/{epochs}-------------------")

        train(model)

        training_loss, training_acc = test(model, training_dataloader)
        print(
            f"Training Loss: {training_loss:.4f}, Training Accuracy: {100 * training_acc:>0.4f}%"
        )

        test_loss, test_acc = test(model, test_dataloader)
        print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {100 * test_acc:>0.4f}%")

        if test_acc > best_acc:
            best_acc = test_acc
            best_model = model.state_dict()
            on_better_accuracy(model, best_acc)

    print(f"Best Test Accuracy: {100 * best_acc:>0.4f}%")

    return best_model
