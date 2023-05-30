#Read data from xlsx file
import openpyxl

# Define variable to load the Excel workbook
dataframe = openpyxl.load_workbook("Oprocentowanie_pozyczki_oszczednosci_na_koncie.xlsx")

# Define variable to read active sheet
datasheet = dataframe.active

# Iterate the loop to read the cell values
for row in range(3, datasheet.max_row):
    month=datasheet.cell(row, 1).value
    inflation=datasheet.cell(row, 2).value
    print(f'{month} : {inflation}')
