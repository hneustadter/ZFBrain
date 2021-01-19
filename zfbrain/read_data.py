import numpy as np

# test_file_name = "test_surface.surf"


def read_surface(file_name):
    with open(file_name) as f:
        lines = f.readlines()

        # read in L=number of slices, N=number of data points per slice
        L, N = map(int, lines[1].split(' '))

        # generate data vertex array
        n_vertex = L*N+2
        n_faces = 2*N*L
        verts = np.zeros((n_vertex, 3), float)
        faces = np.zeros((n_faces, 3), int)
        colors = np.zeros((n_faces, 4), float)

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

        # generate random colors for surfaces
        alpha = 1.0  # transparency
        for ind in range(n_faces):
            rand_num = np.random.uniform(0, 1)
            other = (1 - rand_num) / 2

            colors[ind, 0] = rand_num
            colors[ind, 1] = other
            colors[ind, 2] = other
            colors[ind, 3] = alpha

    return verts, faces, colors
