This script takes a sudoku problem and prints the end result.

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
        # l: instead of initializing



        
