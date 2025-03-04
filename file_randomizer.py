"""
File Randomizer: A Python script to randomize filenames in a directory with numbered prefixes.

This script allows users to:
- Randomly prefix filenames with numbers (e.g., "_1filename.txt").
- Revert files to their original names using a CSV tracker.
- Remove prefixes and recreate the CSV if it's missing.
- Append new files in the directory to the CSV on each run.
- Remove deleted files from the CSV on each run.
- Built to be portable and convertible to an executable with PyInstaller.
"""
import os
import sys
import random
import pandas as pd
import shutil
import re


# Disable pandas chained assignment warnings for cleaner output
pd.options.mode.chained_assignment = None


# --- Global Variables ---
COUNTER = 0  # Unused; reserved for potential future enhancements
NUMBER_LIST = []  # List of randomized numbers for prefixes
SCRIPT_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]  # Base name of script/executable
TYPE = os.path.splitext(os.path.basename(sys.argv[0]))[1]  # File extension
SCRIPT_FULL_NAME = os.path.basename(sys.argv[0])  # Full name (e.g., "File Randomizer.exe")
CURRENT_DIR = os.getcwd()  # Directory where script runs
DIR_PATH = CURRENT_DIR  # Path to process files


def resource_path(relative_path):
    """Get absolute path to resource, supporting dev and PyInstaller environments.

    Args:
        relative_path (str): Path to the resource relative to the script.

    Returns:
        str: Absolute path to the resource.
    """
    if hasattr(sys, '_MEIPASS'):  # PyInstaller runtime environment
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def store_original_file_names():
    """Initialize or update the CSV with original filenames.

    - Creates 'DO_NOT_DELETE_all_file_names.csv' if missing, copying from embedded version if available.
    - Appends new files not already in CSV.
    - Removes entries for files deleted from directory.
    """
    files = [f for f in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, f))]
    exclude_files = {SCRIPT_FULL_NAME, "DO_NOT_DELETE_all_file_names.csv","shuffle.ico"}  # Files to exclude from processing
    files = [f for f in files if f not in exclude_files]
    csv_path = os.path.join(DIR_PATH, "DO_NOT_DELETE_all_file_names.csv")

    # Copy embedded CSV if local version doesn't exist
    if not os.path.exists(csv_path):
        bundled_csv = resource_path("DO_NOT_DELETE_all_file_names.csv")
        if os.path.exists(bundled_csv):
            shutil.copy(bundled_csv, csv_path)

    # Create new CSV or update existing one
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=["original", "new", "unchanged"])
        df["original"] = files
        df.to_csv(csv_path, index=False)
    else:
        print('Welcome back, if you are finding utility from this script consider buying me a coffee:'
              '\nhttps://ko-fi.com/massauto')
        df = pd.read_csv(csv_path)
        existing_originals = set(df["original"].tolist())  # Files already in 'original' column
        existing_new = set(df["new"].tolist())  # Files already in 'new' column
        # New files not yet tracked in CSV
        new_items = [f for f in files if f not in existing_originals and f not in existing_new]

        # Append new files to CSV
        if new_items:
            df_new = pd.DataFrame({"original": new_items})
            df = pd.concat([df, df_new]).drop_duplicates(subset="original").reset_index(drop=True)
            df.to_csv(csv_path, index=False)

        # Remove entries for deleted files with original names
        if df.columns[2] == 'unchanged':
            for each_file in existing_originals:
                if each_file not in files:
                    df = df[~df['original'].isin([each_file])]
                    df.to_csv(csv_path, index=False)

        # Remove entries for deleted files with prefixed names
        if df.columns[2] == 'prefixed':
            for ef in existing_new:
                if ef not in files:
                    df = df[~df['new'].isin([ef])]
                    df.to_csv(csv_path, index=False)


def remove_prefixes():
    """Remove prefixes from filenames and recreate CSV if needed.

    Targets files with '_[number]' prefixes (e.g., '_1file.txt' -> 'file.txt').
    """
    files = [f for f in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, f))]
    exclude_files = {SCRIPT_FULL_NAME, "DO_NOT_DELETE_all_file_names.csv"}  # Files to exclude
    files = [f for f in files if f not in exclude_files]
    csv_path = os.path.join(DIR_PATH, "DO_NOT_DELETE_all_file_names.csv")
    original_names = []
    current_names = []

    # Process each file to remove prefixes
    for filename in files:
        if filename.startswith("_") and filename[1:2].isdigit():
            # Strip '_[number]' prefix using regex
            cleaned_name = re.sub(r"^_\d+", "", filename)
            original_names.append(cleaned_name)
            current_names.append(filename)
            # Rename file to its cleaned name
            source = os.path.join(DIR_PATH, filename)
            dest = os.path.join(DIR_PATH, cleaned_name)
            if os.path.exists(source) and not os.path.exists(dest):
                os.rename(source, dest)
        else:
            original_names.append(filename)
            current_names.append(filename)

    # Recreate CSV with cleaned names
    df = pd.DataFrame(columns=["original", "new", "unchanged"])
    df['original'] = original_names
    df['new'] = current_names
    df.to_csv(csv_path, index=False)


