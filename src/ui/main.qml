import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import InteractiveConceptBottleneck.Ui

ApplicationWindow {
    id: app

    Bridge { id: bridge }

    property var state: JSON.parse(bridge.state)

    visible: true
    width: 1080
    height: 720
    title: "Interactive Concept Bottleneck Model"

    ColumnLayout {
        anchors.fill: parent

        Pane {
            Layout.fillWidth: true
            Layout.fillHeight: true

            background: Rectangle {
                color: "lightgray"
            }

            Image {
                visible: app.state.imagePath.length === 0
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
                source: "assets/icon-picture.svg"
            }

            Image {
                visible: app.state.imagePath.length !== 0
                height: parent.height
                width: parent.width
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
                source: app.state.imagePath
            }
        }

        RowLayout {
            Layout.fillWidth: true

            Button {
                Layout.fillWidth: true
                Layout.leftMargin: 4
                text: "Set Image"
                onClicked: fileDialog.open()

                FileDialog {
                    id: fileDialog
                    nameFilters: [ "Images (*.jpeg *.jpg)" ]
                    onAccepted: bridge.setImagePath(fileDialog.selectedFile)
                }
            }

            Button {
                Layout.fillWidth: true
                Layout.rightMargin: 4
                text: "Predict"
                onClicked: bridge.predict()
                enabled: app.state.imagePath.length !== 0
            }
        }

        RowLayout {
            id: resultTables
            readonly property var rowsPerPage: 8

            Layout.fillWidth: true

            Pane {
                Layout.fillWidth: true
                Layout.preferredWidth: 200 // We need to set the width to a fixed value to make the row layout split two tables evenly

                ColumnLayout {
                    anchors.fill: parent
                    Layout.margins: 12

                    Label {
                        Layout.fillWidth: true
                        text: "Recognized Concepts"
                        horizontalAlignment: Text.AlignHCenter
                        font.bold: true
                    }

                    RowLayout {
                        id: conceptTable
                        Layout.fillWidth: true

                        property var sortedConcepts: Object.entries(app.state.concepts).sort((a, b) => b[1] - a[1])
                        property var pagedConcepts: sortedConcepts.reduce((rows, key, index) => (index % resultTables.rowsPerPage === 0 ? rows.push([key]) : rows[rows.length - 1].push(key)) && rows, [])

                        spacing: 0

                        ColumnLayout {
                            Label {
                                Layout.fillWidth: true
                                text: "Concept"
                                horizontalAlignment: Text.AlignHCenter
                                padding: 8
                                font.bold: true
                            }

                            Repeater {
                                model: conceptTable.pagedConcepts[app.state.selectedConceptPage]?.map(concept => concept[0])

                                delegate: Label {
                                    id: conceptLabelRepeater
                                    required property var modelData
                                    required property var index

                                    Layout.fillWidth: true
                                    text: modelData
                                    horizontalAlignment: Text.AlignHCenter
                                    padding: 4
                                    background: Rectangle {
                                        color: conceptLabelRepeater.index % 2 === 0 ? "white" : "whitesmoke"
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            Label {
                                Layout.fillWidth: true
                                text: "Probability"
                                horizontalAlignment: Text.AlignHCenter
                                padding: 8
                                font.bold: true
                            }

                            Repeater {
                                model: conceptTable.pagedConcepts[app.state.selectedConceptPage]?.map(concept => concept[1])
                                delegate: Pane {
                                    id: conceptProbabilityRepeater
                                    required property var modelData
                                    required property var index

                                    Layout.fillWidth: true

                                    padding: 0
                                    background: Rectangle {
                                        color: conceptProbabilityRepeater.index % 2 === 0 ? "white" : "whitesmoke"
                                    }

                                    RowLayout {
                                        anchors.fill: parent

                                        TextInput {
                                            Layout.fillWidth: true
                                            text: (conceptProbabilityRepeater.modelData * 100).toFixed(2)
                                            horizontalAlignment: Text.AlignHCenter
                                            padding: 4
                                            validator: DoubleValidator {
                                                bottom: 0
                                                top: 100
                                                notation: DoubleValidator.StandardNotation
                                                decimals: 2
                                            }
                                        }

                                        Label {
                                            Layout.rightMargin: 4
                                            text: "%"
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Pane {
                        Layout.fillWidth: true
                        padding: 0
                        background: Rectangle { color: "whitesmoke" }

                        RowLayout {
                            anchors.fill: parent

                            Button {
                                text: "<"
                                enabled: app.state.selectedConceptPage > 0
                                onClicked: bridge.previousConceptPage()
                            }

                            Label {
                                Layout.fillWidth: true
                                horizontalAlignment: Text.AlignHCenter
                                text: `${app.state.selectedConceptPage + 1} / ${conceptTable.pagedConcepts.length}`
                            }

                            Button {
                                text: ">"
                                enabled: app.state.selectedConceptPage + 1 < conceptTable.pagedConcepts.length
                                onClicked: bridge.nextConceptPage()
                            }
                        }
                    }
                }
            }

            Pane {
                Layout.fillWidth: true
                Layout.preferredWidth: 200 // We need to set the width to a fixed value to make the row layout split two tables evenly

                ColumnLayout {
                    anchors.fill: parent
                    Layout.margins: 12

                    Label {
                        Layout.fillWidth: true
                        text: "Final Prediction"
                        horizontalAlignment: Text.AlignHCenter
                        font.bold: true
                    }

                    RowLayout {
                        id: classTable
                        Layout.fillWidth: true

                        property var sortedClasses: Object.entries(app.state.classes).sort((a, b) => b[1] - a[1])
                        property var pagedClasses: sortedClasses.reduce((rows, key, index) => (index % resultTables.rowsPerPage === 0 ? rows.push([key]) : rows[rows.length - 1].push(key)) && rows, [])

                        spacing: 0

                        ColumnLayout {
                            Label {
                                Layout.fillWidth: true
                                text: "Species"
                                horizontalAlignment: Text.AlignHCenter
                                padding: 8
                                font.bold: true
                            }

                            Repeater {
                                model: classTable.pagedClasses[app.state.selectedClassPage]?.map(_class => _class[0])

                                delegate: Label {
                                    id: classLabelRepeater
                                    required property var modelData
                                    required property var index

                                    Layout.fillWidth: true
                                    text: modelData
                                    horizontalAlignment: Text.AlignHCenter
                                    padding: 4
                                    background: Rectangle {
                                        color: classLabelRepeater.index % 2 === 0 ? "white" : "whitesmoke"
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            Label {
                                Layout.fillWidth: true
                                text: "Probability"
                                horizontalAlignment: Text.AlignHCenter
                                padding: 8
                                font.bold: true
                            }

                            Repeater {
                                model: classTable.pagedClasses[app.state.selectedClassPage]?.map(_class => _class[1])

                                delegate: Label {
                                    id: classProbabilityRepeater
                                    required property var modelData
                                    required property var index

                                    Layout.fillWidth: true
                                    text: `${(modelData * 100).toFixed(2)}%`
                                    horizontalAlignment: Text.AlignHCenter
                                    padding: 4
                                    background: Rectangle {
                                        color: classProbabilityRepeater.index % 2 === 0 ? "white" : "whitesmoke"
                                    }
                                }
                            }
                        }
                    }

                    Pane {
                        Layout.fillWidth: true
                        padding: 0
                        background: Rectangle {
                            color: "whitesmoke"
                        }

                        RowLayout {
                            anchors.fill: parent

                            Button {
                                text: "<"
                                enabled: app.state.selectedClassPage > 0
                                onClicked: bridge.previousClassPage()
                            }

                            Label {
                                Layout.fillWidth: true
                                horizontalAlignment: Text.AlignHCenter
                                text: `${app.state.selectedClassPage + 1} / ${classTable.pagedClasses.length}`
                            }

                            Button {
                                text: ">"
                                enabled: app.state.selectedClassPage + 1 < classTable.pagedClasses.length
                                onClicked: bridge.nextClassPage()
                            }
                        }
                    }
                }
            }
        }

        Button {
            Layout.fillWidth: true
            text: "Rerun"
            enabled: app.state.imagePath.length !== 0
            onClicked: bridge.rerun()
        }
    }
}
