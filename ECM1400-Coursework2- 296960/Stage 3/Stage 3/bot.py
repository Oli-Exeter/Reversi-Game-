import components


def bot(board):  # This is the function that allows the bot to make a move
    possible_moves = []
    # we create a list of all the possible moves the bot can make
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if components.legal_move("Light", (row_index, col_index), board) is True:
                possible_moves.append((row_index, col_index))
                # We use the legal move component to check for all the possible
                # moves and than add them to the list of possible moves

    if not possible_moves:
        return None
    # We want to create a greedy algorithm
    current_best = possible_moves[0]
    # We create two variables one which will hold the current best move
    # and a second one that will keep check of how many counters that move flips
    current_best_counter = 0
    # We start of with the first move as the best move in the upper variable
    # just simply as a placeholder for now, of course if it does become the best
    # move than it will stay that way

    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)
    up_left = (-1, -1)
    up_right = (-1, 1)
    down_left = (1, -1)
    down_right = (1, 1)
    directions = [up, down, left, right, up_left, up_right, down_left, down_right]
    # We again create our directions and add them to the list

    board_size = len(board) - 1
    # We take away one to take into account that index values begin at 0

    for move in possible_moves:
        # We check every possible move
        counter_count = 0
        # We create a list to count every counter that this current move has flipped
        row, col = move

        for row_delta, col_delta in directions:
            # We again use similiar logic to the legal move logic where we cycle through every
            # direction and follow it if there are rival counters, in this instance because the bot
            # will always play as light, I didn't bother generlising it for both colours
            row_count = 0  # Therefore we check every direction for the possible moves,
            # we also make row count variable in case a direction turns out to be wrong and we have to
            # take away whatever counters we added to the counter count variable
            new_row = row + row_delta  # New coordinates
            new_col = col + col_delta

            while (
                0 <= new_row <= board_size
                and 0 <= new_col <= board_size
                and board[new_row][new_col] == "Dark "
            ):
                # Bounds plus colour check as long as they are true we follow the path
                row_count += 1
                # add to both counts to keep track
                counter_count += 1
                new_row += row_delta
                new_col += col_delta

            if (
                0 <= new_row <= board_size
                and 0 <= new_col <= board_size
                and board[new_row][new_col] == "Light"
            ):
                continue
            else:
                counter_count -= row_count
                # If it doesnt end on the light counter the move is illegal and therefore we take
                # away from the total count

        if counter_count > current_best_counter:
            current_best = (row, col)
            current_best_counter = counter_count
            # Here we check and update which move is the best by comparing how many counters they flip

    return current_best


# This will return the tuple for the coordinates of which move turned out to be the best 9
