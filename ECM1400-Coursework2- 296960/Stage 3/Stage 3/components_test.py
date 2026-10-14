import pytest
import components 

def test_actual_size():
    board = components.initialise_board(8)
    assert board[3][3] == "Light"
    assert board[3][4] == "Dark "
    assert board[4][3] == "Dark "
    assert board[4][4] == "Light"

def test_default_size():
    board = components.initialise_board()
    assert board[3][3] == "Light"
    assert board[3][4] == "Dark "
    assert board[4][3] == "Dark "
    assert board[4][4] == "Light"

def test_custom_size():
    board = components.initialise_board(10)
    assert board[4][4] == "Light"
    assert board[4][5] == "Dark "
    assert board[5][4] == "Dark "
    assert board[5][5] == "Light"  

def test_legal_input():
    coordinates = (2,3)
    results = components.legal_move("Dark ", coordinates, components.initialise_board())
    assert results == True 

def test_illegal_input():
    coordinates = (7,7)
    results = components.legal_move("Dark ", coordinates, components.initialise_board())
    assert results == False

def test_taken_place():
    coordinates = (4,4)
    results = components.legal_move("Dark ", coordinates, components.initialise_board())
    assert results == False   

