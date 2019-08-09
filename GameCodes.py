import datetime
import random
import shelve

def ChooseBoardSize(default_board_size):
	print("\nChoose the size of the Tic Tac Toe board.")
	print("\nPress <ENTER> or <RETURN> to use the default board of size {}.".format(default_board_size))

	while True:
		choose_board_size = input("\nEnter Board Size:\t")

		try:
			if not choose_board_size:
			    print("\nYou have selected to play with the default board size.")
			    return(default_board_size)

			elif int(choose_board_size) < 3:
				print("\nNot a valid entry: it must be a positive integer >= 3.")

			else:
			    print("\nYou have selected a board of size {}.".format(int(choose_board_size)))
			    return(int(choose_board_size))

		except ValueError as error_message:
		    print("\nNot a valid entry:", error_message)

def ChooseNumberOfHumanPlayers():
	print("\nChoose whether you will play against a dumb machine, or with one of your friend.")

	while True:
		choose_number_of_human_players = input("\nEnter Number of Human Players:\t")

		try:
			if int(choose_number_of_human_players) not in [1, 2]:
				print("\nNot a valid entry: it has to be 1 or 2.")

			else:
				print("\nYou selected to play alone.") if int(choose_number_of_human_players) == 1 else print("\nYou selected to play with a friend.")
				return(int(choose_number_of_human_players))

		except ValueError as error_message:
			print("\nNot a valid entry:", error_message)

def ChooseGameOrder():
	print("\nChoose whether you will play first or second.")

	while True:
		choose_game_order_of_human_player = input("\nEnter your game order:\t")

		try:
			if int(choose_game_order_of_human_player) not in [1, 2]:
				print("\nNot a valid entry: it should be either 1, or 2.")

			else:
				print("\nYou selected to play first.") if int(choose_game_order_of_human_player) == 1 else print("\nYou selected to play second.")
				return(int(choose_game_order_of_human_player))

		except ValueError as error_message:
			print("\nNot a valid entry:", error_message)

