# pylint: disable=invalid-name

import json
from typing import TypedDict

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from src.concept_bottleneck.dataset import load_attribute_names
from src.concept_bottleneck.predict import (
    AttributesToClassModel,
    ImageToAttributesModel,
)

QML_IMPORT_NAME = "InteractiveConceptBottleneck.Ui"
QML_IMPORT_MAJOR_VERSION = 1


class State(TypedDict):
    imagePath: str
    numRowPerPage: int
    pagedConcepts: list[list[str | float]]
    selectedConceptPage: int
    pagedClasses: list[list[str | float]]
    selectedClassPage: int


@QmlElement
class Bridge(QObject):
    stateChanged = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._state: State = {
            "imagePath": "",
            "numRowPerPage": 8,
            "pagedConcepts": [[]],
            "selectedConceptPage": 0,
            "pagedClasses": [[]],
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

        sorted_concepts_with_prob = dict(
            sorted(concepts_with_prob.items(), key=lambda x: x[1], reverse=True)
        )

        paged_concepts: list[list[str | float]] = [[]]
        for idx, (concept, prob) in enumerate(sorted_concepts_with_prob.items()):
            page = idx // self._state["numRowPerPage"]
            if page >= len(paged_concepts):
                paged_concepts.append([])
            paged_concepts[page].extend((concept, prob))

        self._set_state({**self._state, "pagedConcepts": paged_concepts})

        self.rerun()

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
    def nextClassPage(self):
        if self._state["selectedClassPage"] + 1 >= len(self._state["pagedClasses"]):
            return
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
        concepts_with_prob: dict[str, float] = {}

        for concepts in self._state["pagedConcepts"]:
            for concept, prob in zip(concepts[::2], concepts[1::2]):
                assert isinstance(concept, str)
                assert isinstance(prob, float)
                concepts_with_prob[concept] = prob

        concept_names = load_attribute_names()
        classes_with_prob = self.attributes_to_class_model.predict(
            [concepts_with_prob[name] for name in concept_names]
        )

        sorted_classes_with_prob = dict(
            sorted(classes_with_prob.items(), key=lambda item: item[1], reverse=True)
        )

        paged_classes: list[list[str | float]] = [[]]
        for idx, (class_, prob) in enumerate(sorted_classes_with_prob.items()):
            page = idx // self._state["numRowPerPage"]
            if page >= len(paged_classes):
                paged_classes.append([])
            paged_classes[page].extend((class_, prob))

        self._set_state({**self._state, "pagedClasses": paged_classes})
