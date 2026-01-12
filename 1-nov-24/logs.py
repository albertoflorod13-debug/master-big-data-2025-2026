
import json
from collections import defaultdict, Counter
from argparse import ArgumentParser

def count_actions(logs: list[dict]) -> dict[str, int]:
    """
    Counts the number of each unique action appearing on the logs. 

        Args:
            logs (list[dict]): list of logs with actions from different users
        
        Returns:
            actions_counter (dict[str, int]): a dictionary whose key is the id of the action and the value is the number of times appearing on the logs

        Raises:
            TypeError: if input is not a list of dicts
            KeyError: if any log doesn't have the key `action`
    """

    if not isinstance(logs, list):
        raise TypeError("The input needs to be a list of dicts")

    actions_counter = defaultdict(lambda: 0)

    for i, log in enumerate(logs):
        if not isinstance(log, dict):
            raise TypeError("The input needs to be a list of dicts")
        if "action" not in log:
            raise KeyError(f"Log in index {i} is missing required key 'action'")
        actions_counter[log["action"]] +=1

    return dict(actions_counter)

def count_actions_fast(logs):
    return Counter(log["action"] for log in logs)

def get_unique_users(logs: list[dict]) -> set[str]:
    return {log.get("user") for log in logs} 


def filter_by_status(logs):
    return {
        log["user"]
        for log in logs
        if isinstance(log.get("status"), int) and 400 <= log.get("status") < 500
    }

def get_unique_ips(logs):
    return {log.get("ip") for log in logs}


def most_frequent_user(logs):
    counts = Counter(log["user"] for log in logs)
    return max(counts, key=counts.get)

def run_selected_exercise(json_path: str, exercise_number: int) -> None:

    with open(json_path) as f:
        json_data = json.load(f)
    
    match exercise_number:
        case 1:
            f = count_actions
        case 2:
            f = get_unique_users
        case 3:
            f = filter_by_status
        case 4:
            f = get_unique_ips
        case 5:
            f = most_frequent_user
        case _:
            raise ValueError("Invalid exercise number")

    return f(json_data)

if __name__ == "__main__":

    argparser = ArgumentParser()

    argparser.add_argument("--json_path", type=str)
    argparser.add_argument("--exercise_number", type=int)

    args = argparser.parse_args()

    print(run_selected_exercise(args.json_path, args.exercise_number))