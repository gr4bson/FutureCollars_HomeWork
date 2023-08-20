import csv
from pathlib import Path


class CSVHandler:
    def __init__(self, input_file, output_file, list_of_changes):
        self.input_file = input_file
        self.data_in_file = []
        self.output_file = output_file
        self.list_of_changes: List[str] = list_of_changes
        self.changed_data = []
        self.input_file_exists: Bool

    def read_csv_file(self):
        if Path(self.input_file).is_file():
            self.input_file_exists = True
            with open(self.input_file) as file:
                for line in csv.reader(file):
                    self.data_in_file.append(line)
        else:
            self.input_file_exists = False

    def prepare_data_to_save(self):
        self.changed_data = self.data_in_file
        for list_item in self.list_of_changes:
            x = int(list_item.split(",")[0])
            y = int(list_item.split(",")[1])
            self.changed_data[x][y] = list_item.split(",")[2]


    def write_data_to_csv_file(self):
        with open(self.output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.changed_data)

    def change_data(self):
        self.read_csv_file()
        if self.input_file_exists:
            print("Data before modification:")
            for line in self.data_in_file:
                print(line)
            self.prepare_data_to_save()
            self.write_data_to_csv_file()
            print("Data after modification:")
            for line in self.changed_data:
                print(line)
        else:
            print(f"Input file {self.input_file} does not exist")

#change = CSVHandler(sys.argv[1], sys.argv[2], sys.argv[3:])#("in.csv", "out.csv", [[0,0,gitara],[3,1,kubek],[1,2,17],[3,3,0]])

#change.read_csv_file()
#print(change.data_in_file)
#change.change_data()

#CSVHandler().change_data()