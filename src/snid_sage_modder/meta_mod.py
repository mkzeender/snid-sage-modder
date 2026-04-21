from snid_sage.interfaces.gui.components.events.pyside6_event_handlers import PySide6EventHandlers, QtCore

from snid_sage.interfaces.gui.utils.cross_platform_window import (
                CrossPlatformWindowManager as CPW,
            )

from snid_sage_modder import mixin, reload_all


@mixin
class EventHandler(PySide6EventHandlers):

    def setup_keyboard_shortcuts(self):
        super().setup_keyboard_shortcuts()

        CPW.create_shortcut(
                self.main_window,
                "Ctrl+R",
                reload_all,
                context=QtCore.Qt.ApplicationShortcut, # type: ignore
            )