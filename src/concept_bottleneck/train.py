import pathlib
import typing

import torch
from torch.utils.data import DataLoader

MODEL_PATH = pathlib.Path(__file__).parent.resolve() / "models"

TrainFn = typing.Callable[[torch.nn.Module], None]
TestFn = typing.Callable[[torch.nn.Module, DataLoader[typing.Any]], tuple[float, float]]


def run_epochs(  # pylint: disable=too-many-arguments
    epochs: int,
    model: torch.nn.Module,
    train: TrainFn,
    test: TestFn,
    training_dataloader: DataLoader[typing.Any],
    test_dataloader: DataLoader[typing.Any],
    save_name: str | None = None,
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
            if save_name is not None:
                print(
                    f"Saving model to {save_name} with accuracy {100 * best_acc:>0.4f}%"
                )
                torch.save(best_model, MODEL_PATH / save_name)

    print(f"Best Test Accuracy: {100 * best_acc:>0.4f}%")

    return best_model
