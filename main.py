import sys

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # TODO: use rcc # pylint: disable=fixme
    engine.load("src/ui/main.qml")
    rootObjects = engine.rootObjects()
    if not rootObjects:
        sys.exit("Engine loading failed")
    ex = app.exec()
    del engine  # Avoid TypeError from QML app
    sys.exit(ex)
