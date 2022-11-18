# pylint: disable=invalid-name

import json
from typing import TypedDict

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.concept_bottleneck.dataset import load_attribute_names
from src.concept_bottleneck.inference import (
    AttributesToClassModel,
    ImageToAttributesModel,
)

QML_IMPORT_NAME = "InteractiveConceptBottleneck.Ui"
QML_IMPORT_MAJOR_VERSION = 1


class State(TypedDict):
    imagePath: str
    concepts: dict[str, float]
    selectedConceptPage: int
    classes: dict[str, float]
    selectedClassPage: int


@QmlElement
class Bridge(QObject):
    stateChanged = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._state: State = {
            "imagePath": "",
            "concepts": {},
            "selectedConceptPage": 0,
            "classes": {},
            "selectedClassPage": 0,
        }

        self.image_to_attributes_model = ImageToAttributesModel()
        self.attributes_to_class_model = AttributesToClassModel()

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
        concepts_with_prob = self.image_to_attributes_model.predict(
            self._state["imagePath"]
        )

        self._set_state({**self._state, "concepts": concepts_with_prob})

        self.rerun()

    @Slot()
    def nextConceptPage(self):
        self._set_state(
            {
                **self._state,
                "selectedConceptPage": self._state["selectedConceptPage"] + 1,
            }
        )

    @Slot()
    def previousConceptPage(self):
        self._set_state(
            {
                **self._state,
                "selectedConceptPage": self._state["selectedConceptPage"] - 1,
            }
        )

    @Slot()
    def nextClassPage(self):
        self._set_state(
            {
                **self._state,
                "selectedClassPage": self._state["selectedClassPage"] + 1,
            }
        )

    @Slot()
    def previousClassPage(self):
        if self._state["selectedClassPage"] == 0:
            return
        self._set_state(
            {
                **self._state,
                "selectedClassPage": self._state["selectedClassPage"] - 1,
            }
        )

    @Slot()
    def rerun(self):
        concept_names = load_attribute_names()
        classes_with_prob = self.attributes_to_class_model.predict(
            [self._state["concepts"][name] for name in concept_names]
        )

        self._set_state({**self._state, "classes": classes_with_prob})

    @Slot(str, float)
    def setConceptProbability(self, name: str, value: float):
        print(name, value)
        if self._state["concepts"][name] == value:
            return
        self._set_state(
            {
                **self._state,
                "concepts": {**self._state["concepts"], name: value},
            }
        )
