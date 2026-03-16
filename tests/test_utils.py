import pytest

from apprise_api_headless.utils import parse_tag_expression


@pytest.mark.parametrize(
    "input_str,expected",
    [
        (None, None),
        ("", None),
        ("a", ["a"]),
        ("a b", [("a", "b")]),
        ("a, b", ["a", "b"]),
        ("a b, c", [("a", "b"), "c"]),
        ("a , b c", ["a", ("b", "c")]),
        ("   a   b  ,   c ", [("a", "b"), "c"]),
        (" , , ", []),
    ],
)
def test_parse_tag_expression(input_str, expected):
    assert parse_tag_expression(input_str) == expected
