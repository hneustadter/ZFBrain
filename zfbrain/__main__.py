"""
.. module:: main
   :synopsis: main entry point to app.
"""

import os
import sys

import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtGui, QtWidgets

import surface_plotting as sp

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


class brainView(gl.GLViewWidget):
    """ main class for viewing brain regions """
    def __init__(self, parent=None):
        super(brainView, self).__init__(parent)

        HVC_file = "zfbrain/data/HVC.surf"
        RA_file = "zfbrain/data/RA.surf"
        X_file = "zfbrain/data/AreaX.surf"              # what are frogs?
        brain_file = "zfbrain/data/whole_brain.surf"

        verts_HVC, faces_HVC = sp.read_surface(HVC_file)
        verts_RA, faces_RA = sp.read_surface(RA_file)
        verts_X, faces_X = sp.read_surface(X_file)
        verts_brain, faces_brain = sp.read_surface(brain_file)

        self.hvc = gl.GLMeshItem(vertexes=verts_HVC, faces=faces_HVC,
                                 color=(1, 0, 0, 0.2), smooth=True,
                                 drawEdges=False, shader='balloon',
                                 glOptions='additive')

        self.ra = gl.GLMeshItem(vertexes=verts_RA, faces=faces_RA,
                                color=(0, 1, 0, 0.2), smooth=True,
                                drawEdges=False, shader='balloon',
                                glOptions='additive')

        self.areaX = gl.GLMeshItem(vertexes=verts_X, faces=faces_X,
                                color=(0, 0, 1, 0.2), smooth=True,
                                drawEdges=False, shader='balloon',
                                glOptions='additive')

        self.outer = gl.GLMeshItem(vertexes=verts_brain, faces=faces_brain,
                                   color=(1, 1, 1, 0.3), smooth=True,
                                   drawEdges=False, shader='normalColor',
                                   glOptions='opaque')

        self.addItem(self.outer)
        self.addItem(self.hvc)
        self.addItem(self.ra)
        self.addItem(self.areaX)

        print(self.cameraPosition())

        self.setBackgroundColor(50, 50, 50)

        # choose center of whole-brain
        x_center = np.average(verts_brain[:, 0])
        y_center = np.average(verts_brain[:, 1])
        z_center = np.average(verts_brain[:, 2])

        # set camera settings
        self.setCameraPosition(distance=2400, elevation=20)
        # sets center of rotation for field
        new_center = np.array([x_center, y_center, z_center])
        self.opts['center'] = pg.Vector(new_center)

    def redraw_surfaces(self, isCheckedList):
        self.clear()

        if isCheckedList[0] is True:
            self.addItem(self.outer)
        if isCheckedList[1] is True:
            self.addItem(self.hvc)
        if isCheckedList[2] is True:
            self.addItem(self.areaX)
        if isCheckedList[3] is True:
            self.addItem(self.ra)


class BrainRegionChooser(QtWidgets.QWidget):
    """ main settings class for which brain regions to show """
    def __init__(self, parent=None):
        super(BrainRegionChooser, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        region_label = QtGui.QLabel("Choose which regions to show")
        self.viewBrainCB = QtGui.QCheckBox("Outer Brain")
        self.viewHVCCB = QtGui.QCheckBox("HVC")
        self.viewAreaXCB = QtGui.QCheckBox("Area X")
        self.viewRACB = QtGui.QCheckBox("RA")

        self.viewBrainCB.setChecked(True)
        self.viewHVCCB.setChecked(True)
        self.viewAreaXCB.setChecked(True)
        self.viewRACB.setChecked(True)

        self.isCheckedList = [True, True, True, True]

        layout.addWidget(region_label)
        layout.addWidget(self.viewBrainCB)
        layout.addWidget(self.viewHVCCB)
        layout.addWidget(self.viewAreaXCB)
        layout.addWidget(self.viewRACB)

        self.setLayout(layout)

    def get_checked_state(self):
        # Outer Brain
        if self.viewBrainCB.isChecked():
            self.isCheckedList[0] = True
        else:
            self.isCheckedList[0] = False

        # HVC
        if self.viewHVCCB.isChecked():
            self.isCheckedList[1] = True
        else:
            self.isCheckedList[1] = False

        # Area X
        if self.viewAreaXCB.isChecked():
            self.isCheckedList[2] = True
        else:
            self.isCheckedList[2] = False

        # RA
        if self.viewRACB.isChecked():
            self.isCheckedList[3] = True
        else:
            self.isCheckedList[3] = False


class Settings(QtWidgets.QWidget):
    """ main settings class """
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        self.brc = BrainRegionChooser()

        layout.addWidget(self.brc)
        layout.addStretch(1)

        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    """ main class for ZFBrain """
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('ZFBrain')
        self.resize(1000, 600)

        main_layout = QtWidgets.QHBoxLayout()

        self.brv = brainView()
        self.sl = Settings()

        main_layout.addWidget(self.brv, stretch=4)
        main_layout.addWidget(self.sl, stretch=1)

        # checkboxes
        self.sl.brc.viewBrainCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewHVCCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewAreaXCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewRACB.toggled.connect(self.something_toggled)

        main_widget = QtWidgets.QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def something_toggled(self):
        # get isCheckedArray
        self.sl.brc.get_checked_state()

        # redraw everything
        self.brv.redraw_surfaces(self.sl.brc.isCheckedList)


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('ZFBrain')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
