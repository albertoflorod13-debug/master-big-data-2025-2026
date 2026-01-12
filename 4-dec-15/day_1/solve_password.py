from typing import Iterable, Iterator

def parse_code(code: str) -> int:

    if len(code) < 2 or not code[1:].isdigit():
        raise ValueError(f"Invalid input code: {code}")

    direction_char = code[0]
    value = int(code[1:])
    if direction_char == "L":
        return -value
    elif direction_char == "R":
        return value
    else:
        raise ValueError(f"Invalid input code: {code}")

def get_password(code_sequence: Iterable[str], initial_position: int = 50, dial_length: int = 100) -> int:

    if dial_length <= 0:
        raise ValueError("dial_length must be a positive integer")

    position = initial_position % dial_length
    password_counter = 0
    for delta in map(parse_code, code_sequence):
        new_position = position + delta
        if delta >= 0:
            wraps = new_position // dial_length
        else:
            wraps = (dial_length - new_position) // dial_length
            if position == 0:
                wraps -= 1
            
        # Second half solution
        password_counter += wraps

        position =  new_position % dial_length
        print(f"{delta=}, {position=}, {wraps},")

        # First half solution
        # if position == 0:
        #    password_counter += 1

    return password_counter

def iter_lines(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            yield line.strip()

if __name__ == '__main__':

    #sequence = iter_lines('input.txt')

    # input.txt is different for each user, but this is the common one
    sequence = ['L68', 'L30', 'R48', 'L5', 'R60', 'L55', 'L1', 'L99', 'R14', 'L82']
    print(get_password(sequence))
