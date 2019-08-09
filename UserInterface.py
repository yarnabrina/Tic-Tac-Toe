import glob
import GameCodes

print("\nWelcome to the game of Tic Tac Toe!")

saved_games = glob.glob("Tic_Tac_Toe_Saved_At_*-*-*_*:*:*.db")

if saved_games:
	print("\nThe following saved games are available:")
	print("\n".join(str(counter + 1) + ". " + saved_game for counter, saved_game in enumerate(saved_games)))

	while True:
		choose_saved_game = input("\nEnter the corresponding index to load a particular game, else enter 0:\t")
		try:
			if int(choose_saved_game) not in range(len(saved_games) + 1):
				print("\nNot a valid entry: either choose one of the files, or zero.")

			elif choose_saved_game == 0:
				Game = GameCodes.TicTacToe(name_of_file_containing_game = "")
				break

			else:
				Game = GameCodes.TicTacToe(name_of_file_containing_game = saved_games[int(choose_saved_game) - 1])
				break

		except ValueError as error_message:
			print("\nNot a valid entry:", error_message)

else:
	Game = GameCodes.TicTacToe(name_of_file_containing_game = "")

Game.GamePlay()
