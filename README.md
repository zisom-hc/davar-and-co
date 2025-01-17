# QR Code Generator

This script generates QR codes from a CSV file and places a logo in the center of each QR code. The QR codes are saved in a timestamped subfolder within the `qr-code-images` folder that it will create within the working directory, if it does not exist at time of execution.

## Prerequisites

1. **Python Installation**:
    - Ensure you have Python installed on your machine. You can download and install Python from [python.org](https://www.python.org/downloads/).

    ### For macOS:
    - Open Terminal and install Homebrew if you haven't already:
      ```sh
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
    - Install Python using Homebrew:
      ```sh
      brew install python
      ```

2. **Install Required Modules**:
    - Install the required Python modules using `pip`. Open Terminal and run:
      ```sh
      pip install pandas qrcode[pil] pillow
      ```

## Usage

1. **Prepare the CSV File**:
    - Ensure your CSV file contains the necessary columns: `Long URL`, `UTM Source`, and `UTM Medium`.

2. **Run the Script**:
    - Place your logo image (`davar-and-co-logo.png`) in the same directory as the script.
    - Open Terminal and navigate to the directory containing the script.
    - Run the script with the path to your CSV file as an argument:
      ```sh
      python generate-qr-codes.py -csv_path "path/to/your/csvfile.csv"
      ```

3. **Output**:
    - The generated QR codes will be saved in a timestamped subfolder within a [qr-code-images](http://_vscodecontentref_/0) folder that will be created within the working directory, if it does not exist.

## Example

```sh
python generate-qr-codes.py -csv_path "Bitly_Bulk_Shorten_Cottonwood.csv"
