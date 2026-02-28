from plset.cli import union, intersect, diff, xor


def test_union():
    a = ["a", "b", "c"]
    b = ["c", "d"]
    assert union(a, b) == ["a", "b", "c", "d"]


def test_intersect():
    a = ["a", "b", "c"]
    b = ["b", "c", "d"]
    assert intersect(a, b) == ["b", "c"]


def test_diff():
    a = ["a", "b", "c"]
    b = ["b"]
    assert diff(a, b) == ["a", "c"]


def test_xor():
    a = ["a", "b", "c"]
    b = ["b", "d"]
    assert xor(a, b) == ["a", "c", "d"]