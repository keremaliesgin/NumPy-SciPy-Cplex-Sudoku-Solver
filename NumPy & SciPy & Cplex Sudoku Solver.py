#!/usr/bin/env python
# coding: utf-8

# In[2]:


# load libraries
import numpy as np
import scipy.sparse as sp
import math
import cplex as cp


# In[3]:


def mixed_integer_linear_programming(direction, A, senses, b, c, l, u, types, names):
    # create an empty optimization problem
    prob = cp.Cplex()

    # add decision variables to the problem including their coefficients in objective and ranges
    prob.variables.add(obj = c.tolist(), lb = l.tolist(), ub = u.tolist(), types = types.tolist(), names = names.tolist())

    # define problem type
    if direction == "maximize":
        prob.objective.set_sense(prob.objective.sense.maximize)
    else:
        prob.objective.set_sense(prob.objective.sense.minimize)

    # add constraints to the problem including their directions and right-hand side values
    prob.linear_constraints.add(senses = senses.tolist(), rhs = b.tolist())

    # add coefficients for each constraint
    row_indices, col_indices = A.nonzero()
    prob.linear_constraints.set_coefficients(zip(row_indices.tolist(), col_indices.tolist(), A.data.tolist()))

    print(prob.write_as_string())
    # solve the problem
    prob.solve()

    # check the solution status
    print(prob.solution.get_status())
    print(prob.solution.status[prob.solution.get_status()])

    # get the solution
    x_star = prob.solution.get_values()
    obj_star = prob.solution.get_objective_value()

    return(x_star, obj_star)


# In[4]:


def sudoku_with_grid(input_grid):
    N = input_grid.shape[0]
    N_sq = int(math.sqrt(N))

    # decision variable: x_k_i_j: 1 if value k + 1 is in row i and column j, 0 otherwise
    names = np.array(["x_{}_{}_{}".format(k+1, i+1, j+1) for k in range(N) for i in range(N) for j in range(N)])
    types = np.repeat("B", N**3)
    c = np.repeat(1, N**3)
    l = np.zeros((N, N, N))
    u = np.repeat(1, N**3)
    for y in range(N):
        for x in range(N):
            if input_grid[y][x] != 0:
                l[input_grid[y][x] - 1][y][x] = 1
    l = l.flatten()

    b = np.repeat(1, 4 * N**2)
    senses = np.repeat("E", 4 * N**2)

    # Row constraint
    col_rows = np.arange(N**3)    
    # Col constraint
    col_cols = np.arange(N**3).reshape(N, N, N).swapaxes(1, 2).flatten()
    # Cell constraint
    col_cells = np.arange(N**3).reshape(N, N**2).T.flatten()
    # Box constraint
    col_squares = np.arange(N**3).reshape(N, N_sq, N_sq, N_sq, N_sq).swapaxes(2, 3).flatten()

    row = np.repeat(range(4 * N**2), N)
    col = np.concatenate((col_rows, col_cols, col_cells, col_squares))
    aij = np.repeat(1, col.size)

    A = sp.csr_matrix((aij, (row, col)), shape = (4*N**2, N**3))

    x_star, _ = mixed_integer_linear_programming("maximize", A, senses, b, c, l, u, types, names)
    return np.argmax(np.array(x_star).reshape(N, N, N), axis = 0) + 1


# In[8]:


input_grid = np.array([ # empty grid to easily set-up new games
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
])

input_grid = np.array([
    [0, 9, 0, 0, 3, 2, 0, 0, 1],
    [7, 0, 0, 0, 9, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 9, 6, 0],
    [5, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 1, 8],
    [8, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 5, 4],
    [0, 0, 0, 0, 2, 0, 0, 0, 7],
    [0, 0, 4, 0, 0, 1, 0, 0, 0]
])
if math.sqrt(input_grid.shape[0]) % 1 == 0 and input_grid.shape[0] > 0:
    solution = sudoku_with_grid(input_grid)
    print(solution)
else:
    print("Please provide a suitable sudoku board.")

