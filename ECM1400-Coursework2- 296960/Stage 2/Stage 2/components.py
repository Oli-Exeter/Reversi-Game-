def initialise_board(size=8): #Starts the board
    # we create a list of lists containing elements
    # this will help us mirror cooridinates where
    # y = row and x = col/element
    board = [[" none " for _ in range(size)] for _ in range(size)]

    mid = size // 2
    board[mid - 1][mid - 1] = "Light"
    # we make sure that there are two counters of each colour placed in the middle
    board[mid][mid] = "Light"
    board[mid - 1][mid] = "Dark "
    board[mid][mid - 1] = "Dark "

    return board


def legal_move(colour, coordinate, board_object): #Checks if move is legal
    row, col = coordinate
    if board_object[row][col] == "Dark " or board_object[row][col] == "Light":
        return False
    # move cant be legal if a counter is already in the space

    # we make our directions for future use this will allow
    # us to move around the board, we use a tuple so
    # both the row and col can be changed again acting like x and y
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
    # put them in a list which will be helpfull for checking every direction
    if colour == "Dark ":
        opposite_colour = "Light"
    else:
        opposite_colour = "Dark "
    # labeling what is the default colour and what is the opposite one depending on the input
    for row_delta, col_delta in direction:
        # we want to check every direction from our current coordinates
        new_row = row_delta + row
        # this will create our new coordinates that we will follow along
        new_col = col_delta + col
        size = len(board_object) - 1
        # this is again to set our bounds so that the index
        #doesnt go out of bounds and cause an error
        if 0 <= new_row <= size and 0 <= new_col <= size:
            line_length = 0
            # this willcount the amount of rival counters in between ours
            # to make sure the programme isnt counting two counters of the same colour next
            # to each other as a legal move
            if (
                board_object[new_row][new_col] == opposite_colour
            ):  # we check if there is a rival counter in that direction
                line_length += 1
                # we add 1 so that later on we can flag this as a legal move
                new_row += row_delta
                # we again create new coordinates to follow along
                new_col += col_delta
                # we will follow those new coordinates in the same direction as long as they are rival counters
                while (
                    0 <= new_row <= size
                    and 0 <= new_col <= size
                    and board_object[new_row][new_col] == opposite_colour
                ):
                    line_length += 1
                    new_row += (
                        row_delta  # we again create new coordinates to make the path
                    )
                    new_col += col_delta
            # than when the while statment breaks we check if the new cooridnates are within bounds,
            # that they are the same colour and that there is at least one rival
            # counter between two of the same ones
            if (
                0 <= new_row <= size
                and 0 <= new_col <= size
                and board_object[new_row][new_col] == colour
                and line_length > 0
            ):
                return True
            # This will confirm the move is legal
    return False  # If the programme doesnt return True it will return False to show there is no legal move
