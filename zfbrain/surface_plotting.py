"""
.. module:: surface_plotting
   :synopsis: defines functions and classes for plotting surfaces.
"""

import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET


def read_surface(file_name):
    """Reads in surface data type in the *.surf format.

    Note
    ----
    L is the number of slices of data, N is the number of data points
    per slice. Each must be constant.

    A typical *.surf data file is given by the following:

    .. code-block:: python
        :linenos:

        descriptive string of data
        L N
        x11 y11 z11
        x12 y12 z12
            ...
        x1N y1N z1N
        x21 y21 z21
            ...

    The total number of lines in file_name is 2+L*N

    Parameters
    ----------
    file_name : string
        Filename for surface data.

    Returns
    -------
    verts : ndarray(dtype=float, ndim=2)
        Vertex matrix with shape (`N`, 3). Each row represents a point in 3D,
        and each column represents the X, Y, Z coordinate.
    faces : ndarray(dtype=int, ndim=2)
        Face indices matrix with shape (`N`, 3). Each row represents a face
        (triangle), and each column represents the index of the data point
        for a vertex.

    """
    with open(file_name) as f:
        lines = f.readlines()

        # read in L=number of slices, N=number of data points per slice
        L, N = map(int, lines[1].split(' '))

        # generate data vertex array
        n_vertex = L*N+2
        n_faces = 2*N*L
        verts = np.zeros((n_vertex, 3), float)
        faces = np.zeros((n_faces, 3), int)

        # load in vertices
        for ti in range(0, (L*N)):
            verts[ti,0], verts[ti,1], verts[ti,2] = map(float, lines[ti+2].split(' '))

        # generate last 2 ''ghost points''
        first_gp_ind = L*N
        last_gp_ind = L*N+1
        for ti in range(3):
            verts[first_gp_ind, ti] = np.mean(verts[0:N-1, ti])
            verts[last_gp_ind, ti] = np.mean(verts[(L-1)*N:L*N, ti])

        # generate edges for data in 'middle' slices
        # for the love of god don't modify the indices here
        for tl in range(L-1):
            for tn in range(N):
                ind1 = 2*(tn + tl*N)
                ind2 = ind1 + 1

                val1 = tl*N + tn
                val2 = (tl+1)*N + (tn+1) % N
                val3 = (tl+1)*N + tn
                val4 = tl*N + (tn+1) % N

                faces[ind1, 0] = val1
                faces[ind1, 1] = val2
                faces[ind1, 2] = val3
                faces[ind2, 0] = val1
                faces[ind2, 1] = val4
                faces[ind2, 2] = val2

        # last 2*N faces are to 'cap off' closed surface
        # first face
        for tn in range(N):
            ind = 2*(L-1)*N + tn
            faces[ind, 0] = tn
            faces[ind, 1] = first_gp_ind
            faces[ind, 2] = (tn+1) % N

        # last face
        for tn in range(N):
            ind = 2*(L-1)*N + N + tn
            faces[ind, 0] = (L-1)*N + tn
            faces[ind, 1] = (L-1)*N + (tn + 1) % N
            faces[ind, 2] = last_gp_ind

    return verts, faces


def get_interpolant(xvals, yvals, Nvals):
    # append the starting x,y coordinates
    xvals = np.r_[xvals, xvals[0]]
    yvals = np.r_[yvals, yvals[0]]

    # fit splines to x=f(u) and y=g(u), treating both as periodic.
    # also note that s=0 is needed in order to force the spline
    # fit to pass through all the input points.
    tck, u = interpolate.splprep([xvals, yvals], s=0, per=True)

    # evaluate the spline fits for Nvals evenly spaced distance values
    xi, yi = interpolate.splev(np.linspace(0, 1, Nvals+1), tck)

    return xi[0:-1], yi[0:-1]


def show_interpolate(xvals, yvals, Nvals):
    xi, yi = get_interpolant(xvals, yvals, Nvals)

    xi = np.r_[xi, xi[0]]
    yi = np.r_[yi, yi[0]]

    # plot the results
    plt.plot(xi, yi, color="orange")
    plt.scatter(xvals, yvals)
    for i, txt in enumerate(range(len(xvals[0:-1]))):
        plt.annotate(txt, (xvals[i], yvals[i]))
    plt.show()


