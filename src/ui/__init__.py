# pylint: disable=invalid-name

import json
from typing import TypedDict

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.concept_bottleneck.predict import ImageToAttributesModel

QML_IMPORT_NAME = "InteractiveConceptBottleneck.Ui"
QML_IMPORT_MAJOR_VERSION = 1


class State(TypedDict):
    imagePath: str


@QmlElement
class Bridge(QObject):
    stateChanged = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._state: State = {"imagePath": ""}

        self.image_to_attributes_model = ImageToAttributesModel()

    @Property(str, notify=stateChanged)  # type: ignore
    def state(self):
        return json.dumps(self._state)

    def _set_state(self, state: State):
        self._state = state
        self.stateChanged.emit()

    @Slot(str)
    def setImagePath(self, value: str):
        if self._state["imagePath"] == value:
            return
        self._set_state({**self._state, "imagePath": value})

    @Slot()
    def predict(self):
        print(self.image_to_attributes_model.predict(self._state["imagePath"]))

    @Slot()
    def rerun(self):
        pass
