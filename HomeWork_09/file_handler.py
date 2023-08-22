import sys
from pathlib import Path
from abc import abstractmethod
import csv
import json
import pickle


class FileHandler:
    def __init__(self, input_file, output_file, list_of_changes):
        self.input_file = input_file
        self.output_file = output_file
        self.list_of_changes: List[str] = list_of_changes
        self.changed_data = []
        self.input_file_exists: Bool = False
        self.chosen_handler = None

    def get_input(self):
        self.input_file = input_file
        self.output_file = output_file
        self.list_of_changes = list_of_changes

    def prepare_data_to_save(self):
        for list_item in self.list_of_changes:
            x = int(list_item.split(",")[0])
            y = int(list_item.split(",")[1])
            new_value = list_item.split(",")[2]
            self.changed_data[x][y] = new_value

    def check_file_extension(self):
        if self.input_file.endswith(".csv"):
            self.chosen_handler = CSVHandler(self.input_file, self.output_file, self.list_of_changes)
        if self.input_file.endswith(".txt"):
            self.chosen_handler = TXTHandler(self.input_file, self.output_file, self.list_of_changes)
        if self.input_file.endswith(".json"):
            self.chosen_handler = JSONHandler(self.input_file, self.output_file, self.list_of_changes)
        if self.input_file.endswith(".pkl"):
            self.chosen_handler = PICKLEHandler(self.input_file, self.output_file, self.list_of_changes)

    @abstractmethod
    def read_data_from_file(self):
        pass

    @abstractmethod
    def write_data_to_file(self):
        pass


class CSVHandler(FileHandler):

    def read_data_from_file(self):
        if Path(self.input_file).is_file():
            self.input_file_exists = True
            with open(self.input_file) as file:
                for line in csv.reader(file):
                    self.changed_data.append(line)
        else:
            self.input_file_exists = False

    def write_data_to_file(self):
        with open(self.output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.changed_data)


class TXTHandler(FileHandler):

    def read_data_from_file(self):
        if Path(self.input_file).is_file():
            self.input_file_exists = True
            with open(self.input_file) as file:
                for line in file.readlines():
                    list_element = line.strip().split(",")
                    self.changed_data.append(list_element)
        else:
            self.input_file_exists = False

    def write_data_to_file(self):
        with open(self.output_file, mode="w", newline="") as file:
            for list_element in self.changed_data:
                file.write(",".join(list_element) + "\n")

class JSONHandler(FileHandler):

    def read_data_from_file(self):
        if Path(self.input_file).is_file():
            self.input_file_exists = True
            with open(self.input_file) as file:
                self.changed_data = json.load(file)
        else:
            self.input_file_exists = False

    def write_data_to_file(self):
        with open(self.output_file, mode="w", newline="") as file:
            json.dump(self.changed_data, file)


class PICKLEHandler(FileHandler):

    def read_data_from_file(self):
        if Path(self.input_file).is_file():
            self.input_file_exists = True
            with open(self.input_file, mode="rb") as file:
                self.changed_data = pickle.load(file)
        else:
            self.input_file_exists = False

    def write_data_to_file(self):
        with open(self.output_file, mode="wb", newline="") as file:
            pickle.dump(self.changed_data, file)
