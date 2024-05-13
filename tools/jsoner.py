import json
import logging
import config_logging

#Logging Configurarion
logger = logging.getLogger(__name__)
log_level = getattr(logging, config_logging.logging_level.upper())
logging.basicConfig(level=log_level)
# logger.setLevel(logging.config_logging.logging_level)
file_handler = logging.FileHandler(config_logging.logging_file)
logger.addHandler(file_handler)

# Function to create a JSON file
def creator(json_data, json_filename, variable=None):
  """
  This function takes JSON data, a filename to save it as, and an optional variable name.
  - If a variable name is provided, it wraps the JSON data within a dictionary using the variable as the key.
  - Otherwise, it uses the raw JSON data.
  - It then constructs the output filename by prepending "json_" to the provided filename and appending ".json".
  - The function opens the file for writing, dumps the formatted data with indentation, closes the file,
  and prints a message indicating successful save location.
  """
  if variable != None:
    data = {variable: json_data}  # Wrap data in a dictionary if variable is provided
  else:
    data = json_data

  output_file = json_filename  # Construct output filename

  with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent=4)  # Dump data with indentation

  logging.info(f"JSON data saved to: {output_file}")

# Function to load data from a JSON file
def loader(json_file, variable=None):
  """
  This function loads data from a JSON file and returns the value for a specific variable (if provided).
  - It attempts to open the file for reading.
  - If successful, it loads the JSON data.
  - If a variable name is provided, it checks if the variable exists as a key in the loaded data dictionary.
    - If the variable exists, it returns the value associated with that key.
    - If the variable doesn't exist, it prints an error message and returns None.
  - If no variable name is provided, the entire loaded data dictionary is returned.
  - In case of a FileNotFoundError, it prints an error message, exits the program with an exit code of 1.
  """
  try:
    with open(json_file, 'r') as f:
      data = json.load(f)
      if variable != None:
        if variable in data:  # Check if the key exists in the dictionary
          return data[variable]
        else:
          logger.warning(f"Error: Variable '{variable}' not found in JSON data.")
          return None
      else:
        return data
  except FileNotFoundError:
    logger.critical(f"Error: JSON file '{json_file}' not found. Please generate the JSON first.")
    exit(1)

# Function to count entries under a variable in JSON data (assuming it's a list)
def counter(json_file, variable=None):
  """
  This function first calls the loader function to load data from the JSON file based on the variable.
  - If data is loaded successfully (not None), it calculates the number of entries in the data (assuming it's a list).
  - It then prints a message indicating the number of entries under the variable and returns the count.
  - If data loading fails (returns None), the function also returns None.
  """
  loaded_data = loader(json_file, variable)
  if loaded_data is not None:
    num_entries = len(loaded_data)
    logger.info(f"Number of entries under '{variable}': {num_entries}")
    return num_entries
  else:
    return None

def TextToJSON(txt_file, filename=None):
  """
  This function converts a text file into a list of JSON-like elements, assuming each line represents an element.

  Args:
      txt_file (str): Path to the text file to be converted.
      filename (str, optional): Optional filename for the output JSON file (not currently used).

  Returns:
      list: A list of JSON-like elements (strings), potentially with leading/trailing whitespace removed.
  """

  # Open the text file for reading with a 'with' statement for automatic closing
  with open(txt_file, "r") as file:
    # Read the entire content of the file
    text_content = file.read()

    # Split the text content into a list of lines
    lines = text_content.splitlines()

    # Remove leading/trailing whitespaces from each line and create a new list
    json_list = [line.strip() for line in lines]

  # Call the creator function (functionality not defined here)
  creator(json_list, filename, None)

  if filename is None:
    # Since the filename argument is not currently used, we can just return the list
    return json_list

import json


def appender(json_filename, json_data, variable=None):
  """
  Appends JSON data to the specified file.

  Args:
      json_data (dict or list): The data to be appended.
      json_filename (str): Path to the JSON file.
      variable (str, optional): Optional variable name to wrap the data in a dictionary. Defaults to None.

  Returns:
      bool: True if successful, False otherwise.
  """

  try:
    # Construct output filename
    output_file = json_filename

    # Open the existing file for reading (assuming it exists)
    with open(output_file, 'r') as json_file:
      try:
        # Load existing data (handling potential empty file)
        existing_data = json.load(json_file)
      except json.JSONDecodeError:
        # If the file is empty, existing_data will be an empty list or object
        existing_data = []

    # Check if existing data is a list or a dictionary
    if not isinstance(existing_data, (list, dict)):
      logger.error(f"Error: Existing data in '{output_file}' has unexpected type: {type(existing_data)}")
      return False

    # Wrap data in a dictionary if a variable is provided
    appended_data = {variable: json_data} if variable else json_data

    # Combine existing data and appended data
    combined_data = existing_data + appended_data

    # Open the file for writing (overwriting existing content)
    with open(output_file, 'w') as json_file:
      json.dump(combined_data, json_file, indent=4)

    logger.info(f"JSON data saved to: {output_file}")
    return True

  except FileNotFoundError:
    logger.error(f"Error: File '{output_file}' not found.")
    return False
  except json.JSONDecodeError:
    logger.critical(f"Error: Failed to decode existing JSON data in '{output_file}'.")
    return False
