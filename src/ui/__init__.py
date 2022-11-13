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
    pagedConcepts: list[list[str | float]]
    selectedConceptPage: int
    numRowPerPage: int


@QmlElement
class Bridge(QObject):
    stateChanged = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._state: State = {
            "imagePath": "",
            "pagedConcepts": [[]],
            "selectedConceptPage": 0,
            "numRowPerPage": 8,
        }

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
        concepts_with_prob = self.image_to_attributes_model.predict(
            self._state["imagePath"]
        )

        paged_concepts: list[list[str | float]] = [[]]
        for idx, (concept, prob) in enumerate(concepts_with_prob.items()):
            page = idx // self._state["numRowPerPage"]
            if page >= len(paged_concepts):
                paged_concepts.append([])
            paged_concepts[page].extend((concept, prob))

        self._set_state({**self._state, "pagedConcepts": paged_concepts})

    @Slot()
    def nextConceptPage(self):
        if self._state["selectedConceptPage"] + 1 >= len(self._state["pagedConcepts"]):
            return
        self._set_state(
            {
                **self._state,
                "selectedConceptPage": self._state["selectedConceptPage"] + 1,
            }
        )

    @Slot()
    def previousConceptPage(self):
        if self._state["selectedConceptPage"] == 0:
            return
        self._set_state(
            {
                **self._state,
                "selectedConceptPage": self._state["selectedConceptPage"] - 1,
            }
        )

    @Slot()
    def rerun(self):
        pass
