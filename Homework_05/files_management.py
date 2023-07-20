import json


def load_data_from_file(file):
    with open(file) as opened_file:
        stock_data = json.loads(opened_file.read())
        return stock_data


def write_data_to_file(file, balance, stock):
    with open(file, mode="w") as opened_file:
        data_to_save = {
            "account_balance": balance,
            "magazyn": stock
        }
        opened_file.write(json.dumps(data_to_save))


def load_operation_log(file):
    with open(file) as opened_file:
        history_log = opened_file.read().split(",")
        return history_log


def write_log_to_file(file, hist_log):
    with open(file, mode="w") as opened_file:
        delimiter = ","
        hist_log = delimiter.join(hist_log)
        opened_file.write(hist_log)
