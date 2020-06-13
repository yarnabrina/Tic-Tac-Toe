"""Define functions to play the game."""

import datetime
import random
import shelve
import typing

INVALID_ENTRY_MESSAGE = "\nNot a valid entry:"


def choose_board_size(default_board_size: int) -> int:
    """Select the board size based on user input and default value.

    Parameters
    ----------
    default_board_size : int
        default size of the game board

    Returns
    -------
    int
        size of the game board
    """
    print("\nChoose the size of the Tic Tac Toe board.")
    print(
        f"\nPress <ENTER> or <RETURN> to use the default board of size {default_board_size}."
    )
    while True:
        chosen_board_size = input("\nEnter Board Size:\t")
        try:
            if not chosen_board_size:
                print(
                    "\nYou have selected to play with the default board size.")
                return default_board_size

            chosen_board_size = int(chosen_board_size)
            if chosen_board_size < 3:
                print(
                    "\nNot a valid entry: it must be a positive integer >= 3.")
            else:
                print(
                    f"\nYou have selected a board of size {chosen_board_size}.")
                return chosen_board_size
        except ValueError as error_message:
            print(INVALID_ENTRY_MESSAGE, error_message)


def choose_number_of_human_players() -> int:
    """Select type of the game.

    Returns
    -------
    int
        number of human players
    """
    print(
        "\nChoose whether you will play against a dumb machine, or with one of your friend."
    )
    while True:
        chosen_number_of_human_players = input(
            "\nEnter Number of Human Players:\t")
        try:
            chosen_player_number = int(chosen_number_of_human_players)
            if chosen_player_number not in [1, 2]:
                print("\nNot a valid entry: it has to be 1 or 2.")
            else:
                if chosen_player_number == 1:
                    print("\nYou selected to play alone.")
                else:
                    print("\nYou selected to play with a friend.")
                return chosen_player_number
        except ValueError as error_message:
            print(INVALID_ENTRY_MESSAGE, error_message)


def choose_game_order() -> int:
    """Gets order of the human player.

    Returns
    -------
    int
        whether the human player to play first or second
    """
    print("\nChoose whether you will play first or second.")

    while True:
        chosen_game_order_of_human_player = input("\nEnter your game order:\t")
        try:
            chosen_game_order = int(chosen_game_order_of_human_player)
            if chosen_game_order not in [1, 2]:
                print("\nNot a valid entry: it should be either 1, or 2.")
            else:
                if chosen_game_order == 1:
                    print("\nYou selected to play first.")
                else:
                    print("\nYou selected to play second.")
                return chosen_game_order
        except ValueError as error_message:
            print(INVALID_ENTRY_MESSAGE, error_message)


