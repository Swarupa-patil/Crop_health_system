from app.models.fact import Fact
from app.models.rule import Rule
from app.engine.backward_chaining import backward_chain


def test_backward_chaining():
    facts = [Fact("brown_spots", True)]

    rule = Rule(
        "R001",
        [Fact("brown_spots", True)],
        Fact("leaf_spot_condition", True)
    )

    goal = Fact("leaf_spot_condition", True)

    result, trace = backward_chain(goal, facts, [rule])

    assert result is True
    assert trace == ["R001"]