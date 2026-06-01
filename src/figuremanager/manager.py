import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

from PyQt5 import QtWidgets

class FigureManager(QtWidgets.QMainWindow):
    """
    Top‑level Qt with QTabWidget to hold figures
    """
    def __init__(self, show_empty_window):
        super().__init__()
        self.setWindowTitle('FigureManager')
        self.resize(1280, 720)

        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self._canvases = [] # list of FigureCanvas objects
        self._figures  = [] # list of matplotlib Figure objects

        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_tab)
        
        if show_empty_window:
            self.show()

    def _close_tab(self, index: int):
        """
        Remove the tab, delete the canvas and close the associated figure
        """
        widget = self.tab_widget.widget(index)
        if widget is not None:
            canvas = widget.findChild(FigureCanvas)
            if canvas is not None:
                fig = canvas.figure
                plt.close(fig)
                if canvas in self._canvases:
                    self._canvases.remove(canvas)
                if fig in self._figures:
                    self._figures.remove(fig)
                widget.deleteLater()
        self.tab_widget.removeTab(index)

    def add_figure_as_tab(self, fig: plt.Figure):
        canvas = FigureCanvas(fig)

        toolbar = NavigationToolbar(canvas, self)

        tab_container = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(tab_container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(toolbar)
        vbox.addWidget(canvas)

        tab_name = getattr(fig, "_tab_name", None)
        if tab_name is None:
            suptitle = fig._suptitle
            if suptitle is not None and suptitle.get_text():
                tab_name = suptitle.get_text()
            else:
                tab_name = f"Figure {fig.number}"
        tab_name = str(tab_name)

        self.tab_widget.addTab(tab_container, tab_name)
        self.tab_widget.setCurrentWidget(tab_container)

        self._canvases.append(canvas)
        self._figures.append(fig)

        plt.close(fig)

        self.show()
        self.raise_()
        self.activateWindow()


def start_figure_manager(show_empty_window=False):
    """
    Monkey-patches plt.show()
    Embeds current figure, plt.gcf(), inside a master window.
    """
    _app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    _master_win = FigureManager(show_empty_window)

    _original_show = plt.show

    def _patched_show(*args, **kwargs):
        fig = plt.gcf()
        _master_win.add_figure_as_tab(fig)
        return None

    plt.show = _patched_show
