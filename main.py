import json
import sys

import numpy as np
import torch
from torch.utils.data import DataLoader
from torchvision.ops import MLP

from src.concept_bottleneck.dataset import CUB200AttributesToClass

training_data: CUB200AttributesToClass[torch.Tensor, np.int_] = CUB200AttributesToClass(
    train=True,
    transform=torch.from_numpy,  # type: ignore
    target_transform=lambda x: x - 1,  # from 1-indexed to 0-indexed
)
test_data: CUB200AttributesToClass[torch.Tensor, np.int_] = CUB200AttributesToClass(
    train=False,
    transform=torch.from_numpy,  # type: ignore
    target_transform=lambda x: x - 1,  # from 1-indexed to 0-indexed
)


def train(
    dataloader: DataLoader[tuple[torch.Tensor, np.int_]],
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: str,
):
    size = len(dataloader.dataset)  # type: ignore
    model.train()
    for batch, (X, y) in enumerate(dataloader):  # pylint: disable=invalid-name
        X, y = X.to(torch.float).to(device), y.to(device)  # type: ignore # pylint: disable=invalid-name

        logits = model(X)
        loss = loss_fn(logits, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 1000 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(
    dataloader: DataLoader[tuple[torch.Tensor, np.int_]],
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    device: str,
):
    size = len(dataloader.dataset)  # type: ignore
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:  # pylint: disable=invalid-name
            X, y = X.to(torch.float).to(device), y.to(device)  # type: ignore # pylint: disable=invalid-name
            logits = model(X)
            test_loss += loss_fn(logits, y).item()
            correct += (torch.argmax(logits, dim=1) == y).sum().item()
    test_loss /= num_batches
    accuracy = correct / size
    return test_loss, accuracy


def save_model(model: torch.nn.Module, filename: str):
    torch.save(model.state_dict(), f"{filename}.pth")
    print(f"Saved PyTorch Model State to {filename}.pth")


def load_model(model: torch.nn.Module, filename: str):
    model.load_state_dict(torch.load(f"{filename}.pth"))
    print(f"Loaded PyTorch Model State from {filename}.pth")
    model.eval()


def run_epoch(  # pylint: disable=too-many-locals too-many-arguments
    epochs: int,
    model: torch.nn.Module,
    training_dataloader: DataLoader[tuple[torch.Tensor, np.int_]],
    test_dataloader: DataLoader[tuple[torch.Tensor, np.int_]],
    device: str,
    name: str = "mlp",
) -> tuple[list[float], list[float], list[float], list[float]]:
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    train_losses: list[float] = []
    train_accuracies: list[float] = []
    test_losses: list[float] = []
    test_accuracies: list[float] = []
    for t in range(epochs):
        print(f"\nEpoch {t+1}\n-------------------------------")
        train(training_dataloader, model, loss_fn, optimizer, device)
        train_loss, train_accuracy = test(training_dataloader, model, loss_fn, device)
        print(
            f"Train Accuracy: {(100 * train_accuracy):>0.10f}%, Avg loss: {train_loss:>8f}"
        )
        train_losses.append(train_loss)
        train_accuracies.append(train_accuracy)

        test_loss, test_accuracy = test(test_dataloader, model, loss_fn, device)
        print(
            f"Test Accuracy: {(100 * test_accuracy):>0.10f}%, Avg loss: {test_loss:>8f}"
        )
        test_losses.append(test_loss)
        test_accuracies.append(test_accuracy)

        if test_accuracy > 0.85 and t % 50 == 0:
            save_model(model, f"{name}_model_{t}")

        if test_accuracy > 0.98:
            print("Reached 98% accuracy so cancelling training")
            break

    print("Done!")
    return train_losses, train_accuracies, test_losses, test_accuracies


def main(hiddens: list[int]):
    batch_size = 4
    num_workers = 1

    training_dataloader = DataLoader(
        training_data, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    test_dataloader = DataLoader(
        test_data, batch_size=batch_size, num_workers=num_workers
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")

    model = MLP(
        in_channels=training_data.num_attributes,
        hidden_channels=[*hiddens, training_data.num_classes],
        inplace=False,
        dropout=0.5,
    )
    model = model.to(device)
    print(model)

    train_losses, train_accuracies, test_losses, test_accuracies = run_epoch(
        epochs=2000,
        model=model,
        training_dataloader=training_dataloader,
        test_dataloader=test_dataloader,
        device=device,
        name=f"mlp_{''.join(map(str, hiddens))}",
    )
    save_model(model, f"mlp_{''.join(map(str, hiddens))}_model_final")

    with open("train_losses.json", "w", encoding="utf-8") as f:
        json.dump(train_losses, f)

    with open("train_accuracies.json", "w", encoding="utf-8") as f:
        json.dump(train_accuracies, f)

    with open("test_losses.json", "w", encoding="utf-8") as f:
        json.dump(test_losses, f)

    with open("test_accuracies.json", "w", encoding="utf-8") as f:
        json.dump(test_accuracies, f)


if __name__ == "__main__":
    main(hiddens=list(map(int, sys.argv[1:])))
