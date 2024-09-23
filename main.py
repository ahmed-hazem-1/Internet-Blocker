import AppExtractor
import os
import sys
from PyQt5 import QtWidgets, uic
import ListItem


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        # Load the main UI from the UIs folder
        ui_file_path = os.path.join('UIs', 'main.ui')
        uic.loadUi(ui_file_path, self)
        self.ApplyChanges = self.findChild(QtWidgets.QPushButton, 'ApplyChanges')
        self.ApplyChanges.clicked.connect(self.disconnect_internet_for_checked_apps)
        self.return_to_default = self.findChild(QtWidgets.QPushButton, 'Defaults')
        self.return_to_default.clicked.connect(self.return_to_default_func)

        self.setWindowTitle("Internet Control App")
        self.apps = {}
        # Assuming the user_selector and toggle_button are in the UI file
        # Initialize List Widget to display installed apps
        self.app_list_widget = self.findChild(QtWidgets.QListWidget,
                                              'listWidget')  # Adjust the name to match your UI

        ListItem.intialize_list_widget(self.app_list_widget)

        self.apps = AppExtractor.get_installed_apps()

        for app_name, app_info in self.apps.items():
            print("Adding item:", app_name, app_info)  # Check the structure of app_info
            ListItem.add_item(self.app_list_widget, app_name, app_info['version'], False)
        self.show()

        # Connect the 'Select All' checkbox to the select_all_toggle function
        select_all_checkbox = self.app_list_widget.itemWidget(self.app_list_widget.item(0)).Disable
        # select_all_checkbox.stateChanged.connect(ListItem.select_all_toggle)
        select_all_checkbox.stateChanged.connect(self.select_all_toggle)

    def select_all_toggle(self):
        """Toggle all checkboxes based on the 'Select All' checkbox state."""
        # Get the state of the 'Select All' checkbox (first item)
        select_all_state = self.app_list_widget.itemWidget(self.app_list_widget.item(0)).Disable.isChecked()

        # Loop through all items except the first one ('Select All')
        for i in range(1, self.app_list_widget.count()):
            item_widget = self.app_list_widget.itemWidget(self.app_list_widget.item(i))
            if item_widget:
                item_widget.Disable.setChecked(select_all_state)

    def check_select_all_status(self):
        """Check if all checkboxes are checked, and update 'Select All' checkbox accordingly."""
        all_checked = True

        # Check the state of all items except the first one ('Select All')
        for i in self.count():
            item_widget = self.itemWidget(self.item(i))
            if item_widget and not item_widget.Disable.isChecked():
                all_checked = False
                break

        # Update the 'Select All' checkbox
        self.itemWidget(self.item(0)).Disable.setChecked(all_checked)

    def disconnect_internet_for_checked_apps(self):
        for i in range(1, self.app_list_widget.count()):  # Start from 1 to skip 'Select All'
            item_widget = self.app_list_widget.itemWidget(self.app_list_widget.item(i))

            if item_widget and item_widget.Disable.isChecked():  # If checked
                app_name = item_widget.AppName.text()  # Get app name
                app_path = self.get_app_path(app_name)  # Implement this to get the app path
                AppExtractor.block_program(app_path)  # Block the app's internet access

    def return_to_default_func(self):
        for i in range(1, self.app_list_widget.count()):
            item_widget = self.app_list_widget.itemWidget(self.app_list_widget.item(i))
            if item_widget and item_widget.Disable.isChecked():
                app_name = item_widget.AppName.text()
                app_path = self.get_app_path(app_name)
                AppExtractor.delete_firewall_rule(app_path)

    def get_app_path(self, app_name):
        """Get the path of the specified app with the executable."""
        app_info = self.apps.get(app_name)

        if app_info:
            # Get the base path from install_location
            app_path = app_info.get('install_location')

            # Check if the installation path exists
            if not app_path or not os.path.exists(app_path):
                print(f"Installation path not found: {app_path}")
                return None

            # Construct the executable path
            app_executable = os.path.join(app_path,
                                          f"{app_name}.exe")  # Assuming the executable name matches the app name

            # Check if the executable exists
            if os.path.isfile(app_executable):
                return app_executable
            else:
                print(f"Executable not found: {app_executable}")

        print(f"Application '{app_name}' not found in installed apps.")
        return None


if __name__ == "__main__":
    # if is_admin():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    sys.exit(app.exec_())
