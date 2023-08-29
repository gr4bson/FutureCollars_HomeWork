from files_management import FileManager


class Manager(FileManager):
    def __init__(self, operation_log_file, stock_file):
        self.operation_log_file = operation_log_file
        self.stock_file = stock_file
        self.operation_log = self.load_operation_log(operation_log_file)
        self.account_balance, self.kitchen_warehouse = self.load_data_from_file(stock_file)
        self.prompts = {}

    def assign(self, name):
        def wrapper(operation):
            self.prompts[name] = operation
        return wrapper

    def execute(self, name):
        if name not in self.prompts:
            print("Ta operacja jest niedostępna. Spróbuj jeszcze raz.")
        else:
            self.prompts[name](self)