# SCP the data files to remote server
import subprocess
import platform
import os
import glob


def transfer_files_to_remote():
    local_dir = r"C:\Users\cdsjt\data"
    remote_destination = "chenduo@192.168.3.124:/home/chenduo/data/barchart/source_data"

    # Get all files in the directory
    files_to_transfer = glob.glob(os.path.join(local_dir, "*"))

    if not files_to_transfer:
        print(f"No files found in {local_dir}")
        return False

    # Check if running on Windows
    if platform.system() == "Windows":
        # On Windows, we need to use the full path to scp or use it if it's in PATH
        try:
            for local_file in files_to_transfer:
                if os.path.isfile(local_file):  # Only transfer files, not directories
                    print(f"Transferring {local_file} to {remote_destination}...")
                    result = subprocess.run(
                        ["scp", local_file, remote_destination],
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    print(
                        f"File {os.path.basename(local_file)} transferred successfully!"
                    )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error transferring file: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except FileNotFoundError:
            print(
                "scp command not found. Make sure OpenSSH is installed and in your PATH."
            )
            print("You can manually transfer the files using:")
            print(f'scp "{local_dir}/*" {remote_destination}')
            return False
    else:
        # For non-Windows systems
        try:
            for local_file in files_to_transfer:
                if os.path.isfile(local_file):  # Only transfer files, not directories
                    print(f"Transferring {local_file} to {remote_destination}...")
                    result = subprocess.run(
                        ["scp", local_file, remote_destination],
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    print(
                        f"File {os.path.basename(local_file)} transferred successfully!"
                    )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error transferring file: {e}")
            print(f"Error output: {e.stderr}")
            return False


# Execute the transfer
transfer_files_to_remote()
