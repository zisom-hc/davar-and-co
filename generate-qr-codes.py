import pandas as pd
import qrcode
from PIL import Image
import argparse
import os
from datetime import datetime

# Set up argument parser
parser = argparse.ArgumentParser(description='Generate QR codes from a CSV file.')
parser.add_argument('-csv_path', type=str, help='The path to the CSV file')
args = parser.parse_args()

# Read the CSV file
df = pd.read_csv(args.csv_path)

# Create the parent folder if it does not exist
parent_folder = 'qr-code-images'
if not os.path.exists(parent_folder):
    os.makedirs(parent_folder)

# Create a timestamped subfolder
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_folder = os.path.join(parent_folder, timestamp)
os.makedirs(output_folder)

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    # Construct the URL
    long_url = row['Long URL']
    utm_source = row['UTM Source'].replace(' ', '+')
    utm_medium = row['UTM Medium'].replace(' ', '+')
    url = f"{long_url}?utm_medium={utm_medium}&utm_source={utm_source}"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Use high error correction to allow for image in the center
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code instance
    img = qr.make_image(fill_color='blue', back_color='white').convert('RGB')
    
    # Load the logo image
    logo = Image.open('davar-and-co-logo.png')
    
    # Ensure the logo has an alpha channel
    logo = logo.convert("RGBA")
    
    # Calculate the size of the logo
    logo_size = (img.size[0] // 3, img.size[1] // 3)
    logo = logo.resize(logo_size, Image.LANCZOS)
    
    # Calculate the position to paste the logo
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    
    # Create a white background for the logo area
    logo_bg = Image.new('RGB', logo_size, (255, 255, 255))
    img.paste(logo_bg, pos)
    
    # Paste the logo image onto the QR code
    img.paste(logo, pos, logo)
    
    # Save the image in the timestamped subfolder
    img.save(os.path.join(output_folder, f'qr_code_{utm_source}.png'))