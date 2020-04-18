from TicTacToe import TicTacToeBoard
from copy import copy, deepcopy


class Game:
    def __init__(self) -> None:
        cells: str = str(input("Enter Cells: "))
        ai_enabled: bool = 'y' in input("Play against machine? (Y/N) ").lower()
        self.tic_tac_toe: TicTacToeBoard = TicTacToeBoard(cells)
        self.current_player: str = ''

        if ai_enabled:
            self.play_against_machine()
        else:
            self.play()


        print(self.tic_tac_toe)

        if self.game_won() == 'DRAW':
            print("Draw!")
        else:
            print(self.game_won() + ' Wins!')

    def play(self):
        while self.is_game_on():
            self.next_player()
            print(self.tic_tac_toe)
            player_input: dict = self.get_player_input()
            self.tic_tac_toe.insert(self.current_player, player_input['row'], player_input['column'])

    def play_against_machine(self):
        while self.is_game_on():
            print(self.tic_tac_toe)
            self.current_player = 'X'
            player_input: dict = self.get_player_input()
            self.tic_tac_toe.insert(self.current_player, player_input['row'], player_input['column'])

            if not self.is_game_on():
                break

            self.current_player = 'C'
            machine_input: dict = self.AI_move()
            self.tic_tac_toe.insert(self.current_player, machine_input['row'], machine_input['column'])

    def is_game_on(self) -> bool:
        return self.tic_tac_toe.not_full() and not self.game_won()

    def game_won(self, tic_tac_toe:TicTacToeBoard=None) -> str:
        if not tic_tac_toe:
            tic_tac_toe = self.tic_tac_toe
        diagonal_1 = []
        diagonal_2 = []
        for x in range(len(tic_tac_toe.board)):
            row = tic_tac_toe.board[x]
            column = []
            diagonal_1.append(tic_tac_toe.board[x][x])
            diagonal_2.append(tic_tac_toe.board[len(tic_tac_toe.board) - x - 1][x])
            for y in range(len(tic_tac_toe.board[x])):
                column.append(tic_tac_toe.board[y][x])

            if self.checkWinInList(row):
                # Winner is in row!
                return self.checkWinInList(row)
            if self.checkWinInList(column):
                # Winner is in column!
                return self.checkWinInList(column)

        if self.checkWinInList(diagonal_1):
            # Winner is diagonal!
            return self.checkWinInList(diagonal_1)

        if self.checkWinInList(diagonal_2):
            # Winner is diagonal!
            return self.checkWinInList(diagonal_2)

        if not tic_tac_toe.not_full():
            # It is a draw because there are no spaces left
            return 'DRAW'

        # No one has won yet
        return None

    def checkWinInList(self, myList: list) -> bool:
        player: str = myList[0]
        if player == ' ':
            return False

        for element in myList:
            if element != player:
                return False

        return player

    def get_player_input(self) -> dict:
        while True:
            try:
                position: str = str(input(f"{self.current_player}'s turn. Enter the coordinates: "))
            except EOFError:
                print("You should enter numbers!")
                continue
            except KeyboardInterrupt:
                print("You should enter numbers!")
                continue

            if not position:
                print("You should enter numbers!")
                continue


            if not position[0].isdigit() or not position[2].isdigit():
                print("You should enter numbers!")
                continue

            x: int = int(position[0]) - 1
            y: int = int(position[2]) - 1

            if x > 2 or y > 2 or x < 0 or y < 0:
                print("Coordinates should be from 1 to 3!")
                continue

            if not self.tic_tac_toe.is_available(x, y):
                print("This cell is occupied! Choose another one!")
                continue

            return {'row': x, 'column': y}

    def next_player(self) -> None:
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def AI_move(self):
        best_score: float = -float('inf')
        all_available_spots: list = self.tic_tac_toe.get_all_available()
        best_spot: dict = {}
        for spot in all_available_spots:
            temp_tic_tac_toe: TicTacToeBoard = deepcopy(self.tic_tac_toe)
            temp_tic_tac_toe.insert('C', spot['row'], spot['column'])
            score = self.minimax(tic_tac_toe=temp_tic_tac_toe)

            if score > best_score:
                best_score = score
                best_spot = spot

        return best_spot

    def minimax(self, tic_tac_toe: TicTacToeBoard, depth=0, isMaximizing=False):
        scores: dict = {'C': 1, 'X': -1, 'DRAW': 0}
        result = self.game_won(tic_tac_toe=tic_tac_toe)
        all_available_spots: list = tic_tac_toe.get_all_available()

        # if not all_available_spots:
        #     print(tic_tac_toe)
        #     print('result', result)

        if result:
            print(tic_tac_toe)
            return scores[result]

        if isMaximizing:
            best_score: float = -float("inf")
            for spot in all_available_spots:
                temp_tic_tac_toe: TicTacToeBoard = deepcopy(tic_tac_toe)
                temp_tic_tac_toe.insert('C', spot['row'], spot['column'])
                score = self.minimax(tic_tac_toe=temp_tic_tac_toe, depth=depth + 1, isMaximizing=False)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score: float = float("inf")
            for spot in all_available_spots:
                temp_tic_tac_toe: TicTacToeBoard = deepcopy(tic_tac_toe)
                temp_tic_tac_toe.insert('X', spot['row'], spot['column'])
                score =  self.minimax(tic_tac_toe=temp_tic_tac_toe, depth=depth + 1, isMaximizing=True)
                best_score = min(score, best_score)
            return best_score

game: Game = Game()