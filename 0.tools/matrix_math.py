class Matrix:
    def __init__(self):
        self.temp_matrix = [
            [3, 2, 0, -12],
            [1, 2, -4, -3],
            [-4, -6, 15, 16]
        ]
        self.num_rows = len(self.temp_matrix)
        self.num_cols = len(self.temp_matrix[0])

    def to_gaussian(self):
        first_col = [i[0] for i in self.temp_matrix]
        one_index = first_col.index(1)
        if not one_index == 0:
            to_move_row = self.temp_matrix.pop(one_index)
            self.temp_matrix.insert(0, to_move_row)
            print(self.temp_matrix)

Matrix().to_gaussian()
