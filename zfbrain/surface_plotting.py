"""
.. module:: surface_plotting
   :synopsis: defines functions and classes for plotting surfaces.
"""

import pyqtgraph.opengl as gl


def draw_sphere():
    """This is a basic method just to draw a sphere. """
    md = gl.MeshData.sphere(rows=10, cols=10, radius=1)
    return gl.GLMeshItem(
            meshdata=md,
            smooth=False,
            color=(1, 0, 0, 0.2),
            shader="balloon",
            glOptions="additive",
            drawEdges=True
        )
