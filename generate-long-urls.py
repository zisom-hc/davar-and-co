import pandas as pd
import argparse
import os
from datetime import datetime

# Set up argument parser
parser = argparse.ArgumentParser(description='Generate long URLs within the provided CSV file by using the contents of the same CSV file')
parser.add_argument('-csv_path', type=str, help='The path to the CSV file')
parser.add_argument('-base_url', type=str, default="https://www.davarandco.com/what-is-my-home-value", help='The base URL for the long URL that will be generated')
parser.add_argument('-address_column_name', type=str, default="Address", help='The base URL for the long URL that will be generated')
args = parser.parse_args()

# Read the CSV file
csv_data = pd.read_csv(args.csv_path, dtype=str, low_memory=False)

# Check if "Long URL" column exists, if not, create it and insert as the first column
if 'Long URL' not in csv_data.columns:
    csv_data.insert(0, 'Long URL', '')

# Create the parent folder if it does not exist
parent_folder = 'long-url-csv-files'
if not os.path.exists(parent_folder):
    os.makedirs(parent_folder)

# Create a timestamped subfolder
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_folder = os.path.join(parent_folder, timestamp)
os.makedirs(output_folder)

# Filter out rows where the "Address" column is empty
csv_data = csv_data.dropna()

# Loop through each row in the DataFrame
for index, row in csv_data.iterrows():
    
    # Construct the URL
    long_url = args.base_url
    utm_source = row[args.address_column_name].replace(' ', '+')
    utm_medium = "Mailer Valuation"
    url = f"{long_url}?utm_medium={utm_medium}&utm_source={utm_source}"
    
    # Overwrite the value in the "Long URL" column
    csv_data.at[index, 'Long URL'] = url

# Save the updated DataFrame back to the CSV file
#csv_data.to_csv(args.csv_path, index=False)

# Save the updated DataFrame back to a new CSV file in the timestamped subfolder
output_file_path = os.path.join(output_folder, os.path.basename(args.csv_path))
csv_data.to_csv(output_file_path, index=False)