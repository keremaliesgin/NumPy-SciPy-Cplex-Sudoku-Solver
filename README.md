This script takes a sudoku problem, models it as an integer programming model, solves it and prints the end result.

How it works:

  To solve, I used CPLEX library. I have a generic mixed_integer_linear_programming function, which takes the necessary arguments to construct a linear programming model.

Core Logic:

  First, we have to decide what the decision variables should be. In theory, one could use use ones as follows:
        x_i_j = {1, 2, ..., N} (intersection of row i and column j is a number)
  This way, our decision variable count is heavily reduced with the side effect of constraint generation being much, much complex. Instead, we define our decision variables as follows:
        x_k_i_j = {0, 1} (1 if color k is in the intersection of row i and column j, 0 otherwise)
  With this definition, we essentially turn a 2-D array into a 3-D cube with binary decision variables. Each layer of 2-D arrays represent the numerical values (for example, first layer is for number 1,
  second layer is for number 2, ..., N'th layer is for number N, and so on). For example, to set (3, 3) to be 6, we go to the x_5_3_3 and force it to be 1 (notice the indexing of Python). It is that simple. 

  Second, we define our objective. Sudoku has no real objective apart from filling all of the squares appropiately, which is a constraint, so we essentially have no objective for our model. Hence, it is arbitrary.

  Third, we define our constraints. For a sudoku, we have four constraints:
        1: Every row must contain exactly one instance of each number.
        2: Every column must contain exactly one instance of each number.
        3: Every cell must contain exactly one number.
        4: Every sub-square must contain exactly one instance of each number.

Since we defined the entire model, let's move onto how we actually model it:

  We already have a powerful CPLEX solver: mixed_integer_linear_programming. Here is what each parameter represents:
        # direction: in linear/integer programming models, we either minimize or maximize something
        # A: the matrix of constraints, each row represents a constraint and each column represents a decision variable
        # senses: the vector of equalities, less thans and greater thans
        # b: the vector of right hand sides
        # c: the objective vector
        # l: lower bounds of all of the decision variables
        # u: upper bounds of all of the decision variables
        # types: each decision variable is either "continuous", "integer" or "binary"; we define it with this vector.
        # names: the vector to name all of the decision variables

  CPLEX takes all of these arguments and uses them to define the problem and solves it.

  Now, let's move onto the part where we craft each of the parameter:
  
        # N: the length (and the amount of colors) of board
        # N_sq: square root of N
        --- total amount of decision variables is just N^3 ---
        # names: just a regular numpy array with list comprehension
        # types: each variable is binary, we just repeat "B" N^3 times
        # c: it is arbitrary, best to set vector of full zeros or ones
        # l: instead of initializing it full of zeros, we initialize it as a cube of zeros. that way, we can force the existing values.
            --> we look up for indices that are not zero with np.argwhere(input_grid != 0). then, we run a for loop for each index, and set the appropiate lower bound as 1. then, we flatten l to convert it into a vector
        # u: all of the upper bounds are 1
        
  At this point, let's take a stop here and analyze how many constraints we will get. In each constraint, we are working with exactly N variables. Since we are working with the full board, we must have N^2 rows for each constraint to cover every decision variable. And since we have exactly 4 constraints, total row count will be 4 * N^2.
  
        # b: we just repeat "1" 4*(N^2) times
        # senses: similarly, we just repeat "E" 4*(N^2) times

  Now, let's take another stop here to observe how A matrix is generated. If you were to generate the matrix in a normal manner, we would have tons of unnecessary zeros, occupying way more memory than it should. So, instead of generating the whole matrix, we generate it as a sparse matrix, which only stores the values with the row and column indices corresponding to that value. This way, we avoid storing unnecessary zeros. This means, we would be needing the every single aij (A_ij, to be more specific), row and column values with the amount of total rows and columns for the matrix. For this example, I will be csr_matrix. Here is how A matrix is defined:

  We know that in each row, we deal with N variables. And since we have 4*(N^2) of them, total amount of 1's required is simply 4*(N^3). So, we initialize repeat "1" 4*(N^3) times for aij vector. Similarly, for row vector, we would be repeating range(4*N^2) N times. 

  And for column indices, we have to handle them separately for each constraint. The best way to figure out how the indices should be placed is messing around in a smaller board and observing the patterns.
    
    --> for the first constraint, it is just range(N^3)
    --> for the second second constraint, we need to be imagine it as swapping the order of indices of x_k_i_j. We need x_k_j_i, so we take a np.arange(N^3) vector, reshape it to be a NxNxN cube, swap the axes 1 and 2 (in our case, i and j), then flatten it back to a vector
    --> for the third constraint, we need x_i_j_k. to understand what happens here, let's analyze another arbitrary (although not related) example:
            # consider y_i_j with Y as the matrix y_i_j belongs. if we were to transpose Y, to find the original y_i_j, we would be looking at y_j_i.
        we will use a similar approach, instead, we think x_k_i_j as x_k_(i_j). What we need to do is create a matrix with dimensions k and ixj (abuse of notation), and then transpose it so that we have a matrix with ixj and k, resulting with the order we want: x_i_j_k. that is what we are going to do here. we take a np.arange(N^3) vector, reshape it to a matrix with NxN^2 dimensions, transpose it and flatten it back to a vector. this gives us the desired order.
    --> for the last constraint, it is way more complex here to explain, but what we do here is take a np.arange(N^3) vector, reshape it into a 5-D array via .reshape(N, N_sq, N_sq, N_sq, N_sq), then swap the axes 2 and 3, and flatten it back to a vector. I **highly** recommend for you to experiment with this yourself. take a np.arange(64) vector, reshape it with .reshape(4, 2, 2, 2, 2) and experiment over there.

  With all of the column indices generated, we combine every piece to a one large vector.

  Now that we have all of the components ready for A matrix, we generate it with A = sp.csr_matrix((aij, (row, col)), shape = (4*(N^2), N^3)) command, and then pass every parameter to our mixed_integer_linear_programming function. With that being done, we essentially modeled a sudoku problem that works for every board with N^2 size!
    

        



        