def write_surf(A, L, N, out_filename, description=" "):
    """ Writes *.surf data file (ASCII format) into out_filename.surf.
    `description` is the description, N is the number of points on each
    slice (a constant!), L is the number of slices, and A is a N*L x 3
    numpy array containing all data points. """

    # add test that checks L, N and shape of A are consistent

    file = open(fr"{out_filename}.surf", "w")

    # write description
    file.write(description + "\n")

    # write L (number of slice of data) N (number of data points per slice)
    file.write(f"{L} {N}\n")

    # write data
    for row in range(A.shape[0]):
        file.write(f"{A[row,0]} {A[row,1]} {A[row,2]}\n")

    file.close()


def generate_brainexterior_surf(input_file):
    # This code assumes that the hemisphere cut-off is given by the last 
    # slice and is in the z-direction, and starts at zero

    # needs to be hard-coded right now
    DELTA_Z = 40
    MID_Z = DELTA_Z*18
    N_interp = 100

    output_filename = "whole_brain"
    filename = input_file
    tree = ET.parse(filename)
    root = tree.getroot()
    ATTRIB = 'Dendritic extension'

    # ----------------------------------------------
    # 1. first pass, get number of slices and points
    # ----------------------------------------------

    points = []

    ti = 0
    weird_url = '{http://www.mbfbioscience.com/2007/neurolucida}'
    contour_str = weird_url + 'contour'
    point_str = weird_url + 'point'
    for contour in root.iter(contour_str):
        points.append(0)
        for point in contour.iter(point_str):
            points[ti] += 1
        ti += 1

    N_points = sum(points)
    nodes = np.zeros((N_points, 3), dtype=float)

    # -------------------------------
    # 2. second pass, get actual data
    # -------------------------------

    ti = 0
    for contour in root.iter(contour_str):
        for point in contour.iter(point_str):
            nodes[ti, 0] = point.attrib['x']
            nodes[ti, 1] = point.attrib['y']
            nodes[ti, 2] = point.attrib['z']
            ti += 1

    # --------------------------------------------------------------
    # 3. interpolate values so each slice has equal number of points
    # --------------------------------------------------------------

    num_slices = len(points)
    # takes into account that we only get actual data for 1 hemisphere
    num_final_slices = 2*num_slices - 1
    N_final_points = num_final_slices*N_interp

    z_adj = np.zeros((num_slices*N_interp), dtype=float)
    new_nodes = np.zeros((N_final_points, 3), dtype=float)

    for ti in range(num_slices):
        ind_start = sum(points[0:ti])
        ind_end = ind_start + points[ti]
        xvals = nodes[ind_start:ind_end, 0]
        yvals = nodes[ind_start:ind_end, 1]

        xi, yi = get_interpolant(xvals, yvals, N_interp)

        for tj in range(N_interp-1, -1, -1):
            new_nodes[ti*N_interp + tj, 0] = xi[tj]
            new_nodes[ti*N_interp + tj, 1] = yi[tj]
            new_nodes[ti*N_interp + tj, 2] = DELTA_Z*ti
            z_adj[ti*N_interp + tj] = MID_Z - DELTA_Z*ti

        # uncomment this line to display slices and interpolant
        # icc.show_interpolate(xvals, yvals, N_interp)

    # -----------------------------
    # 4. extend data beyond midline
    # -----------------------------

    start_id = num_slices*N_interp
    tj = N_interp + 1
    for ti in range(start_id, N_final_points):
        old_ind = ti - tj
        new_nodes[ti, 0] = new_nodes[old_ind, 0]
        new_nodes[ti, 1] = new_nodes[old_ind, 1]
        new_nodes[ti, 2] = MID_Z + z_adj[old_ind]
        tj += 2

    # --------------------------
    # 5. write data to surf file
    # --------------------------

    L = num_final_slices
    N = N_interp
    write_surf(new_nodes, L, N, output_filename,
               description="This is the outer brain")

    print(f"Output file {output_filename}")


