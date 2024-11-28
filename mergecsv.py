import pandas as pd

def generate_and_merge_csv():
    # Load the CSV file
    csv_file_path = 'final_scores.csv'
    csv_df = pd.read_csv(csv_file_path)

    # Load the Excel file
    excel_file_path = '../main_list.xlsx'
    excel_df = pd.read_excel(excel_file_path)

    # Merge the dataframes based on the emailID field
    merged_df = pd.merge(excel_df, csv_df, on='EmailID', how='left')

    # Save the merged dataframe back to an Excel file
    output_excel_file_path = '../merged_output.xlsx'
    merged_df.to_excel(output_excel_file_path, index=False)

    print(f'Merged Excel file saved as {output_excel_file_path}')
 