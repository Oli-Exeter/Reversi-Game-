
# Read Me 


## Introduction

Here we will describe how each module of the courseworks works and how they work together to give the final product.


## Components.Py

The first file contains the basic functions needed for the game loop to function.

1) Initialise Board

This module is relatively straightforward. It makes a set of lists depending on the board size inputed by the user. Each of the lists represents a row, and each element inside those lists represents a column. This 
allows the programme to consider elements as board squares with the purpose of using x and y-coordinates in a natural way.

After the blank board has been set up, the program calculates the centre by dividing the size by two. It then sets the initial white and dark pieces in their starting positions by identifying these starting 
coordinates through adding and subtracting from the centre position. This was chosen as the easiest and most efficient method.

This is the flowchart for this algorithm - 

[Initialise board](Flowcharts/Initialise%20board.pdf)

2) Legal Move

This module legal_move requires three input values from the user: board, colour, and coordinates. The purpose of this module is to compute whether the given coordinate is a legal move or not.
The program starts by unpacking the coordinate tuple into row and column variables, acting as the board's x and y coordinates. It checks whether the selected square already contains a counter; if it does, the 
function returns with the value False.

If not, it constructs a set of tuples representing all possible directions of movements. These directions are then saved into a list for use throughout the module; this enables the programme to simply iterate over 
them, rather than having to handle each case individually. It also sets an opposite_colour variable for later use in the module to identify rival counters.

This algorithm takes in the input coordinate and iterates through every direction. It advances, one step further along that direction, if it has encountered a rival counter, by adding the directional offsets to the 
coordinate. It checks whether this new coordinate is still within the boundary of the board. It also has a line_length variable tracking how many opposing counters have been encountered so that adjacent allied 
counters are not mistakenly taken as a valid capture.

If the square contains a rival counter, the programme proceeds in that direction, updating the coordinates at each step. It stops when the next square is not a rival counter. Then it checks if the terminating square 
is an allied counter, and if the coordinate remains within the bounds. If these two cases are satisfied, it returns True.

Because a move only needs to be valid in one direction, the programme stops searching when any direction returns True. When all the directions fail, the function returns False. This design is because manually 
iterating through each direction provides a clear and reliable method for validating moves.


This is the flowchart for this algorithm- 

[Legal move](Flowcharts/Legal%20move.pdf)

## Game_engine.py

The second file, game_engine.py, will make use of several functions from components.py.

1) cli Coordinate Input

This module has a while loop, requesting the player input continuously, in case of errors however ends when a user has inputed valid values. It keeps the input within the bounds and handles invalid entries-for 
example, strings or wrongly formatted values, asking the user again. It also converts inputed coordinates to zero-based indices suitable for internal processing.

This is the flowchart for this algorithm-

[cli coordinates inpput](Flowcharts/cli%20coords%20input.pdf)

2) Simple Game Loop

This module contains the main loop of the game. It starts off with a welcome message and initializes all variables that are to be used during this session, such as the number of moves left.

Game state is maintained via a while loop. The only two conditionals that terminate the loop are if the move counter shows zero which implies that the board is full or if the illegal-move counter reaches two, which 
is the signal that neither player has a legal move. 

Within the loop, the programme checks first whether the next player can make a legal move, and if not, increments an illegal-move counter and passes the turn to another player. If they do have a legal move, the programme proceeds with the movement phase, confirming, by using legal_move on the inputed coordinates from the cli input module, that the move is indeed valid.

The next step is the flipping logic. The alogorithm is exactly the same as in legal move, where each direction is checked around the inputed coordinates, except this time each rival counter is added to a list of counters which are later changed to the allied colour given that it's appropriate to do so, if not the list is cleared of the new counters and the algorithm goes to check the next direction until all directions are exghausted.

This is the flowchart for this alogorithm - 

[Simple game loop](Flowcharts/Simple%20game%20loop.pdf)

## Flask Server

This is the main controlling file for the online version of the game. It addresses the routing and interactions between the browser and the more complex backend operations, and it maintains all data necessary for the game within sessions created via Flask. It also engages with components and the bot module to enable it to make its move. There are two versions of this programme one in stage 2 and the other in stage 3, the differance being is that the one in stage 2 does not include the bot allowing a game between 2 people whereas stage 3 does include a bot allowing for a player v ai game. The reason for this is due confusion on whether the finished product was to be included in stage 2 also or just in stage 3 either way both versions of the game are available to play and fully work. The algorithms in both don't differ much, one being based of the other, with the differance being that the code in stage 2 doesn't inculde the bot movement therefore any part relating to that function is to be ignored if you are looking on how the code for stage 2 works.

