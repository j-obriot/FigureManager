import sys
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)

from PyQt5 import QtWidgets

def _get_title(fig: plt.Figure):
    tab_name = getattr(fig, "_tab_name", None)
    if tab_name is not None:
        return str(tab_name)

    # fallback to suptitle
    suptitle = fig._suptitle
    if suptitle is not None and suptitle.get_text():
        tab_name = suptitle.get_text()
        return str(tab_name)

    # fallback to axis title if only one exists
    axes = [ax for ax in fig.get_axes() if ax.get_visible()]
    if len(axes) == 1:
        ax_title = axes[0].get_title()
        if ax_title:
            return str(ax_title)

    # fallback to figure number
    return f"Figure {fig.number}"


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

        tab_name = _get_title(fig)

        self.tab_widget.addTab(tab_container, tab_name)
        self.tab_widget.setCurrentWidget(tab_container)

        self._canvases.append(canvas)
        self._figures.append(fig)

        plt.close(fig)

        self.show()
        self.raise_()
        self.activateWindow()

_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
_master_win = FigureManager(False)

_original_show = plt.show

def _patched_show(*args, **kwargs):
    fig = plt.gcf()
    _master_win.add_figure_as_tab(fig)
    return None

plt.show = _patched_show
