import os
import shutil
import csv

def write_text_file(filename, content):
    try:
        # Open the file in write mode and write the content
        with open(filename, "w") as f:
            f.write(content)
        print(f"Written: {filename}")
    except IOError as e:
        # If writing fails, print the error
        print(f"Error writing file: {e}")

def read_text_file(filename):
    try:
        # Open the file in read mode and get all lines
        with open(filename, "r") as f:
            lines = f.readlines()
        print(f"\nContents of {filename}:")
        for i, line in enumerate(lines, 1):
            # rstrip removes the trailing newline from each line
            print(f"  Line {i}: {line.rstrip()}")
        return lines
    except FileNotFoundError:
        # File does not exist at the given path
        print(f"File not found: {filename}")
    except IOError as e:
        print(f"Could not read: {e}")

def write_csv_file(filename, headers, rows):
    try:
        # newline="" prevents extra blank lines on Windows
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            # Write the header row first
            writer.writerow(headers)
            # Write all data rows at once
            writer.writerows(rows)
        print(f"CSV written: {filename}")
    except IOError as e:
        print(f"Error writing CSV: {e}")

def read_csv_file(filename):
    try:
        with open(filename, "r", newline="") as f:
            # DictReader maps each row to a dictionary using headers as keys
            reader = csv.DictReader(f)
            print(f"\nContents of {filename}:")
            for row in reader:
                print(f"  {dict(row)}")
    except FileNotFoundError:
        print(f"CSV not found: {filename}")

def rename_file(old_name, new_name):
    try:
        # Rename the file from old_name to new_name
        os.rename(old_name, new_name)
        print(f"\nRenamed: {old_name} -> {new_name}")
    except FileNotFoundError:
        print(f"File not found: {old_name}")
    except PermissionError:
        print(f"Permission denied: {old_name}")

def move_file(source, dest_folder):
    try:
        # Create the destination folder if it doesn't already exist
        os.makedirs(dest_folder, exist_ok=True)
        # Move the file into the destination folder
        shutil.move(source, dest_folder)
        print(f"Moved {source} to {dest_folder}/")
    except FileNotFoundError:
        print(f"Source not found: {source}")
    except shutil.Error as e:
        print(f"Move failed: {e}")

def delete_file(filename):
    try:
        # Permanently delete the file from the system
        os.remove(filename)
        print(f"Deleted: {filename}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except PermissionError:
        print(f"Permission denied: {filename}")

if __name__ == "__main__":
    # Write and read a text file
    write_text_file("notes.txt", "Hello from Alfido Tech!\nPython file handling is simple.\nLine 3 here.")
    read_text_file("notes.txt")

    # Write and read a CSV file
    headers = ["Name", "Age", "Score"]
    rows = [["Alice", 21, 88], ["Bob", 23, 75], ["Carol", 22, 92], ["David", 24, 60]]
    write_csv_file("students.csv", headers, rows)
    read_csv_file("students.csv")

    # Rename the file, move it to archive folder, then delete the CSV
    rename_file("notes.txt", "renamed_notes.txt")
    move_file("renamed_notes.txt", "archive")
    delete_file("students.csv")

    # Error handling demo - trying to read a file that doesn't exist
    print("\nTrying to read a missing file:")
    read_text_file("missing.txt")
