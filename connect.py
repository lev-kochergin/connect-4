def get_players() -> dict[str, str]:
    """
    Prompts players for their names.

    Returns:
    * players (`dict[str, str]`): The player's names, mapping from 
      `"X"` or `"O"` to the corresponding player.
    """
    player_one: str = input("Enter Player 1's (X) name: ")
    player_two: str = input("Enter Player 2's (O) name: ")
    return {"X": player_one.strip(), "O": player_two.strip()}


def get_col(board: list[list], index: int) -> list:
    """
    Returns a column from list of lists, as a list.
    
    Arguments:
    * board (`list[list]`): The rectangular list of lists that 
      contains the tiles and open spaces.
    * index (`int`): The column index to be retrieved.
    
    Returns:
    * col (`list`): The contents of the specified column in 
      the list of lists.
    """
    return [i[index] for i in board]


def get_open(board: list[list]) -> list[int]:
    """
    Returns the indexes of the open columns in a board. A column is 
    considered open if the top row of the column is empty.

    Arguments:
    * board (`list[list]`): The rectangular list of lists that 
      contains the tiles and open spaces.

    Returns:
    * open_cols (`list`): The column names (starting from `1`, not `0`)
      that are open and can have a tile placed in them.
    """
    open_c = []
    for count, item in enumerate(board[0]):
        if item == "":
            open_c.append(count + 1)
    return open_c


def print_board(board: list[list]) -> None:
    """
    Displays a board to the players.
    
    Arguments:
    * board (`list[list]`): The rectangular list of lists to be displayed.
    """
    
    # print the open column indexes
    open_cols = get_open(board)
    print(1 if 1 in open_cols else " ", end="")
    for i in range(2, len(board[0]) + 1):
        print(f"   {i if i in open_cols else ' '}", end="")
    
    # print the board contents
    print("")
    for row in board:
        print(" " if row[0] == "" else row[0], end="")
        for item in row[1:]:
            print(" | " + (" " if item == "" else item), end="")
        print("")


def place_tile(board: list[list], player_tile: str) -> None:
    """
    Prompts a player to pick a column to place a tile in.
    
    Arguments:
    * board (`list[list]`): The rectangular list of lists that 
      contains the tiles and open spaces.
    * player_tile (`str`): The tiles the active player is playing with.
    """

    # get a valid column to place a tile into
    index = ask_int("Choose a column to place a tile in: ")
    while not index in get_open(board):
        print(f"Column {index} is full or not a column, try again.")
        index = ask_int("Choose a column to place a tile in: ")

    # add the tile into the board.
    column = get_col(board, index - 1)
    first_open = column[::-1].index("")
    board[len(board) - first_open - 1][index - 1] = player_tile


def ask_int(prompt: str) -> int:
    """
    Helper method to get an int from a user..
    
    Argument:
    * prompt (`str`): The question to as the user.

    Returns:
    * number (`int`): The numeric value retrieved from the user.
    """

    num: str = input(prompt)
    while not num.isnumeric():
        print(f'"{num}" is not a number, please provide valid input.')
        num: str = input(prompt)
    return int(num)


def check_win(board: list[list], tile: str) -> bool:
    """
    Checks if a player has won the game.

    Arguments:
    * board (`list[list]`): The rectangular list of lists that 
      contains the tiles and open spaces.
    * tile (`str`): The tiles the active player is playing with.

    Returns:
    * win (`bool`): If the active player has won the game.
    """

    height = len(board[0])
    width = len(board)

    # check horizontal segments
    for y in range(height):
        for x in range(width - 3):
            if all(
                (
                    board[x][y] == tile,
                    board[x + 1][y] == tile,
                    board[x + 2][y] == tile,
                    board[x + 3][y] == tile,
                )
            ):
                return True

    # check vertical segments
    for x in range(width):
        for y in range(height - 3):
            if all(
                (
                    board[x][y] == tile,
                    board[x][y + 1] == tile,
                    board[x][y + 2] == tile,
                    board[x][y + 3] == tile,
                )
            ):
                return True

    # check / diagonal spaces
    for x in range(width - 3):
        for y in range(3, height):
            if all(
                (
                    board[x][y] == tile,
                    board[x + 1][y - 1] == tile,
                    board[x + 2][y - 2] == tile,
                    board[x + 3][y - 3] == tile,
                )
            ):
                return True

    # check \ diagonal spaces
    for x in range(width - 3):
        for y in range(height - 3):
            if all(
                (
                    board[x][y] == tile,
                    board[x + 1][y + 1] == tile,
                    board[x + 2][y + 2] == tile,
                    board[x + 3][y + 3] == tile,
                )
            ):
                return True

    return False


def start():
    """
    Main function to start a game.
    """

    players: dict[str, str] = get_players()
    print("")
    board: list[list] = [["" for _ in range(7)] for _ in range(6)]
    finished = False
    active_player = "X"

    while not finished:
        print(f"-- It's {players[active_player]}'s ({active_player}) turn --\n")
        print_board(board)
        print("")
        place_tile(board, active_player)
        print("")

        finished = check_win(board, active_player)

        if not get_open(board):
            print("This game ended in a tie!")
            break

        if not finished:
            active_player = next(i for i in players.keys() if i != active_player)

    if finished:
        print(f"{players[active_player]} ({active_player}) won the game! Congrats!\n")
        print_board(board)

    if input("\nDo you want to play again? (yes/no): ").lower() == "yes":
        print("")
        start()


if __name__ == "__main__":
    # (when file is run directly)
    print("! Welcome to Connect Four !\n")
    start()
