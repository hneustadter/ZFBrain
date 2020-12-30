"""
This module defines functions that are used to generate graphical
objects in the main viewer window.
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
