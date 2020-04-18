class TicTacToeBoard:
    def __str__(self) -> str:
        board_str: str = '---------\n'
        for row in self.board:
            board_str += '| ' + ' '.join(row) + ' |\n'
        board_str += '---------'
        return board_str

    def __init__(self, initial_board: str) -> None:
        if not initial_board:
            initial_board = '_________'
        elif len(initial_board) != 9:
            print("Whoops! 3x3 board requires 9 characters as input.")
            return
        self.board = self.convert_str_board_to_list_board(initial_board)

    def convert_str_board_to_list_board(self, initial_board: str) -> list:
        initial_board = initial_board.replace('_', ' ')
        return [list(initial_board[x: x+3]) for x in range(0, 9, 3)]

    def is_available(self, row: int, column: int) -> bool:
        return self.board[row][column] == ' '

    def insert(self, user: str, row: int, column: int) -> None:
        self.board[row][column] = user

    def not_full(self) -> bool:
        for x in self.board:
            for y in x:
                if y == ' ':
                    return True
        return False

    def get_all_available(self) -> list:
        all_available: list = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.is_available(row, column):
                    all_available.append({"row": row, "column": column})
        return all_available
