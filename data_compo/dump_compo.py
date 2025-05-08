import os
import pandas as pd
from pathlib import Path

# Define paths
downloads_path = Path(r"C:\Users\cdsjt\Downloads")
data_path = Path(r"C:\Users\cdsjt\data")
download_pattern = "ngm25_intraday"
output_name = "NG1"

# Check if output file already exists
output_file = data_path / f"{output_name}.csv"
hist_df = (
    pd.read_csv(output_file, parse_dates=["Time"])
    if output_file.exists()
    else pd.DataFrame()
)

# Get all matching CSV files in the downloads folder
csv_files = [
    file
    for file in os.listdir(downloads_path)
    if file.endswith(".csv") and download_pattern in file
]

# Combine data from all files
combined_data = pd.DataFrame()
for file in csv_files:
    try:
        df = pd.read_csv(downloads_path / file)
        combined_data = pd.concat([combined_data, df], ignore_index=True)
        print(f"Successfully added {file} to combined data.")
    except Exception as e:
        print(f"Error reading {file}: {str(e)}")


# Clean and process the data
if not combined_data.empty:
    # Process new data
    combined_data = combined_data.dropna(subset=["Time", "Open"])
    combined_data = (
        combined_data.assign(Time=pd.to_datetime(combined_data["Time"]))
        .drop_duplicates(subset=["Time"])
        .sort_values(by="Time")
    )

    # Merge with historical data
    final_data = (
        pd.concat([hist_df, combined_data], ignore_index=True)
        .drop_duplicates(subset=["Time"])
        .sort_values(by="Time")
        .reset_index(drop=True)
    )

    # Save the processed data
    final_data.to_csv(output_file, index=False)
    print(f"Data successfully saved to {output_file}")
    print(final_data.head())
    # Remove all processed CSV files from downloads folder
    for file in csv_files:
        try:
            file_path = downloads_path / file
            os.remove(file_path)
            print(f"Removed file: {file}")
        except Exception as e:
            print(f"Error removing {file}: {str(e)}")
else:
    print("No data was combined. Check if any matching files exist.")
