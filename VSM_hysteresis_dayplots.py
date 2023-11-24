from tkinter import Tk, filedialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import os


def load_data_hys(file_path):
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            # Join lines into a single string
            file_content = "\n".join(file.readlines())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    # Create a DataFrame with the required columns
    columns = ["Field [T]", "Moment [Am²]", "Adjusted Field [T]", "Adjusted Moment [Am²]"]
    data_file = []
    # Read the content line by line and extract the relevant information
    lines = file_content.split('\n')
    for line in lines:  # Considering the first 82 lines
        if line.startswith("+") or line.startswith("-"):
            # Extract data from lines starting with "+" or "-"
            data_file.append(line)

    df = pd.read_csv(io.StringIO('\n'.join(data_file)))
    df.columns = columns

    return df

def load_data_irm(file_path_irm):
    try:
        with open(file_path_irm, 'r', encoding='ISO-8859-1') as file:
            # Join lines into a single string
            file_content = "\n".join(file.readlines())
    except FileNotFoundError:
        print(f"File not found: {file_path_irm}")
        return None

    # Create a DataFrame with the required columns
    columns = ["Field [T]", "Remanence [Am²]"]
    data_file = []
    # Read the content line by line and extract the relevant information
    lines = file_content.split('\n')
    for line in lines:
        if line.startswith("+") or line.startswith("-"):
            # Extract data from lines starting with "+" or "-"
            data_file.append(line)

    df = pd.read_csv(io.StringIO('\n'.join(data_file)))
    df.columns = columns

    return df

def load_data_coe(file_path_coe):
    try:
        with open(file_path_coe, 'r', encoding='ISO-8859-1') as file:
            # Join lines into a single string
            file_content = "\n".join(file.readlines())
    except FileNotFoundError:
        print(f"File not found: {file_path_coe}")
        return None

    # Create a DataFrame with the required columns
    columns = ["Field [T]", "Remanence [Am²]"]
    data_file = []
    # Read the content line by line and extract the relevant information
    lines = file_content.split('\n')
    for line in lines:
        if line.startswith("+") or line.startswith("-"):
            # Extract data from lines starting with "+" or "-"
            data_file.append(line)

    df = pd.read_csv(io.StringIO('\n'.join(data_file)))
    df.columns = columns

    return df

