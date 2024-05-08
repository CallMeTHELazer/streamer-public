import os

def replace_spaces_in_filenames(directory):
  """
  Replaces spaces in filenames within a directory and its subdirectories.

  Args:
      directory: The path to the directory to process.
  """
  if os.path.isdir(directory):
    for root, _, files in os.walk(directory):
      for filename in files:
        # Construct old and new filenames
        old_path = os.path.join(root, filename)
        new_filename = filename.replace(" ", "_")
        new_path = os.path.join(root, new_filename)

        # Check if filenames are different
        if old_path != new_path:
          # Rename the file if filenames differ
          os.rename(old_path, new_path)
          print(f"Renamed: {old_path} to {new_path}")
  else:
    print(f"Directory '{directory}' does not exist. Skipping...")

# Target directories
target_directories = ["/HDD_1/plexmedia/movies", "/HDD_2/plexmedia/movies"]

# Process each directory
for directory in target_directories:
  replace_spaces_in_filenames(directory)

print("Finished renaming files.")
