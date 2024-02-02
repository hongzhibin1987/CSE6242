import csv

def username():
    return 'zhong61/zhong87'

def data_wrangling():
    # Open the CSV file
    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Read in the header
        header = next(reader)
        
        # Initialize an empty list to store the first 100 rows
        table = []
        
        # Iterate over the rows of the file
        for i, row in enumerate(reader):
            # Stop after reading the first 100 rows
            if i == 100:
                break
            # Append each row to the table list
            table.append(row)
        
        # Convert the last column to float for sorting, then convert back to string
        for row in table:
            row[-1] = float(row[-1])
        
        # Sort the table by the 'Avg' column in descending order
        table.sort(key=lambda x: x[-1], reverse=True)
        
        # Convert the last column back to string
        for row in table:
            row[-1] = str(row[-1])

    # Return the header and the sorted table
    return header, table


import csv


def username():
    return 'zhong61/zhong87'  # Replace with your actual GTUsername


import csv


def username():
    return 'your_GTUsername'  # Replace with your actual GTUsername


def data_wrangling():
    with open('data/movies.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Read in the header
        table = []

        # Read in the first 100 data rows
        for row in reader:
            if len(table) < 100:
                table.append(row)
            else:
                break  # Stop reading after the first 100 rows

        # Convert the last column to float for sorting, and then back to string
        for row in table:
            row[-1] = float(row[-1])

        # Sort the table by the 'Avg' column in descending order
        table.sort(key=lambda row: row[-1], reverse=True)

        # Convert the last column back to string
        for row in table:
            row[-1] = str(row[-1])

    return header, table

header, sorted_table = data_wrangling()
print(header)
for row in sorted_table[:10]:  # Print first 10 rows to verify sorting
    print(row)
