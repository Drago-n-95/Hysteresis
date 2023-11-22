from tkinter import Tk, filedialog

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import os


def load_data(file_path):

    # Initialize lists to store lines for each DataFrame
    set1_lines = []
    set0_lines = []

    # Set a flag to indicate which set we are currently reading
    current_set = None

    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Identify the start of each DataFrame
            if line.startswith("Set 1:"):
                current_set = "Set 1"
                continue
            elif line.startswith("Set 0:"):
                current_set = "Set 0"
                continue

            # Append lines to the corresponding set
            if current_set == "Set 1":
                set1_lines.append(line)
            elif current_set == "Set 0":
                set0_lines.append(line)
    
    # Create DataFrames from the lists
    set1_df = pd.read_csv(io.StringIO('\n'.join(set1_lines)), sep='\t')
    set0_df = pd.read_csv(io.StringIO('\n'.join(set0_lines)), sep='\t')

    selected_columns = ['mag / emu / g', 'temp / centigrade']

    df_set1_selected = set1_df[selected_columns]
    df_set0_selected = set0_df[selected_columns]

    return df_set1_selected, df_set0_selected

def normalize_data(df):
    # Calculate the derivative using numpy's gradient function
    df['mag_normalized'] = np.gradient(df['mag / emu / g'], df['temp / centigrade'])

    return df
def plot_data(df1_original, df1_normalized, df0_original, df0_normalized, sample_name):
    # Plot the original 'mag / emu / g' against 'temp / centigrade'
    plt.subplot(211)
    plt.plot(df1_original['temp / centigrade'], df1_original['mag / emu / g'], 'r')
    plt.plot(df0_original['temp / centigrade'], df0_original['mag / emu / g'], 'b')
    plt.title('Sample ' + sample_name + ' - Original Data')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Magnetization (emu/g)')

    index_min_value_set1_normalized = df1_normalized['mag_normalized'].idxmin()
    df0_normalized_copy = df0_normalized.copy()

    df0_normalized_copy = df0_normalized_copy[::-1]
    df0_normalized_copy = df0_normalized_copy.drop(0)

    index_min_value_set0_normalized = df0_normalized_copy['mag_normalized'].idxmin()

    min_value_set1_normalized_temp = df1_normalized['temp / centigrade'][index_min_value_set1_normalized]
    min_value_set0_normalized_temp = df0_normalized['temp / centigrade'][index_min_value_set0_normalized]

    # Plot the normalized 'mag / emu / g' against 'temp / centigrade'
    plt.subplot(212)
    plt.plot(df1_normalized['temp / centigrade'], df1_normalized['mag_normalized'], 'r')
    plt.plot(df0_normalized['temp / centigrade'], df0_normalized['mag_normalized'], 'b')
    plt.axvline(x=min_value_set1_normalized_temp, color='r', linestyle='--', label=min_value_set1_normalized_temp)
    plt.axvline(x=min_value_set0_normalized_temp, color='b', linestyle='--', label=min_value_set0_normalized_temp)
    plt.title(f'Heating Temperature (°C) = {min_value_set1_normalized_temp}°; Cooling Temperature (°C) = {min_value_set0_normalized_temp}°')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Derivative')

    plt.tight_layout()
    plt.show()

def main():
    # Create a Tkinter window to select the file
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(title="Select a data file", filetypes=[("Text files", "*.rmp")])
    filename = os.path.basename(file_path)
    sample_name, extension = os.path.splitext(filename)

    if not file_path:
        print("No file selected. Exiting.")
        return

    # Load and process the data
    df_set1_original, df_set0_original = load_data(file_path)
    df_set1_normalized = normalize_data(df_set1_original.copy())
    df_set0_normalized = normalize_data(df_set0_original.copy())

    # Plot the data
    plot_data(df_set1_original, df_set1_normalized, df_set0_original, df_set0_normalized, sample_name)

if __name__ == "__main__":
    main()
