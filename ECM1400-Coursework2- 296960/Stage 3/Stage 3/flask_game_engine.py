from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import components
import json
import bot

othello = Flask(__name__)

othello.secret_key = "password123"


@othello.route("/")  # Here we set up our game
def start():
    session["board"] = components.initialise_board(
        8
    )  # We set up 4 sessions that we're going to use throughout and setup their default values
    session["colour"] = "Dark "
    session["move counter"] = 60
    session["illegal count"] = 0

    return render_template(
        "Othello Board.html", game_board=session["board"]
    )  # Here we update the board in the html file and send it to the browser


@othello.route("/move")
def move():  # Here we will actually make the move happen
    x = int(request.args.get("x"))
    # We get our x and y coordinates
    y = int(request.args.get("y"))
    row = y - 1  # We adjust them for index values
    col = x - 1
    board = session["board"]
    colour = session["colour"]
    move_counter = session["move counter"]
    if (
        components.legal_move(colour, (row, col), board) == True
    ):  # Here if the inputed move is legal we move on to the flipping function
        board[row][col] = colour
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
        ]  # Setting up our directions for flipping function
        if colour == "Dark ":
            opposite_colour = "Light"
        else:
            opposite_colour = "Dark "
            # We set up the opposite colour variable
        for (
            row_delta,
            col_delta,
        ) in direction:
            # We check for every direction around the coordinates
            pieces = []
            # We set up the pieces list which will hold the pieces that we will flip if legal
            new_row = row_delta + row
            # New cooridnates in the same direction
            new_col = col_delta + col
            board_size = len(board) - 1
            # We adjust for the index values
            if 0 <= new_row <= board_size and 0 <= new_col <= board_size:
                # We keep the coordinates within the board parameters
                line_length = 0
                # We set this up to make sure their is at least one rival counters in between
                if board[new_row][new_col] == opposite_colour:
                    # We check for rival counters around coordinate
                    line_length += 1
                    pieces.append((new_row, new_col))
                    # If rival counter we add it to the list of counters to be flipped
                    new_row += row_delta
                    new_col += col_delta
                    while (
                        0 <= new_row <= board_size
                        and 0 <= new_col <= board_size
                        and board[new_row][new_col] == opposite_colour
                    ):
                        # While it's still the rival colour it will keep going in the same direction
                        pieces.append((new_row, new_col))  # Add the counter to the list
                        line_length += 1
                        new_row += row_delta
                        new_col += col_delta
                if (
                    0 <= new_row <= board_size
                    and 0 <= new_col <= board_size
                    and board[new_row][new_col] == colour
                    and line_length > 0
                ):
                    # We check if the move ends on a light counter to make sure it's legal
                    for r, c in pieces:
                        board[r][c] = colour
                        # if true it will flip all the counters in the list

        move_counter -= 1
        # We reduce the move counter by one
        session["board"] = board
        session["colour"] = opposite_colour
        session["move counter"] = move_counter
        # We update the sessions

        stop = False
        # We set this up for later use

        for row_index, row in enumerate(board):
            # We check if the next player has a legal move
            for col_index, col in enumerate(row):
                if col == " none ":
                    if (
                        components.legal_move(
                            opposite_colour, (row_index, col_index), board
                        )
                        is True
                    ):
                        stop = True
                        # If so we make the stop variable true and brake the loop as we dont need to check further moves
                        break
            if stop is True:
                break
            # This breaks the outer loop

        if stop is True:
            session["illegal count"] = 0
            session["colour"] = (
                opposite_colour
                # If they can we switch the colours round and reset illegal count
            )
        elif stop is False:
            session["illegal count"] += 1
            # If not we keep the same colour and pass the opposite players turn as well as increase illegal count by 1
            session["colour"] = colour
            print("No legal move, passing turn")

        if move_counter == 0 or session["illegal count"] >= 2:
            # We check the two conditions needed to end the game if they are true we check who the winner is and end the game
            light_counters = 0
            dark_counters = 0
            # Here we count the counters of each colour
            for row in board:
                for col in row:
                    if col == "Dark ":
                        dark_counters += 1
                    elif col == "Light":
                        light_counters += 1

            if light_counters > dark_counters:
                # Here we decide who the winner is
                winner = "Light is the winner"
            elif dark_counters > light_counters:
                winner = "Dark is the winner"
            elif light_counters == dark_counters:
                winner = "Its a draw"
            return jsonify({"finished": winner, "board": board})
        # We return the infomation back to the player

        bot_move = bot.bot(session["board"])
        # If not we allow the bot to make a move

        if bot_move is not None:
            # If the bot has a move we set up the variables needed to process it's move
            row, col = bot_move
            board = session["board"]
            colour = session["colour"]
            move_counter = session["move counter"]

            board[row][col] = colour
            # We treat the bots turn exactly how we would the player's

            if colour == "Dark ":
                opposite_colour = "Light"
            else:
                opposite_colour = "Dark "
            for row_delta, col_delta in direction:
                pieces = []
                new_row = row_delta + row
                new_col = col_delta + col
                board_size = len(board) - 1
                if 0 <= new_row <= board_size and 0 <= new_col <= board_size:
                    line_length = 0
                    if board[new_row][new_col] == opposite_colour:
                        line_length += 1
                        pieces.append((new_row, new_col))
                        new_row += row_delta
                        new_col += col_delta
                        while (
                            0 <= new_row <= board_size
                            and 0 <= new_col <= board_size
                            and board[new_row][new_col] == opposite_colour
                        ):
                            pieces.append((new_row, new_col))
                            line_length += 1
                            new_row += row_delta
                            new_col += col_delta
                    if (
                        0 <= new_row <= board_size
                        and 0 <= new_col <= board_size
                        and board[new_row][new_col] == colour
                        and line_length > 0
                    ):
                        for r, c in pieces:
                            board[r][c] = colour
                            # We use the same flipping logic

            move_counter -= 1
            # Again we reduce the move count
            session["board"] = board
            session["colour"] = opposite_colour
            session["move counter"] = move_counter

            stop = False

            for row_index, row in enumerate(board):
                for col_index, col in enumerate(row):
                    if col == " none ":
                        if (
                            components.legal_move(
                                opposite_colour, (row_index, col_index), board
                            )
                            is True
                        ):
                            stop = True
                            break
                if stop is True:
                    break
                # We do the same legal move check for the player

            if stop is True:
                session["illegal count"] = 0
                session["colour"] = opposite_colour
            elif stop is False:
                session["illegal count"] += 1
                session["colour"] = colour
                print("No legal move, passing turn")

            if move_counter == 0 or session["illegal count"] >= 2:
                # And again we check the same parameters in the same way we did earlier
                light_counters = 0
                dark_counters = 0
                for row in board:
                    for col in row:
                        if col == "Dark ":
                            dark_counters += 1
                        elif col == "Light":
                            light_counters += 1
                if light_counters > dark_counters:
                    winner = "Light is the winner"
                elif dark_counters > light_counters:
                    winner = "Dark is the winner"
                elif light_counters == dark_counters:
                    winner = "Its a draw"
                return jsonify({"finished": winner, "board": board})

        return jsonify(
            {"status": "success", "board": board, "player": session["colour"]}
        )
    # If the move is valid and there isn't a problem we simply update the game with new information
    else:
        return jsonify({"status": "fail", "message": "invalid move"})
    # if the inputed coordinates are not legal than we return a failed message we don't bother for the bot as it
    # always makes a legal move unless it can't


@othello.route("/save", methods=["POST"])
def save_game():
    game_data = {
        "board": session["board"],
        "colour": session["colour"],
        "move_counter": session["move counter"],
        "illegal_count": session.get("illegal count", 0),
    }
    with open("savegame.json", "w") as saved_game:
        # we create game_data with all the variables needed to setup the game than we open the savegame file
        json.dump(
            game_data, saved_game
        )  # we put all the game data into the file to save
    return render_template(
        "Othello Board.html", game_board=session["board"]
    )  # we return the updated template


@othello.route("/load", methods=["POST"])
def load_game():
    # here we load the game data
    try:
        with open("savegame.json", "r") as saved_game:
            # We open the file
            game_data = json.load(saved_game)
            # retrieve the data
            session["board"] = game_data["board"]
            # update the current sessions
            session["colour"] = game_data["colour"]
            session["move counter"] = game_data["move_counter"]
            return render_template(
                "Othello Board.html", game_board=session["board"]
            )  # return the updated template 
    except FileNotFoundError:
        return redirect(
            url_for("start")
        )  # if the file is not fount than it redirects the player to the start to make a new game


if __name__ == "__main__":
    othello.run(debug=True)