def generate_HVC_surf(input_file):
    # This code is used to generate the HVC surf

    # needs to be hard-coded right now
    DELTA_Z = 40
    MID_Z = DELTA_Z*18  # there are 18 total slices per hemisphere
    N_interp = 100
    OFFSET = 9*DELTA_Z

    output_filename = "HVC"
    filename = input_file
    tree = ET.parse(filename)
    root = tree.getroot()
    ATTRIB = 'HVC L'

    # ----------------------------------------------
    # 1. first pass, get number of slices and points
    # ----------------------------------------------

    points = []

    ti = 0
    elID = 0
    weird_url = '{http://www.mbfbioscience.com/2007/neurolucida}'
    contour_str = weird_url + 'contour'
    point_str = weird_url + 'point'
    for contour in root.iter(contour_str):
        if (contour.attrib['name'] == ATTRIB):
            points.append(0)
            for point in contour.iter(point_str):
                points[ti] += 1
            ti += 1
        elID += 1

    N_points = sum(points)
    nodes = np.zeros((N_points, 3), dtype=float)

    # -------------------------------
    # 2. second pass, get actual data
    # -------------------------------

    ti = 0
    for contour in root.iter(contour_str):
        if (contour.attrib['name'] == ATTRIB):
            for point in contour.iter(point_str):
                nodes[ti, 0] = point.attrib['x']
                nodes[ti, 1] = point.attrib['y']
                nodes[ti, 2] = point.attrib['z']
                ti += 1

    # --------------------------------------------------------------
    # 3. interpolate values so each slice has equal number of points
    # --------------------------------------------------------------

    num_slices = len(points)
    new_nodes = np.zeros((num_slices*N_interp, 3), dtype=float)

    for ti in range(num_slices):
        ind_start = sum(points[0:ti])
        ind_end = ind_start + points[ti]
        xvals = nodes[ind_start:ind_end, 0]
        yvals = nodes[ind_start:ind_end, 1]

        xi, yi = get_interpolant(xvals, yvals, N_interp)

        for tj in range(N_interp-1, -1, -1):
            new_nodes[ti*N_interp + tj, 0] = xi[tj]
            new_nodes[ti*N_interp + tj, 1] = yi[tj]
            new_nodes[ti*N_interp + tj, 2] = DELTA_Z*ti + OFFSET

        # uncomment this line to display slices and interpolant
        # icc.show_interpolate(xvals, yvals, N_interp)

    # --------------------------
    # 4. write data to surf file
    # --------------------------

    L = num_slices
    N = N_interp
    write_surf(new_nodes, L, N, output_filename,
               description=f"This is the {output_filename}")

    print(f"Output file {output_filename}")