class TicTacToe:
    """Initiate the game.

    Parameters
    ----------
    name_of_file_containing_game : str
        file containing saved game
    """

    def __init__(self, name_of_file_containing_game) -> None:
        if not name_of_file_containing_game:
            print("\nStart with configuring the game as per your preferences.")
            self.board_size = choose_board_size(default_board_size=3)
            chosen_number_of_human_players = choose_number_of_human_players()
            if chosen_number_of_human_players == 2:
                self.first_player_name, self.second_player_name = ("User 1",
                                                                   "User 2")
            else:
                chosen_game_order = choose_game_order()
                self.first_player_name, self.second_player_name = (
                    "User",
                    "Machine") if chosen_game_order == 1 else ("Machine",
                                                               "User")
            self.played_moves = []
        else:
            with shelve.open(name_of_file_containing_game.rstrip(
                    '.db')) as file_containing_game:
                self.board_size = file_containing_game['board_size']
                self.first_player_name = file_containing_game[
                    'first_player_name']
                self.second_player_name = file_containing_game[
                    'second_player_name']
                self.played_moves = file_containing_game['played_moves']

        self.first_player_type, self.second_player_type = ("[X]", "[O]")

    @property
    def current_board_situation(self) -> typing.List[str]:
        """Create structure of current board.

        Returns
        -------
        typing.List[str]
            played and available positions
        """
        initialisation = list(
            map(lambda t: str(t + 1), range(self.board_size**2)))
        for move_counter, each_move in enumerate(self.played_moves):
            initialisation[
                int(each_move) -
                1] = self.first_player_type if move_counter % 2 == 0 else self.second_player_type
        return initialisation

    @property
    def playable_board_positions(self) -> typing.List[str]:
        """Store available positions.

        Returns
        -------
        typing.List[str]
            list of available board positions
        """
        return list(
            set(self.current_board_situation) -
            {self.first_player_type, self.second_player_type})

    def __str__(self) -> str:
        """Contains board structure.

        Returns
        -------
        str
            board structure
        """
        board_situation = "\nThe board situation is as follows:\n"
        for row_counter in range(self.board_size):
            for column_counter in range(self.board_size):
                current_cell = self.current_board_situation[(self.board_size *
                                                             row_counter) +
                                                            column_counter]
                board_situation += current_cell
                if column_counter != self.board_size:
                    board_situation += "\t"
            board_situation += "\n"
        return board_situation

    def check_rows_columns_diagonals(self, player_type: str) -> bool:
        """Check whether current player wins or not.

        Parameters
        ----------
        player_type : str
            whether current player played first or second

        Returns
        -------
        bool
            whether current player won or not
        """
        for row_counter in range(self.board_size):
            if all(self.current_board_situation[(self.board_size *
                                                 row_counter) +
                                                column_counter] == player_type
                   for column_counter in range(self.board_size)):
                return True

        for column_counter in range(self.board_size):
            if all(self.current_board_situation[column_counter +
                                                (self.board_size *
                                                 row_counter)] == player_type
                   for row_counter in range(self.board_size)):
                return True

        if all(self.current_board_situation[(self.board_size * row_counter) +
                                            column_counter] == player_type
               for row_counter, column_counter in zip(range(self.board_size),
                                                      range(self.board_size))):
            return True

        if all(self.current_board_situation[(self.board_size * row_counter) +
                                            (self.board_size - 1) -
                                            column_counter] == player_type
               for row_counter, column_counter in zip(range(self.board_size),
                                                      range(self.board_size))):
            return True

        return False

    def check_result(self, player_type: str, player_name: str):
        """Check whether game is over or not.

        Parameters
        ----------
        player_type : str
            whether it is the first or second player
        player_name : str
            name of the player

        Raises
        ------
        GameCompleted
            player wins the current board
        GameCompleted
            current board is complete
        """
        player_is_winner = self.check_rows_columns_diagonals(player_type)
        if player_is_winner:
            print(f"\n{player_name} wins!")
            raise GameCompleted

        if not self.playable_board_positions:
            print("\nIt's a draw!")
            raise GameCompleted

    def make_move(self, player_name: str) -> str:
        """Register one move of current player.

        Parameters
        ----------
        player_name : str
            name of the current player

        Returns
        -------
        str
            current move of the current player

        Raises
        ------
        GameInterrupted
            current player chooses to quit the game
        """
        if player_name == "Machine":
            print("\nMachine's turn is over.")
            return random.choice(self.playable_board_positions)

        print(f"\n{player_name}, it's your turn now.")
        print(self)
        while True:
            chosen_position = input("\nEnter a position:\t")
            try:
                if chosen_position.upper() == "Q":
                    print("\nSorry to see you quit!")
                    while True:
                        check_save = input(
                            "\nDo you want to save the game? [Y]es / [N]o:\t")
                        if check_save.upper() not in ["Y", "N"]:
                            print("\nNot a valid entry: it has to be Y or N.")
                        else:
                            raise GameInterrupted if check_save.upper(
                            ) == "N" else GameSaved
                elif int(chosen_position) in list(
                        map(int, self.playable_board_positions)):
                    print(
                        f"\n{player_name}, your turn is over, and you chose {chosen_position}."
                    )
                    while True:
                        check_undo = input("\n[C]onfirm / [U]ndo?:\t")
                        if check_undo.upper() in ["C", "U"]:
                            return chosen_position if check_undo.upper(
                            ) == "C" else self.make_move(player_name)
                        print("\nNot a valid entry: it has to be C or U.")
                else:
                    print(
                        "\nNot a valid entry: this position is not available.")
            except ValueError as error_message:
                print(INVALID_ENTRY_MESSAGE, error_message)

    def game_play(self):
        """Define main gameplay"""
        print("\nLet's start the game. You can press Q anytime to quit.")

        try:
            while True:
                current_player_name, current_player_type = (
                    self.first_player_name, self.first_player_type
                ) if len(self.played_moves) % 2 == 0 else (
                    self.second_player_name, self.second_player_type)
                self.played_moves.append(self.make_move(current_player_name))
                self.check_result(current_player_type, current_player_name)

        except GameCompleted:
            print(self)
            print("\nThe game is over!")

            while True:
                check_replay = input(
                    "\nDo you want to play with the same configuration again? [Y]es / [N]o:\t"
                )
                if check_replay.upper() not in ["Y", "N"]:
                    print("\nNot a valid entry: it has to be Y or N.")
                elif check_replay.upper() == "N":
                    print("\nHave a nice day!")
                    break
                else:
                    self.played_moves = []
                    self.game_play()
                    break

        except GameInterrupted:
            print("""\nYou interrupted the game by pressing Q.
                  Also you chose not to save the game.
                  Hope to see you coming back soon!""")

        except GameSaved:
            with shelve.open("Tic_Tac_Toe_Saved_At_" + datetime.datetime.now(
            ).strftime("%Y-%m-%dT%H:%M:%S")) as open_file_to_save_game:
                open_file_to_save_game['board_size'] = self.board_size
                open_file_to_save_game[
                    'first_player_name'] = self.first_player_name
                open_file_to_save_game[
                    'second_player_name'] = self.second_player_name
                open_file_to_save_game['played_moves'] = self.played_moves
            print("""\nYou interrupted the game by pressing Q.
                  The game is saved for you.
                  Hope to see you coming back soon!""")\


class GameCompleted(Exception):
    """Custom exception class for game completion"""


class GameInterrupted(Exception):
    """Custom exception class for game interruption"""


class GameSaved(Exception):
    """Custom exception class for game save"""
