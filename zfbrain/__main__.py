"""
This is the module ZFBrain.

It is used to visualize the zebra finch brain in 3D.
"""

if __name__ == '__main__':
    import pyqtgraph as pg
    import numpy as np
    import pyqtgraph.opengl as gl
    import mymath
    import surface_plotting as sp

    print("This is the ZFBrain module!")

    ## build a QApplication before building other widgets
    pg.mkQApp()

    a = mymath.my_square_root(324.0)

    ## make a widget for displaying 3D objects
    view = gl.GLViewWidget()
    view.show()

    ## create three grids, add each to the view
    xgrid = gl.GLGridItem()
    ygrid = gl.GLGridItem()
    zgrid = gl.GLGridItem()
    view.addItem(xgrid)
    view.addItem(ygrid)
    view.addItem(zgrid)

    ## rotate x and y grids to face the correct direction
    xgrid.rotate(90, 0, 1, 0)
    ygrid.rotate(90, 1, 0, 0)

    ## scale each grid differently
    xgrid.scale(0.2, 0.1, 0.1)
    ygrid.scale(0.2, 0.1, 0.1)
    zgrid.scale(0.1, 0.2, 0.1) 

    sp.draw_sphere()

    print("This is the end of the ZFBrain module!")