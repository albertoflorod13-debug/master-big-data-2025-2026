import pytest

from solve_password import parse_code, get_password, iter_lines


@pytest.mark.parametrize(
    "code, expected",
    [
        ("R3", 3),
        ("L3", -3),
        ("R0", 0),
        ("L0", 0),
        ("R0007", 7),   # accepted by current implementation
        ("L0007", -7),  # accepted by current implementation
    ],
)
def test_parse_code_valid(code: str, expected: int) -> None:
    assert parse_code(code) == expected


@pytest.mark.parametrize(
    "code",
    [
        "X3",     # invalid direction
        "R",      # missing magnitude
        "L",      # missing magnitude
        "",       # empty
        "R-3",    # non-digit magnitude
        "R3.2",   # non-digit magnitude
        "R 3",    # whitespace inside
        " R3",    # leading whitespace (parse_code does not strip)
        "R3 ",    # trailing whitespace
    ],
)
def test_parse_code_invalid(code: str) -> None:
    with pytest.raises(ValueError):
        parse_code(code)


# -----------------------
# get_password unit tests
# -----------------------

def test_get_password_empty_sequence_returns_zero() -> None:
    assert get_password([], initial_position=5, dial_length=10) == 0


def test_get_password_hits_zero_once_simple() -> None:
    assert get_password(["L1"], initial_position=1, dial_length=10) == 1


def test_get_password_wraparound_left_does_not_hit_zero() -> None:
    # 0 + (-1) % 10 = 9
    assert get_password(["L1"], initial_position=0, dial_length=10) == 0


def test_get_password_wraparound_right_hits_zero() -> None:
    # 9 + 1 % 10 = 0
    assert get_password(["R1"], initial_position=9, dial_length=10) == 1


def test_get_password_multiple_zero_hits() -> None:
    # initial 1:
    # L1 -> 0 (hit #1)
    # R1 -> 1
    # L1 -> 0 (hit #2)
    assert get_password(["L1", "R1", "L1"], initial_position=1, dial_length=10) == 2


def test_get_password_large_step_equivalent_to_modulo() -> None:
    # 21 % 10 = 1, from 0 ends at 1, never hits 0 during the move-counting (only after move)
    assert get_password(["R21"], initial_position=0, dial_length=10) == 0


def test_get_password_initial_position_normalized_when_out_of_range_positive() -> None:
    # initial 11 -> 1, then L1 -> 0
    assert get_password(["L1"], initial_position=11, dial_length=10) == 1


def test_get_password_initial_position_normalized_when_out_of_range_negative() -> None:
    # initial -1 -> 9, then R0 keeps 9
    assert get_password(["R0"], initial_position=-1, dial_length=10) == 0


def test_get_password_invalid_dial_length_raises() -> None:
    with pytest.raises(ValueError):
        get_password(["R1"], initial_position=0, dial_length=0)
    with pytest.raises(ValueError):
        get_password(["R1"], initial_position=0, dial_length=-10)


def test_get_password_invalid_code_in_sequence_raises() -> None:
    with pytest.raises(ValueError):
        get_password(["R1", "BAD", "R1"], initial_position=0, dial_length=10)


def test_get_password_accepts_iterable_generator() -> None:
    def gen():
        yield "L1"
        yield "R1"
        yield "L1"
    assert get_password(gen(), initial_position=1, dial_length=10) == 2


# -----------------------
# iter_lines integration tests
# -----------------------

def test_iter_lines_strips_newlines(tmp_path) -> None:
    p = tmp_path / "input.txt"
    p.write_text("R1\nL2\n", encoding="utf-8")
    assert list(iter_lines(str(p))) == ["R1", "L2"]


def test_iter_lines_blank_line_produces_empty_string_and_causes_failure_downstream(tmp_path) -> None:
    p = tmp_path / "input.txt"
    p.write_text("R1\n\nL2\n", encoding="utf-8")

    seq = iter_lines(str(p))
    # current behavior: yields ["R1", "", "L2"]
    assert next(seq) == "R1"
    assert next(seq) == ""

    # and get_password will raise once it hits the blank line
    with pytest.raises(ValueError):
        get_password(iter_lines(str(p)), initial_position=0, dial_length=10)
