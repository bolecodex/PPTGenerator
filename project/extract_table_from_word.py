from docx import Document
import pandas as pd

# Load the docx file
docx_path = 'Q3_2023_e.docx'
doc = Document(docx_path)

# Extracting tables
extracted_tables = []

for i, table in enumerate(doc.tables):
    # Extracting each row
    rows = []
    for row in table.rows:
        cells = [cell.text for cell in row.cells]
        rows.append(cells)
    
    # Creating a DataFrame for each table
    df = pd.DataFrame(rows)
    extracted_tables.append(df)

# Display the number of tables extracted and the first table as an example
num_tables_extracted = len(extracted_tables)
first_table_example = extracted_tables[0] if num_tables_extracted > 0 else None

print(num_tables_extracted)
print(first_table_example)

# Saving the extracted tables to an Excel file
excel_path = 'Q3_2023_e_extracted_tables.xlsx'

# Creating a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    for i, table in enumerate(extracted_tables):
        # Writing each dataframe to a different worksheet
        table.to_excel(writer, sheet_name=f'Table_{i+1}', index=False)
