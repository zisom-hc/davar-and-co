import pandas as pd
import qrcode
from PIL import Image, ImageOps, ImageDraw
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

def add_rounded_corners(image, radius):
    # Create a mask for rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + image.size, radius, fill=255)
    image.putalpha(mask)
    return image

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
    img = qr.make_image(fill_color='#254bad', back_color='white').convert('RGBA')
    
    # Add white border to the QR code
    white_border_size = 20  # Adjust the white border size as needed
    img_with_white_border = ImageOps.expand(img, border=white_border_size, fill='white')
    
    # Add rounded corners to the QR code with white border
    corner_radius = 50  # Adjust the corner radius as needed
    img_with_white_border = add_rounded_corners(img_with_white_border, corner_radius)
    
    # Create a black background with rounded corners
    black_border_size = 30  # Adjust the black border size as needed
    black_bg_size = (img_with_white_border.size[0] + 2 * black_border_size, img_with_white_border.size[1] + 2 * black_border_size)
    black_bg = Image.new('RGBA', black_bg_size, 'black')
    black_bg = add_rounded_corners(black_bg, corner_radius + black_border_size)
    
    # Calculate the position to paste the QR code with white border onto the black background
    pos = (black_border_size, black_border_size)
    black_bg.paste(img_with_white_border, pos, img_with_white_border)
    
    # Load the logo image
    logo = Image.open('davar-and-co-logo.png')
    
    # Ensure the logo has an alpha channel
    logo = logo.convert("RGBA")
    
    # Calculate the size of the logo
    logo_size = (black_bg.size[0] // 3, black_bg.size[1] // 3)
    logo = logo.resize(logo_size, Image.LANCZOS)
    
    # Calculate the position to paste the logo
    pos = ((black_bg.size[0] - logo.size[0]) // 2, (black_bg.size[1] - logo.size[1]) // 2)
    
    # Create a white background for the logo area
    logo_bg = Image.new('RGBA', logo_size, (255, 255, 255, 255))
    black_bg.paste(logo_bg, pos, logo_bg)
    
    # Paste the logo image onto the QR code
    black_bg.paste(logo, pos, logo)
    
    # Save the image in the timestamped subfolder
    black_bg.save(os.path.join(output_folder, f'qr_code_{utm_source}.png'.replace('+', '_')))