def plot_data(df_hys, df_irm, df_coe, sample_name):
    # Plot the hysteresis loop
    plt.subplot(221)
    plt.axvline(x=0., color='k')
    plt.axhline(y=0., color='k')
    plt.plot(df_hys["Adjusted Field [T]"], df_hys["Adjusted Moment [Am²]"], 'r')
    hys_Ms = np.interp(0, df_hys["Adjusted Field [T]"][:50], df_hys["Adjusted Moment [Am²]"][:50])
    hys_Mrs = np.interp(0, df_hys["Adjusted Field [T]"][245:255], df_hys["Adjusted Moment [Am²]"][245:255])
    hys_Bc = np.interp(0, df_hys["Adjusted Moment [Am²]"][247:254], df_hys["Adjusted Field [T]"][247:254])

    if hys_Mrs<0:
        hys_Mrs = hys_Mrs*(-1)

    if hys_Bc<0:
        hys_Bc = hys_Bc*(-1)

    plt.axhline(y=hys_Ms, color='b', linestyle='--')
    plt.axhline(y=hys_Mrs, color='b', linestyle='--')
    plt.axvline(x=hys_Bc, color='b', linestyle='--')
    plt.axvline(x=-hys_Bc, color='b', linestyle='--')
    plt.text(-0.4, 5.0e-6, f"Ms = {hys_Ms:.2e} Am²", fontsize=11)
    plt.text(-0.4, 3.0e-6, f"Mrs = {hys_Mrs:.2e} Am²", fontsize=11)
    plt.text(-0.4, 1.0e-6, f"Bc = {hys_Bc:.2e} T", fontsize=11)
    plt.ylim(-6e-6, 6e-6)
    print(hys_Ms, hys_Mrs, hys_Bc)
    plt.title('Hysteresis loop for sample ' + sample_name)
    plt.xlabel('Applied Field [T]')
    plt.ylabel('Magnetic Moment [Am²]')

    # IRM acquisition curve
    plt.subplot(222)
    plt.axvline(x=0., color='k')
    plt.axhline(y=0., color='k')
    plt.plot(df_irm["Field [T]"], df_irm["Remanence [Am²]"], 'r')
    plt.scatter(df_irm["Field [T]"], df_irm["Remanence [Am²]"], edgecolors='k')
    lenght_df = len(df_irm["Field [T]"])
    interp_y = np.interp(0, df_irm["Field [T]"][lenght_df-5:lenght_df-1], df_irm["Remanence [Am²]"][lenght_df-5:lenght_df-1])
    plt.axhline(y=interp_y, color='r', linestyle='--')
    plt.title('IRM acquisition curve for sample ' + sample_name)
    plt.text(0.2, 4.0e-7, f"IRM = {interp_y:.2e} Am²", fontsize=11)
    plt.xlabel('Applied Field [T]')
    plt.ylabel('Remanence [Am²]')

    # Back-field curve
    plt.subplot(223)
    plt.axvline(x=0., color='k')
    plt.axhline(y=0., color='k')
    plt.plot(df_coe["Field [T]"], df_coe["Remanence [Am²]"], 'r')
    plt.scatter(df_coe["Field [T]"], df_coe["Remanence [Am²]"], edgecolors='k')
    Bcr = np.interp(0, df_coe["Remanence [Am²]"][10:13], df_coe["Field [T]"][10:13])*(-1)
    plt.text(-0.4, 3.0e-7, f"Bcr = {Bcr:.2e} T", fontsize=11)
    plt.title('Back-field curve for sample ' + sample_name)
    plt.xlabel('Applied Field [T]')
    plt.ylabel('Remanence [Am²]')

    # Day plot
    plt.subplot(224)
    plt.axvline(x=0., color='k')
    plt.axhline(y=0., color='k')
    plt.scatter(Bcr/hys_Bc, hys_Mrs/hys_Ms, edgecolors='k')
    plt.axhline(y=0.5, color='k', linestyle='-')
    plt.axhline(y=0.01, color='k', linestyle='-')
    plt.axvline(x=2, color='k', linestyle='-')
    plt.axvline(x=5, color='k', linestyle='-')
    plt.text(1.45, 0.55, "SD", fontsize=11)
    plt.text(4.3, 0.42, "PSD", fontsize=11)
    plt.title('Day plot for sample ' + sample_name)
    plt.ylim(0.0, 0.6)
    plt.xlim(1, 6)
    plt.xlabel('Bcr/Bc')
    plt.ylabel('Mrs/Ms')

    plt.savefig("/home/dragomir/Downloads/Paleomagnetism/programming in python/munmagtools-master/playground/Thesis_works/" + sample_name + "_VSM_analysis.png", dpi=300)


    plt.show()

def main():
    # Create a Tkinter window to select the file
    root = Tk()
    root.withdraw()  # Hide the main window

    file_path_hys = filedialog.askopenfilename(title="Select a hys file", filetypes=[("Text files", "*.hys")])
    file_path_irm = filedialog.askopenfilename(title="Select an irm file", filetypes=[("Text files", "*.irm")])
    file_path_coe = filedialog.askopenfilename(title="Select a coe file", filetypes=[("Text files", "*.coe")])
    filename = os.path.basename(file_path_irm)
    sample_name, extension = os.path.splitext(filename)

    if not file_path_hys and not file_path_irm and not file_path_coe:
        print("No file selected. Exiting.")
        return

    # Load and process the data
    df_set_hys = load_data_hys(file_path_hys)
    df_set_irm = load_data_irm(file_path_irm)
    df_set_coe = load_data_coe(file_path_coe)

    # Plot the data
    plot_data(df_set_hys, df_set_irm, df_set_coe, sample_name)

if __name__ == "__main__":
    main()
