import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels

ApplicationWindow {
    id: app

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
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
                source: "assets/icon-picture.svg"
            }

            // Image {
            //     height: parent.height
            //     width: parent.width
            //     anchors.centerIn: parent
            //     fillMode: Image.PreserveAspectFit
            //     source: "assets/667-2000x300.jpg"
            // }
        }

        RowLayout {
            Layout.fillWidth: true

            Button {
                Layout.fillWidth: true
                text: "Set Image"
            }

            Button {
                Layout.fillWidth: true
                text: "Predict"
            }
        }

        RowLayout {
            Layout.fillWidth: true

            ColumnLayout {
                Layout.fillWidth: true
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
                            "Concept 1", 0.5, "Concept 2", 0.3, "Concept 3", 0.2, "Concept 3", 0.2, "Concept 3", 0.2, "Concept 3", 0.2, "Concept 3", 0.2, "Concept 3", 0.2, "Concept 3", 0.2, "Concept 3", 0.2,
                        ]
                        Label {
                            id: conceptLabel
                            required property string modelData
                            required property int index
                            Layout.fillWidth: true
                            text: modelData
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
                        }

                        Label {
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignHCenter
                            text: "1/10"
                        }

                        Button {
                            text: ">"
                        }
                    }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
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
                            "Species 1", 0.5, "Species 2", 0.3, "Species 3", 0.2, "Species 3", 0.2, "Species 3", 0.2, "Species 3", 0.2, "Species 3", 0.2, "Species 3", 0.2, "Species 3", 0.2, "Species 3", 0.2,
                        ]
                        Label {
                            id: speciesLabel
                            required property string modelData
                            required property int index
                            Layout.fillWidth: true
                            text: modelData
                            horizontalAlignment: Text.AlignHCenter
                            padding: 4

                            background: Rectangle {
                                color: Math.floor(speciesLabel.index / 2) % 2 == 0 ? "whitesmoke" : "white"
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
                        }

                        Label {
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignHCenter
                            text: "1/10"
                        }

                        Button {
                            text: ">"
                        }
                    }
                }
            }
        }

        Button {
            Layout.fillWidth: true
            text: "Rerun"
        }
    }
}
