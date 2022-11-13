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
                text: "Predict"
                onClicked: bridge.predict()
                enabled: app.state.imagePath.length !== 0
            }
        }

        RowLayout {
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

                    GridLayout {
                        Layout.fillWidth: true

                        columns: 2
                        columnSpacing: 0
                        rowSpacing: 0

                        Label {
                            Layout.fillWidth: true
                            text: "Concept"
                            horizontalAlignment: Text.AlignHCenter
                            padding: 8
                            font.bold: true
                        }

                        Label {
                            Layout.fillWidth: true
                            text: "Probability"
                            horizontalAlignment: Text.AlignHCenter
                            padding: 8
                            font.bold: true
                        }

                        Repeater {
                            model: [
                                ...app.state.pagedConcepts[app.state.selectedConceptPage],
                                ...new Array(app.state.numRowPerPage * 2 - app.state.pagedConcepts[app.state.selectedConceptPage].length).fill("-")
                            ]
                            Label {
                                id: conceptLabel
                                required property var modelData
                                required property int index
                                Layout.fillWidth: true
                                text: typeof(modelData) === "number" ? `${(modelData * 100).toFixed(2)}%` : modelData
                                horizontalAlignment: Text.AlignHCenter
                                padding: 4

                                background: Rectangle {
                                    color: Math.floor(conceptLabel.index / 2) % 2 == 0 ? "whitesmoke" : "white"
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
                                enabled: app.state.selectedConceptPage > 0
                                onClicked: bridge.previousConceptPage()
                            }

                            Label {
                                Layout.fillWidth: true
                                horizontalAlignment: Text.AlignHCenter
                                text: `${app.state.selectedConceptPage + 1} / ${Object.keys(app.state.pagedConcepts).length}`
                            }

                            Button {
                                text: ">"
                                enabled: app.state.selectedConceptPage < Object.keys(app.state.pagedConcepts).length - 1
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

                    GridLayout {
                        Layout.fillWidth: true

                        columns: 2
                        columnSpacing: 0
                        rowSpacing: 0

                        Label {
                            Layout.fillWidth: true
                            text: "Species"
                            horizontalAlignment: Text.AlignHCenter
                            padding: 8
                            font.bold: true
                        }

                        Label {
                            Layout.fillWidth: true
                            text: "Probability"
                            horizontalAlignment: Text.AlignHCenter
                            padding: 8
                            font.bold: true
                        }

                        Repeater {
                            model: [
                                ...app.state.pagedClasses[app.state.selectedClassPage],
                                ...new Array(app.state.numRowPerPage * 2 - app.state.pagedClasses[app.state.selectedClassPage].length).fill("-")
                            ]
                            Label {
                                id: conceptLabel
                                required property var modelData
                                required property int index
                                Layout.fillWidth: true
                                text: typeof(modelData) === "number" ? `${(modelData * 100).toFixed(2)}%` : modelData
                                horizontalAlignment: Text.AlignHCenter
                                padding: 4

                                background: Rectangle {
                                    color: Math.floor(conceptLabel.index / 2) % 2 == 0 ? "whitesmoke" : "white"
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
                                text: `${app.state.selectedClassPage + 1} / ${Object.keys(app.state.pagedClasses).length}`
                            }

                            Button {
                                text: ">"
                                enabled: app.state.selectedClassPage < Object.keys(app.state.pagedClasses).length - 1
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
