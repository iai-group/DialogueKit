"""Test UtteranceFeedback class."""
from dialoguekit.core.feedback import BinaryFeedback, UtteranceFeedback


def test_initialization():
    """Tests utterance feedback initialization."""
    f1 = UtteranceFeedback("utterance_1", BinaryFeedback.POSITIVE)
    assert isinstance(f1, UtteranceFeedback)
    assert f1.feedback == BinaryFeedback.POSITIVE


def test_comparison():
    """Tests utterance feedback comparison."""
    f1 = UtteranceFeedback("utterance_1", BinaryFeedback.POSITIVE)
    f2 = f1
    assert f1 == f2

    f3 = UtteranceFeedback("utterance_1", BinaryFeedback.POSITIVE)
    assert f1 == f3

    f4 = UtteranceFeedback("utterance_1", BinaryFeedback.NEGATIVE)
    assert f1 != f4
