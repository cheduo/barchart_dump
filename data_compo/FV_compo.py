import os
import pandas as pd

# Define the path to the downloads folder
downloads_path = r"C:\Users\cdsjt\Downloads"
data_path = r"C:\Users\cdsjt\data"
# Get a list of all CSV files in the downloads folder
csv_files = [
    file
    for file in os.listdir(downloads_path)
    if file.endswith(".csv")
    and file.startswith("zfm25_intraday-nearby-1min_historical")
]
combined_data = pd.DataFrame()
# Loop through each CSV file, read it, and append to the combined DataFrame
for file in csv_files:
    file_path = os.path.join(downloads_path, file)
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        # Append to the combined DataFrame
        combined_data = pd.concat([combined_data, df], ignore_index=True)
        print(f"Successfully added {file} to combined data.")
    except Exception as e:
        print(f"Error reading {file}: {str(e)}")
combined_data = combined_data.dropna(subset=["Time", "Open"])
combined_data["Time"] = pd.to_datetime(combined_data["Time"])
combined_data.drop_duplicates(subset=["Time"], inplace=True)
combined_data.sort_values(by="Time", inplace=True)
combined_data.reset_index(drop=True, inplace=True)
# combined_data.head()
combined_data.to_csv(r"C:\Users\cdsjt\data\FV1.csv", index=False)
