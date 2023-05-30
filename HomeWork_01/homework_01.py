# Read data from xlsx file
import openpyxl

# Define variable to load the Excel workbook
dataframe = openpyxl.load_workbook("Oprocentowanie_pozyczki_oszczednosci_na_koncie.xlsx")

# Define variable to read active sheet
datasheet = dataframe.active  # since there's only one worksheet in the xlsx file it will always be the active one

debt_value = input('Podaj wysokosc zaciagnietego kredytu: ')
interest_rate = input('Podaj oprocentowanie kredytu: ')
due_monthly = input('Podaj wysokosc miesiecznej raty kredytu: ')
# Check if "," was used instead of "." as decimal point and change string into float
if ',' in debt_value:
    debt_value.replace(',', '.')
debt_value = float(debt_value)
if ',' in interest_rate:
    interest_rate.replace(',', '.')
percent_sign = False
if '%' in interest_rate:
    interest_rate.replace('%', '')
    percent_sign = True
interest_rate = float(interest_rate)
if percent_sign:
    interest_rate = interest_rate / 100
if ',' in due_monthly:
    due_monthly.replace(',', '.')

# Iterate the loop to read 1the cell values
for row in range(3, datasheet.max_row):
    month = datasheet.cell(row, 1).value
    inflation = datasheet.cell(row, 2).value
    print(f'{month} : {inflation}')
