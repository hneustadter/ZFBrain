"""
.. module:: main
   :synopsis: main entry point to app.
"""

import sys
import os
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets, uic
import mymath
import surface_plotting as sp


class ZFBrain(QtWidgets.QMainWindow):
    """ main class for ZFBrain """
    def __init__(self):
        super(ZFBrain, self).__init__()
        self.init_ui()

    def init_ui(self):
        """Initializes GUI"""
        ui_path = os.path.join("zfbrain", "ui", "zfbrain.ui")
        self.ui = uic.loadUi(ui_path)

        self.ui.setWindowTitle('ZFBrain')
        # self.ui.setWindowIcon(QtGui.QIcon('logo.png'))

        # this is just a test that mymath was imported as expected
        a = mymath.my_square_root(324.0)

        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        self.ui.mywidget.addItem(xgrid)
        self.ui.mywidget.addItem(ygrid)
        self.ui.mywidget.addItem(zgrid)
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        # scale each grid differently
        xgrid.scale(0.2, 0.1, 0.1)
        ygrid.scale(0.2, 0.1, 0.1)
        zgrid.scale(0.1, 0.2, 0.1)

        # draw sphere
        sphere = sp.draw_sphere()
        self.ui.mywidget.addItem(sphere)

        # custom option
        verts = np.array([
            [0, 0, 0],
            [2, 0, 0],
            [1, 2, 0],
            [1, 1, 1],
        ])
        faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])
        colors = np.array([
            [1, 0, 0, 0.3],
            [0, 1, 0, 0.3],
            [0, 0, 1, 0.3],
            [1, 1, 0, 0.3]
        ])

        ## Mesh item will automatically compute face normals.
        m1 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
        m1.setGLOptions('additive')
        self.ui.mywidget.addItem(m1)

        # there's gotta be a better way to do this, but I don't have it now.
        self.ui.checkBox1.setChecked(True)
        self.ui.checkBox1.stateChanged.connect(
            lambda: self.checkbox_state(self.ui.checkBox1))
        self.ui.checkBox2.setChecked(True)
        self.ui.checkBox2.stateChanged.connect(
            lambda: self.checkbox_state(self.ui.checkBox2))
        self.ui.checkBox3.setChecked(True)
        self.ui.checkBox3.stateChanged.connect(
            lambda: self.checkbox_state(self.ui.checkBox3))
        self.ui.checkBox4.setChecked(True)
        self.ui.checkBox4.stateChanged.connect(
            lambda: self.checkbox_state(self.ui.checkBox4))
        self.ui.checkBox5.setChecked(True)
        self.ui.checkBox5.stateChanged.connect(
            lambda: self.checkbox_state(self.ui.checkBox5))
        # this doesn't work as expected, but it is the closest alternative
        # self.checkboxes = (self.ui.checkboxes.itemAt(i).widget() for
        # i in range(self.ui.checkboxes.count()))
        # for item in self.checkboxes:
        #    item.setChecked(True)
        #    item.stateChanged.connect(lambda:self.checkbox_state(item))

        self.ui.show()

    def checkbox_state(self, b):
        if b.isChecked():
            print(b.text()+" is selected")
        else:
            print(b.text()+" is deselected")


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('ZFBrain')
    ZFBrain()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
