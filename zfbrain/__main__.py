"""
.. module:: main
   :synopsis: main entry point to app.
"""

import os
import sys

import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtGui, QtWidgets, QtCore

import surface_plotting as sp

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


# taken from https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class brainView(gl.GLViewWidget):
    """ main class for viewing brain regions """
    def __init__(self, parent=None):
        super(brainView, self).__init__(parent)

        HVC_L_file = resource_path("zfbrain/data/HVC_L.surf")
        HVC_R_file = resource_path("zfbrain/data/HVC_R.surf")
        RA_L_file = resource_path("zfbrain/data/RA_L.surf")
        RA_R_file = resource_path("zfbrain/data/RA_R.surf")
        X_L_file = resource_path("zfbrain/data/AreaX_L.surf")
        X_R_file = resource_path("zfbrain/data/AreaX_R.surf")
        brain_L_file = resource_path("zfbrain/data/whole_brain_L.surf")
        brain_R_file = resource_path("zfbrain/data/whole_brain_R.surf")

        verts_HVC_L, faces_HVC_L = sp.read_surface(HVC_L_file)
        verts_HVC_R, faces_HVC_R = sp.read_surface(HVC_R_file)
        verts_RA_L, faces_RA_L = sp.read_surface(RA_L_file)
        verts_RA_R, faces_RA_R = sp.read_surface(RA_R_file)
        verts_X_L, faces_X_L = sp.read_surface(X_L_file)
        verts_X_R, faces_X_R = sp.read_surface(X_R_file)
        verts_brain_L, faces_brain_L = sp.read_surface(brain_L_file)
        verts_brain_R, faces_brain_R = sp.read_surface(brain_R_file)

        self.hvc_L = gl.GLMeshItem(vertexes=verts_HVC_L, faces=faces_HVC_L,
                                   color=(1, 0, 0, 0.2), smooth=True,
                                   drawEdges=False, shader='balloon',
                                   glOptions='additive')

        self.hvc_R = gl.GLMeshItem(vertexes=verts_HVC_R, faces=faces_HVC_R,
                                   color=(0.5, 0.5, 0, 0.2), smooth=True,
                                   drawEdges=False, shader='balloon',
                                   glOptions='additive')

        self.ra_L = gl.GLMeshItem(vertexes=verts_RA_L, faces=faces_RA_L,
                                  color=(0, 1, 0, 0.2), smooth=True,
                                  drawEdges=False, shader='balloon',
                                  glOptions='additive')

        self.ra_R = gl.GLMeshItem(vertexes=verts_RA_R, faces=faces_RA_R,
                                  color=(0.5, 1, 0.5, 0.2), smooth=True,
                                  drawEdges=False, shader='balloon',
                                  glOptions='additive')

        self.areaX_L = gl.GLMeshItem(vertexes=verts_X_L, faces=faces_X_L,
                                     color=(0, 0.5, 0.5, 0.2), smooth=True,
                                     drawEdges=False, shader='balloon',
                                     glOptions='additive')

        self.areaX_R = gl.GLMeshItem(vertexes=verts_X_R, faces=faces_X_R,
                                     color=(1, 0.5, 1, 0.2), smooth=True,
                                     drawEdges=False, shader='balloon',
                                     glOptions='additive')

        self.outer_L = gl.GLMeshItem(vertexes=verts_brain_L, faces=faces_brain_L,
                                   color=(200/255, 100/255, 100/255, 0.5),
                                   drawEdges=False, drawFaces=True,
                                   shader='shaded', glOptions='opaque')

        self.outer_R = gl.GLMeshItem(vertexes=verts_brain_R, faces=faces_brain_R,
                                   color=(200/255, 100/255, 100/255, 0.5),
                                   drawEdges=False, drawFaces=True,
                                   shader='shaded', glOptions='opaque')

        self.addItem(self.outer_L)
        self.addItem(self.outer_R)
        self.addItem(self.hvc_L)
        self.addItem(self.hvc_R)
        self.addItem(self.ra_L)
        self.addItem(self.ra_R)
        self.addItem(self.areaX_L)
        self.addItem(self.areaX_R)

        self.setBackgroundColor(50, 50, 50)

        # choose center of whole-brain
        x_center = np.average(np.concatenate((verts_brain_L[:, 0], verts_brain_R[:, 0])))
        y_center = np.average(np.concatenate((verts_brain_L[:, 1], verts_brain_R[:, 1])))
        z_center = np.average(np.concatenate((verts_brain_L[:, 2], verts_brain_R[:, 2])))

        # set camera settings
        # sets center of rotation for field
        new_center = np.array([x_center, y_center, z_center])
        self.opts['center'] = pg.Vector(new_center)
        self.setCameraPosition(distance=2400, elevation=20, azimuth=50)

    def redraw_surfaces(self, isCheckedList):
        self.clear()

        if isCheckedList[0] is True:
            self.addItem(self.outer_L)
        if isCheckedList[1] is True:
            self.addItem(self.outer_R)
        if isCheckedList[2] is True:
            self.addItem(self.hvc_L)
        if isCheckedList[3] is True:
            self.addItem(self.hvc_R)
        if isCheckedList[4] is True:
            self.addItem(self.areaX_L)
        if isCheckedList[5] is True:
            self.addItem(self.areaX_R)
        if isCheckedList[6] is True:
            self.addItem(self.ra_L)
        if isCheckedList[7] is True:
            self.addItem(self.ra_R)


