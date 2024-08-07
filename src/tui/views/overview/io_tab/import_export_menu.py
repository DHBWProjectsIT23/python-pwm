import curses
from curses.textpad import rectangle
from src.tui.keys import Keys
from src.tui.panel import Panel
from src.tui.popup import create_centered_popup
from src.tui.window import Window


class ImportExportMenu:
    def __init__(self, parent: Panel) -> None:
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
        self._select_import()
        self._deselect_export()
        self.choice = 1

    def down_action(self) -> None:
        self._deselect_import()
        self._select_export()
        self.choice = 2

    def get_choice(self) -> int:
        return self.choice

    def refresh(self) -> None:
        if self.choice == 1:
            self.down_action()
            self.up_action()
        elif self.choice == 2:
            self.up_action()
            self.down_action()
        else:
            raise ValueError("Invalid menu choice")

    def _select_import(self) -> None:
        self.import_button.writeCenteredText(self.import_text)
        self.import_button().box()
        self.import_button().bkgd(" ", curses.A_REVERSE)
        self.import_button().refresh()

    def _deselect_import(self) -> None:
        self.import_button.writeCenteredText(self.import_text)
        self.import_button().box()
        self.import_button().bkgd(" ")
        self.import_button().refresh()

    def _select_export(self) -> None:
        self.export_button.writeCenteredText(self.export_text)
        self.export_button().box()
        self.export_button().bkgd(" ", curses.A_REVERSE)
        self.export_button().refresh()

    def _deselect_export(self) -> None:
        self.export_button.writeCenteredText(self.export_text)
        self.export_button().box()
        self.export_button().bkgd(" ")
        self.export_button().refresh()
