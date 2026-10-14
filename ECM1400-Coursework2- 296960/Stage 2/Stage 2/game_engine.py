def cli_coords_input(): #Inputs valid coordinates
    # True statment will make sure the file keep running even if the user enters a wrong value
    while True:
        try:
            x_co = int(input("Please input the X coordinate between 1-8: "))
            y_co = int(input("Please input the y coordinate between 1-8: "))
            coordinates = (
                y_co - 1,
                x_co - 1,
            )
            # we take away to account for index position
            if x_co > 8 or y_co > 8 or x_co < 1 or y_co < 1:
                # we put bounds on the input so that it doesnt
                # go over the borders of the board and cause an error down the line
                print("Invalid input please input coordinates within the range")
            else:
                return coordinates
        except ValueError:
            # error handling in case the user put in letters
            print("Please enter an integer")


def simple_game_loop(): # Lets us play a game
    import components

    # we import some functions to make coding quicker and cleaner

    print(
        "Hello World! Welcome to the game of othello, "
        "please be familiar with the rules before starting the game"
    )
    # Starting message
    size = 8
    board = components.initialise_board(size)
    move_counter = 60
    colour = "Dark "
    illegal_count = 0
    light_counter = 0
    dark_counter = 0
    # here we set up the different varaibles that are going to be used throughout the loop
    while move_counter > 0:
        # We start the loop and it will keep going until either 
        #of the two conditions are met here is one until we still have moves left
        stop = False
        # Another condition that we want to reset each time
        if illegal_count == 2:
            # Here we have the second condition if there are no 
            #legal moves on the board for both players the game will end
            print("Neither Player can move end of the game")
            return board
        for row_index, row in enumerate(board):
            # In this function we check every space to see if there is a legal move
            for col_index, col in enumerate(row):
                if col == " none ":
                    if (
                        components.legal_move(colour, (row_index, col_index), board)
                        is True
                    ):
                        print("You can make a move")
                        stop = True
                        break
            # If there is we break the loop to hasten the programme 
            #and not print out the message each time
            if stop:
                break
        # breaking the outer loop
        if not stop:
            # there are no legal moves, so we increase illegal count
            #to represent that one player can't make a move
            illegal_count += 1
            print("You don't have any legal moves to play. Next player")
            if colour == "Dark ":
                colour = "Light"
            else:
                colour = "Dark "
            continue
        # we than change the colour to the opposite player so that
        #they can make a move and not decrease the counter by accident
        else:
            illegal_count = 0
        # if there is a legal move illegal count resets to 0 as we
        #need two in a row to know both players can't make a move

        player_coordinates = cli_coords_input()
        while components.legal_move(colour, player_coordinates, board) is False:
            print("Illegal move please try again")
            player_coordinates = cli_coords_input()
        # This will run until coordinates entered by the user are valid

        # This code runs similiar to the legal_move 
        #function in components, I'll describe the differances here
        up = (-1, 0)
        down = (1, 0)
        left = (0, -1)
        right = (0, 1)
        up_left = (-1, -1)
        up_right = (-1, 1)
        down_left = (1, -1)
        down_right = (1, 1)
        direction = [
            up,
            down,
            left,
            right,
            up_left,
            up_right,
            down_left,
            down_right,
        ]
        row, col = (
            player_coordinates
            # row and col are manually entered by the user we than extract the individual coordinates from the tuple
        )
        if colour == "Dark ":
            opposite_colour = "Light"
        else:
            opposite_colour = "Dark "
        board[row][col] = colour
        # we already know the move is legal so we can go ahead and place a counter there
        for row_delta, col_delta in direction:
            pieces = []
            # we create a list of all the pieces that need changing, this also resets the list 
            #when we check another direction, so that we don't accidently change counters we didn't mean to later on
            new_row = row_delta + row
            # we create new coordinates to check in the direction we want to go in
            new_col = col_delta + col
            board_size = len(board) - 1
            if 0 <= new_row <= board_size and 0 <= new_col <= board_size:
                line_length = 0
                if board[new_row][new_col] == opposite_colour:
                    # we iterate over every element around our coordinates and check wether each one is a rival counter
                    line_length += 1
                    # we create line length to make track the amount of counters which helps us later check if we're its a valid move
                    pieces.append((new_row, new_col))
                    # we add the new rival counter coordinates to our list of pieces
                    new_row += row_delta
                    # moving onto the next piece in line
                    new_col += col_delta
                    while (
                        0 <= new_row <= board_size
                        and 0 <= new_col <= board_size
                        and board[new_row][new_col] == opposite_colour
                    ):
                        # we make sure to check the bounds first to not get an index error and here
                        # we continue in the direction so long as there are rival counters there
                        pieces.append((new_row, new_col))
                        # we repeat what we did for the first counter add it to the list make new coordinates etc
                        line_length += 1
                        new_row += row_delta
                        new_col += col_delta
                if (
                    0 <= new_row <= board_size
                    and 0 <= new_col <= board_size
                    and board[new_row][new_col] == colour
                    and line_length > 0
                ):
                    # If we stumble onto the same coloured piece again we can confirm that it's ok for us to change
                    # these pieces again we check the bounds and that line length is bigger than
                    #0 to make sure there actually where some rival counters between the current players counters
                    for r, c in pieces:
                        board[r][c] = colour
        # Here we simply select and flip every piece in our list aka those that where in line
        move_counter -= 1
        # we reduce the move counter for this move
        if colour == "Dark ":
            # we now change the colour for the next players turn
            colour = "Light"
        else:
            colour = "Dark "
        print(board)

    for row in board:
        # When the moves eventually run out or illegal move reaches two it will
        #move onto the game end which now checks which player has won
        for col in row:
            if col == "Light":
                light_counter += 1
            elif col == "Dark ":
                dark_counter += 1
    if light_counter > dark_counter:
        print("Light wins")
    elif dark_counter > light_counter:
        print("Dark wins")
    elif light_counter == dark_counter:
        print("It's a tie")
    print("Light:", light_counter, "Dark:", dark_counter)

    return board


if __name__ == "__main__":
    simple_game_loop()