class BrainRegionChooser(QtWidgets.QWidget):
    """ main settings class for which brain regions to show """
    def __init__(self, parent=None):
        super(BrainRegionChooser, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        region_label = QtGui.QLabel("Choose which regions to show")
        self.viewBrainLCB = QtGui.QCheckBox("Outer Brain (L)")
        self.viewBrainRCB = QtGui.QCheckBox("Outer Brain (R)")
        self.viewHVCLCB = QtGui.QCheckBox("HVC (L)")
        self.viewHVCRCB = QtGui.QCheckBox("HVC (R)")
        self.viewAreaXLCB = QtGui.QCheckBox("Area X (L)")
        self.viewAreaXRCB = QtGui.QCheckBox("Area X (R)")
        self.viewRALCB = QtGui.QCheckBox("RA (L)")
        self.viewRARCB = QtGui.QCheckBox("RA (R)")

        self.viewBrainLCB.setChecked(True)
        self.viewBrainRCB.setChecked(True)
        self.viewHVCLCB.setChecked(True)
        self.viewHVCRCB.setChecked(True)
        self.viewAreaXLCB.setChecked(True)
        self.viewAreaXRCB.setChecked(True)
        self.viewRALCB.setChecked(True)
        self.viewRARCB.setChecked(True)

        self.isCheckedList = [True, True, True, True, True, True, True, True]

        layout.addWidget(region_label)
        layout.addWidget(self.viewBrainLCB)
        layout.addWidget(self.viewBrainRCB)
        layout.addWidget(self.viewHVCLCB)
        layout.addWidget(self.viewHVCRCB)
        layout.addWidget(self.viewAreaXLCB)
        layout.addWidget(self.viewAreaXRCB)
        layout.addWidget(self.viewRALCB)
        layout.addWidget(self.viewRARCB)

        self.setLayout(layout)

    def get_checked_state(self):
        # Outer Brain
        if self.viewBrainLCB.isChecked():
            self.isCheckedList[0] = True
        else:
            self.isCheckedList[0] = False

        if self.viewBrainRCB.isChecked():
            self.isCheckedList[1] = True
        else:
            self.isCheckedList[1] = False

        # HVC L
        if self.viewHVCLCB.isChecked():
            self.isCheckedList[2] = True
        else:
            self.isCheckedList[2] = False

        # HVC R
        if self.viewHVCRCB.isChecked():
            self.isCheckedList[3] = True
        else:
            self.isCheckedList[3] = False

        # Area X L
        if self.viewAreaXLCB.isChecked():
            self.isCheckedList[4] = True
        else:
            self.isCheckedList[4] = False

        # Area X R
        if self.viewAreaXRCB.isChecked():
            self.isCheckedList[5] = True
        else:
            self.isCheckedList[5] = False

        # RA L
        if self.viewRALCB.isChecked():
            self.isCheckedList[6] = True
        else:
            self.isCheckedList[6] = False

        # RA R
        if self.viewRARCB.isChecked():
            self.isCheckedList[7] = True
        else:
            self.isCheckedList[7] = False


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
        self.setWindowIcon(QtGui.QIcon(resource_path("images/zfbrain_logo_small.png")))

        main_layout = QtWidgets.QHBoxLayout()

        self.brv = brainView()
        self.sl = Settings()

        main_layout.addWidget(self.brv, stretch=4)
        main_layout.addWidget(self.sl, stretch=1)

        # checkboxes
        self.sl.brc.viewBrainLCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewBrainRCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewHVCLCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewHVCRCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewAreaXLCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewAreaXRCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewRALCB.toggled.connect(self.something_toggled)
        self.sl.brc.viewRARCB.toggled.connect(self.something_toggled)

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
