from project import game_status

def test_game_status():
    assert game_status(True) == "successful"
    assert game_status(False) == "error"



