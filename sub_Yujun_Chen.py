import sys
def read_data(filename):
    with open(filename, 'r') as file:
        # Read each line of the file and remove the newline character at the end of each line
        lines = [line.strip() for line in file.readlines()]
   
        # Extract all unique characters
    unique_chars = set(''.join(lines))

    # Initialize the set of possible numbers each character can represent
    variables = {char: set(range(10)) for char in unique_chars}

    # For the first letter of each word in the addition operation, remove the possibility of being 0
    for line in lines:
        first_char = line[0]
        if first_char in variables:
            variables[first_char].discard(0)
    return lines, variables

def calculate_degree(variable, lines):
    # Calculate the total number of occurrences of the variable in all lines
    return sum(line.count(variable) for line in lines)

def select_unassigned_variable(assignment, variables, lines):
    # First use MRV to select a variable
    unassigned_vars = [v for v in variables if v not in assignment]
    vars_with_min_values = [v for v in unassigned_vars if len(variables[v]) == min(len(variables[v]) for v in unassigned_vars)]

    # If there are multiple variables with the same minimum remaining values, use DH to select a variable
    if len(vars_with_min_values) > 1:
        return max(vars_with_min_values, key=lambda var: calculate_degree(var, lines))
    else:
        return vars_with_min_values[0] if vars_with_min_values else None

def is_valid(assignment, lines):
    try:
        values = []
        for line in lines:
            number = ''
            for char in line:
                if char in assignment:
                    number += str(assignment[char])
                else:
                    # Return False if the character has not yet been assigned
                    print(f"Character '{char}' not yet assigned.")
                    return False
            values.append(int(number))

        valid = sum(values[:-1]) == values[-1]
        return valid
    except ValueError:
        print("Invalid: ValueError encountered.")
        return False

def backtrack(assignment, variables, lines, depth=0):
    if len(assignment) == len(variables):
        return assignment if is_valid(assignment, lines) else None

    var = select_unassigned_variable(assignment, variables, lines)
    for value in variables[var]:
        # Ensure the current value being tried is not already used by an assigned variable
        if any(value == assigned_value for assigned_value in assignment.values()):
            continue

        new_assignment = assignment.copy()
        new_assignment[var] = value

        result = backtrack(new_assignment, variables, lines, depth + 1)
        if result is not None:
            return result

    return None

# Example usage
# Note: This code is for reference only and should be used within a complete code framework
# that includes the definition of select_unassigned_variable and other functions

# Solve the problem

def output_solution(solution, lines, filename):
    with open(filename, 'w') as file:
        for line in lines:
            # Replace each character in the line with the corresponding number
            number_line = ''.join(str(solution[char]) if char in solution else char for char in line.strip())
            file.write(number_line + '\n')


def main():
    
    if len(sys.argv) < 2:
        print("Usage: python script.py input_filename [output_filename]")
        return

    input_filename = sys.argv[1]  # First command line argument
    output_filename = sys.argv[2] if len(sys.argv) > 2 else "default_output.txt"  # Second command line argument or default

    # Read problem data and initialize variables
    lines, variables,= read_data(input_filename)

    # Initialize current solution
    assignment = {}

    # Use the backtracking algorithm to find a solution
    solution = backtrack(assignment, variables, lines)
    
    if solution:
        # If a solution is found, output it to a file
        output_solution(solution, lines, output_filename)
        print(f"Solution found and written to {output_filename}")
    else:
        # If no solution is found
        print("No solution found.")

if __name__ == "__main__":
    main()