class TicTacToe:

	def __init__(self, name_of_file_containing_game):
		if not name_of_file_containing_game:
			print("\nStart with configuring the game as per your preferences.")

			self.board_size = ChooseBoardSize(default_board_size = 3)

			choose_number_of_human_players = ChooseNumberOfHumanPlayers()

			if choose_number_of_human_players == 2:
				self.first_player_name, self.second_player_name = ("User 1", "User 2")

			else:
				choose_game_order = ChooseGameOrder()
				self.first_player_name, self.second_player_name = ("User", "Machine") if choose_game_order == 1 else ("Machine", "User")

			self.played_moves = []

		else:
			with shelve.open(name_of_file_containing_game.rstrip('.db')) as file_containing_game:
				self.board_size = file_containing_game['board_size']

				self.first_player_name = file_containing_game['first_player_name']
				self.second_player_name = file_containing_game['second_player_name']

				self.played_moves = file_containing_game['played_moves']

		self.first_player_type, self.second_player_type = ("[X]", "[O]")

	@property
	def current_board_situation(self):
		initialisation = list(map(lambda t: str(t + 1), range(self.board_size ** 2)))
		for move_counter, each_move in enumerate(self.played_moves):
			initialisation[int(each_move) - 1] = self.first_player_type if move_counter % 2 == 0 else self.second_player_type

		return(initialisation)

	@property
	def playable_board_positions(self):
		return(list(set(self.current_board_situation) - {self.first_player_type, self.second_player_type}))

	def __str__(self):
		return("\nThe board situation is as follows:\n" + "\n".join(("\t".join((self.current_board_situation[(self.board_size * row_counter) + column_counter] for column_counter in range(self.board_size))) for row_counter in range(self.board_size))))

	def CheckWRowsColumnsDiagonals(self, player_type):
		for row_counter in range(self.board_size):
			if all(self.current_board_situation[(self.board_size * row_counter) + column_counter] == player_type for column_counter in range(self.board_size)):
				return(True)

		for column_counter in range(self.board_size):
			if all(self.current_board_situation[column_counter + (self.board_size * row_counter)] == player_type for row_counter in range(self.board_size)):
				return(True)

		if all(self.current_board_situation[(self.board_size * row_counter) + column_counter] == player_type for row_counter, column_counter in zip(range(self.board_size), range(self.board_size))):
			return(True)

		if all(self.current_board_situation[(self.board_size * row_counter) + (self.board_size - 1) - column_counter] == player_type for row_counter, column_counter in zip(range(self.board_size), range(self.board_size))):
			return(True)

		return(False)

	def CheckResult(self, player_type, player_name):
		player_is_winner = self.CheckWRowsColumnsDiagonals(player_type)

		if player_is_winner:
			print("\n{} wins!".format(player_name))
			raise GameCompleted

		elif not self.playable_board_positions:
			print("\nIt's a draw!")
			raise GameCompleted

	def MakeMove(self, player_name):
		if player_name == "Machine":
			print("\nMachine's turn is over.")
			return(random.choice(self.playable_board_positions))

		else:
			print("\n{}, it's your turn now.".format(player_name))
			print(self)

			while True:
				choose_position = input("\nEnter a position:\t")

				try:
					if choose_position.upper() == "Q":
						print("\nSorry to see you quit!")

						while True:
							check_save = input("\nDo you want to save the game? [Y]es / [N]o:\t")

							if check_save.upper() not in ["Y", "N"]:
								print("\nNot a valid entry: it has to be Y or N.")

							else:
								raise GameInterrupted if check_save.upper() == "N" else GameSaved

					elif int(choose_position) in list(map(int, self.playable_board_positions)):
						print("\n{}, your turn is over, and you chose {}.".format(player_name, choose_position))

						while True:
							check_undo = input("\n[C]onfirm / [U]ndo?:\t")

							if check_undo.upper() in ["C", "U"]:
								return(choose_position if check_undo.upper() == "C" else self.MakeMove(player_name))

							else:
								print("\nNot a valid entry: it has to be C or U.")

					else:
						print("\nNot a valid entry: this position is not available.")

				except ValueError as error_message:
					print("\nNot a valid entry:", error_message)

	def GamePlay(self):
		print("\nLet's start the game. You can press Q anytime to quit.")

		try:
			while True:
				current_player_name, current_player_type = (self.first_player_name, self.first_player_type) if len(self.played_moves) % 2 == 0 else (self.second_player_name, self.second_player_type)

				self.played_moves.append(self.MakeMove(current_player_name))
				self.CheckResult(current_player_type, current_player_name)

		except GameCompleted:
			print(self)
			print("\nThe game is over!")

			while True:
				check_replay = input("\nDo you want to play with the same configuration again? [Y]es / [N]o:\t")

				if check_replay.upper() not in ["Y", "N"]:
					print("\nNot a valid entry: it has to be Y or N.")

				elif check_replay.upper() == "N":
					print("\nHave a nice day!")
					break

				else:
					self.played_moves = []
					self.GamePlay()
					break

		except GameInterrupted:
			print("\nYou interrupted the game by pressing Q, and chose not to save the game.\n\ChooseNumberOfHumanPlayers!")

		except GameSaved:
			with shelve.open("Tic_Tac_Toe_Saved_At_" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) as open_file_to_save_game:
				open_file_to_save_game['board_size'] = self.board_size

				open_file_to_save_game['first_player_name'] = self.first_player_name
				open_file_to_save_game['second_player_name'] = self.second_player_name

				open_file_to_save_game['played_moves'] = self.played_moves

			print("\nYou interrupted the game by pressing Q, and the game is saved for you.\n\nHope to see you coming back soon!")

class GameCompleted(Exception):
	pass

class GameInterrupted(Exception):
	pass

class GameSaved(Exception):
	pass
