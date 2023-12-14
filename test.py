from Main import is_win_turn
from Main import do_field
from Main import is_game_finished

field = do_field(5, 400 - 14.5 * 40, 300 - 40 / 2, 40)


def test_is_win_turn():
    field[0][0].color = 'red'
    field[0][1].color = 'red'
    field[0][2].color = 'red'
    field[0][3].color = 'red'
    assert is_win_turn(field, 'red', 'blue') == (0, 4)

    field[0][0].color = 'blue'
    field[2][0].color = 'blue'
    field[3][0].color = 'blue'
    field[4][0].color = 'blue'
    assert is_win_turn(field, 'red', 'blue') == (1, 0)

    field[0][0].color = 'red'
    field[1][1].color = 'red'
    field[3][2].color = 'red'
    field[2][3].color = 'red'
    assert is_win_turn(field, 'red', 'blue') == (-1, -1)


def test_is_game_finished():
    field[0][0].color = 'red'
    field[0][1].color = 'red'
    field[0][2].color = 'red'
    field[0][3].color = 'red'
    field[0][4].color = 'red'
    assert is_game_finished(field, 'red') == True
    assert is_game_finished(field, 'blue') == True

    field[0][0].color = 'blue'
    field[1][0].color = 'blue'
    field[2][0].color = 'blue'
    field[3][0].color = 'blue'
    field[4][0].color = 'blue'
    assert is_game_finished(field, 'blue') == True

    field[1][0].color = 'red'
    field[2][1].color = 'red'
    field[0][2].color = 'red'
    field[3][3].color = 'red'
    field[5][0].color = 'red'
    assert is_game_finished(field, 'red') == False
