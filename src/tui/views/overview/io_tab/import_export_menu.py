"""
Module for handling the import and export menu in a terminal user interface.
Includes the ImportExportMenu class for managing menu options and user interactions.
"""
import curses

from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window


class ImportExportMenu:
    """
    A menu for selecting between import and export options. Displays buttons for 
    importing and exporting passwords, and allows navigation between these options.

    Args:
        parent (Panel): The parent Panel object where the menu will be displayed.
    """
    def __init__(self, parent: Panel) -> None:
        """
        Initializes the ImportExportMenu with buttons for import and export options.

        Args:
            parent (Panel): The parent Panel object where the menu will be displayed.
        """
        self.parent = Window(parent())

        self.import_text = "Import Passwords"
        self.import_button = create_centered_popup(
            self.parent, 5, len(self.import_text) + 4, (-3, 0)
        )
        self._select_import()

        self.export_text = "Export Passwords"
        self.export_button = create_centered_popup(
            self.parent, 5, len(self.export_text) + 4, (3, 0)
        )
        self._deselect_export()

        self.choice = 1

    def up_action(self) -> None:
        """
        Highlights the import option and deselects the export option.
        Sets the choice to 1 (import).
        """
        self._select_import()
        self._deselect_export()
        self.choice = 1

    def down_action(self) -> None:
        """
        Highlights the export option and deselects the import option.
        Sets the choice to 2 (export).
        """
        self._deselect_import()
        self._select_export()
        self.choice = 2

    def get_choice(self) -> int:
        """
        Gets the currently selected menu option.

        Returns:
            int: The selected option. 1 for import and 2 for export.
        """
        return self.choice

    def refresh(self) -> None:
        """
        Refreshes the menu display based on the current choice. Updates the button 
        highlights according to the selected option.
        
        Raises:
            ValueError: If the choice is invalid (not 1 or 2).
        """
        if self.choice == 1:
            self.down_action()
            self.up_action()
        elif self.choice == 2:
            self.up_action()
            self.down_action()
        else:
            raise ValueError("Invalid menu choice")

    def _select_import(self) -> None:
        """
        Highlights the import button to indicate it is selected.
        """
        self.import_button.write_centered_text(self.import_text)
        self.import_button().box()
        self.import_button().bkgd(" ", curses.A_REVERSE)
        self.import_button().refresh()

    def _deselect_import(self) -> None:
        """
        Removes the highlight from the import button to indicate it is not selected.
        """
        self.import_button.write_centered_text(self.import_text)
        self.import_button().box()
        self.import_button().bkgd(" ")
        self.import_button().refresh()

    def _select_export(self) -> None:
        """
        Highlights the export button to indicate it is selected.
        """
        self.export_button.write_centered_text(self.export_text)
        self.export_button().box()
        self.export_button().bkgd(" ", curses.A_REVERSE)
        self.export_button().refresh()

    def _deselect_export(self) -> None:
        """
        Removes the highlight from the export button to indicate it is not selected.
        """
        self.export_button.write_centered_text(self.export_text)
        self.export_button().box()
        self.export_button().bkgd(" ")
        self.export_button().refresh()