def initialize_number_list(file_count):
    """Generate and shuffle a list of numbers for random prefixes.

    Args:
        file_count (int): Number of files needing prefixes.
    """
    global NUMBER_LIST
    NUMBER_LIST = [str(i) for i in range(1, file_count + 1)]
    random.shuffle(NUMBER_LIST)


def add_random_prefixes():
    """Apply random numbered prefixes to filenames and update CSV."""
    csv_path = os.path.join(DIR_PATH, "DO_NOT_DELETE_all_file_names.csv")
    df = pd.read_csv(csv_path)
    original_names = df["original"].tolist()
    new_names = []

    # Create prefixed filenames
    for filename in original_names:
        if NUMBER_LIST:
            number = NUMBER_LIST.pop(0)
            prefixed = "_" + number + filename
            new_names.append(prefixed)
        else:
            new_names.append(filename)

    # Update CSV with new names
    df["new"] = pd.Series(new_names).reindex(df.index)
    df.to_csv(csv_path, index=False)

    # Rename files in directory
    for _, row in df.iterrows():
        original = row["original"]
        new = row["new"]
        source = os.path.join(DIR_PATH, original)
        dest = os.path.join(DIR_PATH, new)
        if os.path.exists(source) and not os.path.exists(dest):
            os.rename(source, dest)


def path_reset():
    """Revert filenames to originals using CSV data."""
    csv_path = os.path.join(DIR_PATH, "DO_NOT_DELETE_all_file_names.csv")
    df = pd.read_csv(csv_path)

    # Rename files back to original names
    for _, row in df.iterrows():
        original = row["original"]
        new = row["new"]
        try:  # Avoid crash if new file added after prefixing
            source = os.path.join(DIR_PATH, new)
            dest = os.path.join(DIR_PATH, original)
            if os.path.exists(source) and not os.path.exists(dest):
                os.rename(source, dest)
        except TypeError:
            pass


def pre_change():
    """Reset filenames to original, then add new random prefixes."""
    try:
        path_reset()
    except (FileNotFoundError, TypeError):
        pass  # Silently handle missing files or CSV errors
    add_random_prefixes()


def status(choice):
    """Update CSV column name based on user choice.

    Args:
        choice (str): User selection ('rs' or 'cb').
    """
    if choice == 'rs':
        csv_path = os.path.join(DIR_PATH, "DO_NOT_DELETE_all_file_names.csv")
        df = pd.read_csv(csv_path)
        df.rename(columns={'unchanged': 'prefixed'}, inplace=True)
        df.to_csv(csv_path, index=False)
    elif choice == 'cb':
        csv_path = os.path.join(DIR_PATH, "DO_NOT_DELETE_all_file_names.csv")
        df = pd.read_csv(csv_path)
        df.rename(columns={'prefixed': 'unchanged'}, inplace=True)
        df.to_csv(csv_path, index=False)


def main():
    """Main loop to handle user input and file operations."""
    store_original_file_names()  # Check and update CSV at startup

    running = True
    while running:
        choice = input(
            "Choose an action:\n"
            "  'rs' - Randomly sort files with numbered prefixes\n"
            "  'cb' - Change back to original names\n"
            "  'rp' - Remove prefixes and recreate CSV (if missing)\n"
            "         (Note: files originally starting with a number may have that number removed)\n"
            "  'ex' - Exit\n"
            "Your choice: "
        ).lower()

        if choice == "rs":
            files = [f for f in os.listdir(DIR_PATH) if os.path.isfile(os.path.join(DIR_PATH, f))]
            initialize_number_list(len(files))
            pre_change()
            status(choice)
            print("Files randomized successfully!")
        elif choice == "cb":
            path_reset()
            status(choice)
            print("Files returned to normal!")
        elif choice == "rp":
            remove_prefixes()
            print("Prefixes removed and CSV recreated!")
        elif choice == "ex":
            print("Exiting program. Goodbye!")
            running = False
        else:
            print("Invalid input. Please try 'rs', 'cb', 'rp', or 'ex'.")


if __name__ == "__main__":
    main()