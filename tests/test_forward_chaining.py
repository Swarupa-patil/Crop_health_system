from app.models.fact import Fact
from app.models.rule import Rule
from app.engine.forward_chaining import forward_chain


def test_forward_chaining():
    facts = [
        Fact("brown_spots", True)
    ]

    rule = Rule(
        "R001",
        [Fact("brown_spots", True)],
        Fact("leaf_spot_condition", True)
    )

    new_facts, trace = forward_chain(facts, [rule])

    assert any(
        f.name == "leaf_spot_condition" and f.value is True
        for f in new_facts
    )
    assert trace == ["R001"]