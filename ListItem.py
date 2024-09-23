from PyQt5 import uic, QtWidgets
import os

from PyQt5.QtCore import QSize

ui_file_path = os.path.join('UIs', 'list_item.ui')
CustomListItemUi, _ = uic.loadUiType(ui_file_path)


def intialize_list_widget(self):
    list_item = QtWidgets.QListWidgetItem()
    list_item.setSizeHint(QSize(100, 50))
    self.addItem(list_item)
    item = ListItem(self)
    item.add_app_to_list("App Name", "Version", False)
    item.Disable.setText("Select All")
    item.Version.setStyleSheet(
        "font-size: 15px;"
        "color: black;"
        "font-weight: 900;"
        "font-family: Segoe UI;"

    )
    item.AppName.setStyleSheet(
        "font-size: 15px;"
        "color: black;"
        "font-weight: 900;"
        "font-family: Segoe UI;"

    )
    item.Disable.setStyleSheet(
        "font-size: 15px;"
        "color: black;"
        "font-weight: 900;"
        "font-family: Segoe UI;"

    )
    self.setItemWidget(list_item, item)

    # # Connect the checkbox state change to a function
    # item.Disable.stateChanged.connect(check_select_all_status)


def add_item(self, app_name, app_version, toggle_state=False):
    list_item = QtWidgets.QListWidgetItem()
    list_item.setSizeHint(QSize(100, 50))
    self.addItem(list_item)
    item = ListItem(self)
    item.add_app_to_list(app_name, app_version, toggle_state)
    self.setItemWidget(list_item, item)


class ListItem(QtWidgets.QWidget, CustomListItemUi):
    def __init__(self, list_widget):
        super().__init__()
        self.setupUi(self)
        self.list_widget = list_widget
        self.label_name = self.findChild(QtWidgets.QLabel, 'AppName')
        self.Disable = self.findChild(QtWidgets.QCheckBox, 'Disable')
        self.app_version = self.findChild(QtWidgets.QLabel, 'Version')
        self.fixed_font_size()
        self.fixed_size()

    def add_app_to_list(self, app_name, app_version, toggle_state=False):
        self.label_name.setText(app_name)
        self.app_version.setText(app_version)
        self.app_version.repaint()  # Force the QLabel to update its display
        self.Disable.setChecked(toggle_state)

    def fixed_size(self):
        self.app_version.setFixedHeight(25)
        self.label_name.setFixedHeight(25)
        self.Disable.setFixedWidth(150)

    def fixed_font_size(self):
        self.app_version.setStyleSheet(
            "font-size: 12px;"
            "color: red;"
        )
        self.label_name.setStyleSheet(
            "font-size: 15px;"
            "color: black;"
            "font-weight: normal;"  # Increase the font weight
        )
        self.Disable.setStyleSheet(
            "font-size: 15px;"
            "color: black;"
            "font-weight: normal;"  # Increase the font weight
        )
