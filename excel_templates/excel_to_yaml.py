import pandas as pd
import yaml
import re
import process_junos_yaml
import argparse

def clean_value(value):
    """Helper function to clean individual cell values."""
    if pd.isna(value):  # Ignore NaN or empty cells
        return None
    elif isinstance(value, float) and value.is_integer():  # Convert floats like 12.0 to 12
        return int(value)
    elif isinstance(value, str):  # Handle strings
        # Remove '*' from string values and convert "Y"/"y" to True and "N"/"n" to False
        cleaned_value = value.replace('*', '')
        if cleaned_value.lower() == 'y':
            return True
        elif cleaned_value.lower() == 'n':
            return False
        return cleaned_value.strip()
    return value
  
def clean_row(row):
    """Remove None values and empty lists from a dictionary."""
    cleaned_row = {k: v for k, v in row.items() if v is not None}
    return {k: v for k, v in cleaned_row.items() if not (isinstance(v, list) and not v)}

def get_last_word(sheet_name):
    """Extract the last word from the sheet name."""
    return sheet_name.split()[-1]

def read_excel_to_dict(excel_path):
    """Read an Excel workbook and return its contents as a dictionary, processing only sheets where the name starts with a single digit."""
    workbook = pd.ExcelFile(excel_path)
    data = {}

    for sheet_name in workbook.sheet_names:
        # Process only sheets with names that start with a single digit
        if re.match(r'^\d', sheet_name):
            simplified_name = get_last_word(sheet_name)  # Use last word as the key
            df = workbook.parse(sheet_name)  # Load sheet into a DataFrame
            cleaned_data = [
                clean_row({k: clean_value(v) for k, v in row.items()})
                for row in df.to_dict(orient='records')
            ]
            # Exclude completely empty rows
            data[simplified_name] = [row for row in cleaned_data if row]

    return data

def write_yaml(data, yaml_path):
    """Write data to a YAML file."""
    with open(yaml_path, 'w') as yaml_file:
        yaml.dump(data, yaml_file, sort_keys=False, allow_unicode=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=">>> Juniper SRX Spreadsheet Template conversion tool")
    parser.add_argument(
        "--excel",
        required=False,
        type=str,
        default='.\\sample_workbook.xlsx',
        help="Specify the Junos configuration template file"
    )
    parser.add_argument(
        "--yaml",
        required=False,
        type=str,
        default='..\\group_vars\\base_srx.yml',
        help="Specify the YAML variable file to output to"
    )
    args = parser.parse_args()

    # Calls the function to read Excel file and convert to a clean YAML Dataframe
    data = read_excel_to_dict(args.excel)

    # Call the script to perform normalization of the data to prepare  
    # for Juniper based configuration. 
    data = process_junos_yaml.main(data)

    # Write the final data to YAML
    write_yaml(data, args.yaml)
