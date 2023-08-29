from PyQt5.QtWidgets import QMenuBar, QAction, QMainWindow, QApplication


class MainMenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.file_menu = self.addMenu("&File")
        self.edit_menu = self.addMenu("&Edit")
        self.view_menu = self.addMenu("&View")
        self.help_menu = self.addMenu("&Help")

        self.init_file_menu()
        self.init_edit_menu()
        self.init_view_menu()
        self.init_help_menu()

    def init_file_menu(self):
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        self.file_menu.addAction(new_action)
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)

    def init_edit_menu(self):
        undo_action = QAction("Undo", self)
        redo_action = QAction("Redo", self)
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)

        self.edit_menu.addAction(undo_action)
        self.edit_menu.addAction(redo_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(cut_action)
        self.edit_menu.addAction(copy_action)
        self.edit_menu.addAction(paste_action)

    def init_view_menu(self):
        zoom_in_action = QAction("Zoom In", self)
        zoom_out_action = QAction("Zoom Out", self)

        self.view_menu.addAction(zoom_in_action)
        self.view_menu.addAction(zoom_out_action)

    def init_help_menu(self):
        about_action = QAction("About", self)

        self.help_menu.addAction(about_action)