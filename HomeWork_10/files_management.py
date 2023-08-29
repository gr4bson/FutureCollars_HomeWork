import json
from abc import abstractmethod, ABC


class FileManagementUI(ABC):

    @abstractmethod
    def load_data_from_file(self):
        pass

    def write_data_to_file(self):
        pass


class FileManager(FileManagementUI):
    def load_data_from_file(self, file):
        with open(file) as opened_file:
            stock_data = json.loads(opened_file.read())
            balance = stock_data.get("account_balance")
            kitchen_warehouse = stock_data.get("warehouse")
            return balance, kitchen_warehouse

    def write_data_to_file(self, file, balance, stock):
        with open(file, mode="w") as opened_file:
            data_to_save = {
                "account_balance": balance,
                "warehouse": stock
            }
            opened_file.write(json.dumps(data_to_save))

    def load_operation_log(self,file):
        with open(file) as opened_file:
            history_log = opened_file.read().split(",")
            return history_log

    def write_log_to_file(self, file, hist_log):
        with open(file, mode="w") as opened_file:
            delimiter = ","
            hist_log = delimiter.join(hist_log)
            opened_file.write(hist_log)