## Start Route("/")-

Initialising the Game - As soon as the user accesses the webpage, this route will be triggered. Within this function, we have set up four session variables that will be our main source of storage.
 The board initialization occurs via the call to the initialise_board function from the components module. It defaults with a size attribute set at 8.
 The initial colour will be set as "Dark" because it plays first.
 The counter for moves is set at 60, which represents the maximum number of moves that can be made before reaching maximum board capacity.
 The number of illegal moves made will be set at 0 and will increase if there are no legal moves.

We have set up our sessions and will then render an HTML page and send our board created with these sessions to be drawn on an HTML page. For both stage 2 and 3 algorithms this process is the same.

## Move Route ("/move")

The move route in the flask engine algorithm is based on the simple game loop algorithm made in previous file therefore there are some parts of the code that have been recycled.

This path is involved in implementing the move as soon as the player clicks on the board.

Reading Input - It first reads the coordinates x and y as an input from the browser. Both x and y coordinates are passed as strings. We convert them into integers and then reduce them by 1 so that they correspond with 0 based indexing.

Checking Validity - We pull out our session variables. We then make a call to legal_move from components. If it's an illegal move, we return a response indicating this information requesting another input.

Placing the Piece - Having determined that we have a legal move, we put our current piece type on the board at the position. We then prepare all eight directions with which we will scan for flipping in our algorithm similiarly and for the same reasons as have been done in the previous modules such as legal move or simple game loop.

Flipping pieces - We identify our opposite colour based on who made the previous move. For our flipping logic the coordinates are followed step-by-step for every direction. We search for opposite numbers and then put them into a list named as pieces, we move in the same direction until we either reach the end of the board or encounter a piece that isn't our opponents, if this line ends at an allied piece and we have at least one rival counter in-between, then all values in the pieces list are flipped to the allied colour.

After a move, the move counter will be decremented, and variables board and colour will be updated for the next move.

Checking for Legal Moves - Before making a permanent changeover among players, it checks for legal moves for the next colour. It does so by checking the whole board for an empty square and examining if it is a legal move for the next colour. The reason it's done before the opposite player's turn is because the checks for move counter and legal move happen at the end, as this algorithm doesn't use a while loop to continue the game ,it has no such need as the route will continue to be used until the end of the game with the appropriate updates being made to the routes  

When at least one legal move is possible, illegal moves = 0 this is because we try to count consecutive moves therefore if that's broken the counter will reset.
If no legal move can be made, then the number of illegal counts will be incremented by 1.
Ending the Game - Once the move counter hits zero, or if no player has any legal moves and it becomes an illegal move counter of 2, it signals the end of the game. It calls a function involving counting moves on the board and signals victory or a draw via a JSON response.

This is the end of the stage 2 algorithm so from now on the rest of explanation for the move route will be for only the stage 3 algorithm.

AI Move - If it's a valid move by the player and it's not a game over situation, then an AI move will be made. It uses the bot function for that.
It repeats exactly the same logic as in player moves:
The bot picks a coordinate.
The game piece is positioned and then the flipping algorithm is processed.
Session variables are updated.
It verifies legal moves.
It checks for game end.

The AI's move also returns a JSON response so that it can be reflected on the board.



Final Response (included in stage 2) - If all steps were successful, it will return a response with a JSON structure containing:

The new board
Colour of next player
Success message
If it was an invalid move, it will return a json response saying it failed.

For flowchart for move route with the bot:

[Move route without bot](Flowcharts/move%20route%20bot.pdf)

For flowchart for move without the bot:

[Move route with bot](Flowcharts/move%20route%20no%20bot.pdf)

## Save Route ("/save")
It is tasked with saving the state of the current game into a file.

It creates a dictionary with entries for: The board, the current colour, the move counter, the illegal count. It then writes these details into a file with the name savegame.json, which the player can then load. The script then reloads the board page. 

## Load Route ("/load") 

The load route tries to read savegame.json.  

If it finds it, it will reload the data inside it back into session variables. A message will be shown indicating that the file does not exist, and then the user will be redirected to the start screen so that a new game can be initialized.