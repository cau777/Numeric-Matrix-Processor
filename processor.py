from sys import exit


def read_matrix():
    while True:
        size = input('Enter size of matrix:').split()
        n_rows = int(size[0])

        print('Enter matrix (numbers separated by spaces):')
        matrix = []
        for x in range(n_rows):
            in_row = input().split()
            try:
                matrix.append([float(x) for x in in_row])
            except (ValueError, IndexError):
                print('Wrong format!')
                break
        else:
            return matrix


def same_size(m1: list[list], m2: list[list]):
    return len(m1) == len(m2) and len(m1[0]) == len(m2[0])


def get_size(m: list[list]):
    return len(m), len(m[0])


def add_matrices(m1: list[list], m2: list[list]):
    result = m1.copy()
    rows, cols = get_size(m1)
    for r in range(rows):
        for c in range(cols):
            result[r][c] += m2[r][c]

    return result


def multiply_by_constant(m: list[list], f: float):
    result = m.copy()
    rows, cols = get_size(m)
    for r in range(rows):
        for c in range(cols):
            result[r][c] *= f

    return result


def multiply_matrices(m1: list[list], m2: list[list]):
    result = []
    for r in range(len(m1)):
        result_row = []
        for c in range(len(m2[0])):
            product = dot(m1[r], [x[c] for x in m2])
            result_row.append(product)
        result.append(result_row)

    return result


def dot(l1: list, l2: list):
    total = 0
    for c1, c2 in zip(l1, l2):
        total += c1 * c2
    return total


def print_matrix(m: list[list], header=''):
    n_rows, n_cols = get_size(m)
    if header != '':
        print(header)

    columns_max_length = []
    for c in range(n_cols):
        max_length = 0
        for r in range(n_rows):
            num = prepare_number(m[r][c])
            max_length = max(max_length, len(num))
        columns_max_length.append(max_length)

    for row in m:
        line = ''
        for n in range(n_cols):
            num = prepare_number(row[n])
            line += ' ' * (1 + columns_max_length[n] - len(num)) + num
        line = line[1:]
        print(line)


def prepare_number(n):
    return str(round(n, 2))


def transpose_main(m: list[list]):
    n_rows, n_cols = get_size(m)
    result = create_matrix(n_cols, n_rows)
    for r in range(n_rows):
        for c in range(n_cols):
            result[c][r] = m[r][c]

    return result


def transpose_side(m: list[list]):
    n_rows, n_cols = get_size(m)
    result = create_matrix(n_cols, n_rows)
    for r in range(n_rows):
        for c in range(n_cols):
            result[n_cols - c - 1][n_rows - r - 1] = m[r][c]

    return result


def transpose_vertical(m: list[list]):
    result = m.copy()
    for row in result:
        row.reverse()

    return result


def transpose_horizontal(m: list[list]):
    result = m.copy()
    result.reverse()
    return result


def find_determinant_recursion(m: list[list]):
    size = len(m)
    if size == 2:
        determinant = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    else:
        determinant = 0
        for x in range(size):
            smaller_matrix = remove_row_column(m, 0, x)
            if x % 2 == 0:
                determinant += m[0][x] * find_determinant_recursion(smaller_matrix)
            else:
                determinant -= m[0][x] * find_determinant_recursion(smaller_matrix)
    return determinant


def invert(m: list[list]):
    n_rows, n_cols = get_size(m)
    determinant = find_determinant_recursion(m)
    if determinant == 0:
        return "This matrix doesn't have an inverse."

    cofactors = []
    for r in range(n_rows):
        line = []
        for c in range(n_cols):
            line.append(pow(-1, r + c) * find_determinant_recursion(remove_row_column(m, r, c)))
        cofactors.append(line)
    # print_matrix(transpose_main(cofactors))
    # print_matrix(cofactors)
    # print(determinant)
    # print(1 / determinant)
    return multiply_by_constant(transpose_main(cofactors), 1 / determinant)


def remove_row_column(m: list[list], index_row: int, index_col: int):
    result = []
    copy = m.copy()
    copy.pop(index_row)

    for r in copy:
        new_row = r.copy()
        new_row.pop(index_col)
        result.append(new_row)
    return result


def create_matrix(rows, cols):
    result = []
    for r in range(rows):
        result.append([0] * cols)

    return result


def show_main():
    while True:
        print('1. Add matrices')
        print('2. Multiply matrix by a constant')
        print('3. Multiply matrices')
        print('4. Transpose matrix')
        print('5. Calculate a determinant')
        print('6. Inverse matrix')
        print('0. Exit')

        try:
            option = int(input('Your choice:'))
        except ValueError:
            print('Wrong Format')
            continue

        if option == 0:
            exit()
        elif option == 1:
            matrix1 = read_matrix()
            matrix2 = read_matrix()

            if same_size(matrix1, matrix2):
                op_result = add_matrices(matrix1, matrix2)
                print_matrix(op_result, 'The result is:')
            else:
                print('The operation cannot be performed.')
        elif option == 2:
            matrix1 = read_matrix()
            const = float(input('Enter constant:'))
            op_result = multiply_by_constant(matrix1, const)
            print_matrix(op_result, 'The result is:')
        elif option == 3:
            matrix1 = read_matrix()
            matrix2 = read_matrix()
            op_result = multiply_matrices(matrix1, matrix2)
            print_matrix(op_result, 'The result is:')
        elif option == 4:
            print('1. Main diagonal')
            print('2. Side diagonal')
            print('3. Vertical line')
            print('4. Horizontal line')
            transpose_option = int(input('Your choice:'))

            if 1 <= transpose_option <= 4:
                matrix1 = read_matrix()

                if transpose_option == 1:
                    op_result = transpose_main(matrix1)
                elif transpose_option == 2:
                    op_result = transpose_side(matrix1)
                elif transpose_option == 3:
                    op_result = transpose_vertical(matrix1)
                else:
                    op_result = transpose_horizontal(matrix1)

                print_matrix(op_result)
            else:
                print('Operation not supported. ')
        elif option == 5:
            matrix1 = read_matrix()
            if len(matrix1) == 1:
                op_result = matrix1[0][0]
            else:
                op_result = find_determinant_recursion(matrix1)
            print(op_result)
        elif option == 6:
            matrix1 = read_matrix()
            op_result = invert(matrix1)

            if op_result is str:
                print(op_result)
            else:
                print_matrix(op_result)
        else:
            print('Operation not supported. ')


show_main()