def generate_RA_surf(input_file):
    # This code is used to generate the HVC surf

    # needs to be hard-coded right now
    DELTA_Z = 40
    MID_Z = DELTA_Z*18  # there are 18 total slices per hemisphere
    N_interp = 100
    OFFSET = 7*DELTA_Z

    output_filename = "RA"
    filename = input_file
    tree = ET.parse(filename)
    root = tree.getroot()
    ATTRIB = 'RA'

    # ----------------------------------------------
    # 1. first pass, get number of slices and points
    # ----------------------------------------------

    points = []

    ti = 0
    elID = 0
    weird_url = '{http://www.mbfbioscience.com/2007/neurolucida}'
    contour_str = weird_url + 'contour'
    point_str = weird_url + 'point'
    for contour in root.iter(contour_str):
        if (contour.attrib['name'] == ATTRIB):
            points.append(0)
            for point in contour.iter(point_str):
                points[ti] += 1
            ti += 1
        elID += 1

    N_points = sum(points)
    nodes = np.zeros((N_points, 3), dtype=float)

    # -------------------------------
    # 2. second pass, get actual data
    # -------------------------------

    ti = 0
    for contour in root.iter(contour_str):
        if (contour.attrib['name'] == ATTRIB):
            for point in contour.iter(point_str):
                nodes[ti, 0] = point.attrib['x']
                nodes[ti, 1] = point.attrib['y']
                nodes[ti, 2] = point.attrib['z']
                ti += 1

    # --------------------------------------------------------------
    # 3. interpolate values so each slice has equal number of points
    # --------------------------------------------------------------

    num_slices = len(points)
    new_nodes = np.zeros((num_slices*N_interp, 3), dtype=float)

    for ti in range(num_slices):
        ind_start = sum(points[0:ti])
        ind_end = ind_start + points[ti]
        xvals = nodes[ind_start:ind_end, 0]
        yvals = nodes[ind_start:ind_end, 1]

        xi, yi = get_interpolant(xvals, yvals, N_interp)

        for tj in range(N_interp-1, -1, -1):
            new_nodes[ti*N_interp + tj, 0] = xi[tj]
            new_nodes[ti*N_interp + tj, 1] = yi[tj]
            new_nodes[ti*N_interp + tj, 2] = DELTA_Z*ti + OFFSET

        # uncomment this line to display slices and interpolant
        # icc.show_interpolate(xvals, yvals, N_interp)

    # --------------------------
    # 4. write data to surf file
    # --------------------------

    L = num_slices
    N = N_interp
    write_surf(new_nodes, L, N, output_filename,
               description=f"This is the {output_filename}")

    print(f"Output file {output_filename}")


def generate_X_surf(input_file):
    # This code is used to generate the HVC surf

    # needs to be hard-coded right now
    DELTA_Z = 40
    MID_Z = DELTA_Z*18  # there are 18 total slices per hemisphere
    N_interp = 100
    OFFSET = 6*DELTA_Z

    output_filename = "AreaX"
    filename = input_file
    tree = ET.parse(filename)
    root = tree.getroot()
    ATTRIB = 'Area X'

    # ----------------------------------------------
    # 1. first pass, get number of slices and points
    # ----------------------------------------------

    points = []

    ti = 0
    elID = 0
    weird_url = '{http://www.mbfbioscience.com/2007/neurolucida}'
    contour_str = weird_url + 'contour'
    point_str = weird_url + 'point'
    for contour in root.iter(contour_str):
        if (contour.attrib['name'] == ATTRIB):
            points.append(0)
            for point in contour.iter(point_str):
                points[ti] += 1
            ti += 1
        elID += 1

    N_points = sum(points)
    nodes = np.zeros((N_points, 3), dtype=float)

    # -------------------------------
    # 2. second pass, get actual data
    # -------------------------------

    ti = 0
    for contour in root.iter(contour_str):
        if (contour.attrib['name'] == ATTRIB):
            for point in contour.iter(point_str):
                nodes[ti, 0] = point.attrib['x']
                nodes[ti, 1] = point.attrib['y']
                nodes[ti, 2] = point.attrib['z']
                ti += 1

    # --------------------------------------------------------------
    # 3. interpolate values so each slice has equal number of points
    # --------------------------------------------------------------

    num_slices = len(points)
    new_nodes = np.zeros((num_slices*N_interp, 3), dtype=float)

    for ti in range(num_slices):
        ind_start = sum(points[0:ti])
        ind_end = ind_start + points[ti]
        xvals = nodes[ind_start:ind_end, 0]
        yvals = nodes[ind_start:ind_end, 1]

        xi, yi = get_interpolant(xvals, yvals, N_interp)

        for tj in range(N_interp-1, -1, -1):
            new_nodes[ti*N_interp + tj, 0] = xi[tj]
            new_nodes[ti*N_interp + tj, 1] = yi[tj]
            new_nodes[ti*N_interp + tj, 2] = DELTA_Z*ti + OFFSET

        # uncomment this line to display slices and interpolant
        # icc.show_interpolate(xvals, yvals, N_interp)

    # --------------------------
    # 4. write data to surf file
    # --------------------------

    L = num_slices
    N = N_interp
    write_surf(new_nodes, L, N, output_filename,
               description=f"This is the {output_filename}")

    print(f"Output file {output_filename}")