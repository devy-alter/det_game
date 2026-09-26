from app.game.confidence import apply_confidence, apply_progress

def test_confidence_clamps():
    assert apply_confidence(3,-20)==0
    assert apply_confidence(98,20)==100

def test_progress_clamps():
    assert apply_progress(98,20)==100
