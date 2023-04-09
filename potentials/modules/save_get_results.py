import json


def save_results(filename: str, results: list) -> None:
    with open(filename.split('.')[0] + '.txt', mode='w') as f:
        json.dump(results, f)


def get_results(filename: str) -> list:
    with open(filename.split('.')[0] + '.txt', mode='r') as f:
        results = json.load(f)
    return results
