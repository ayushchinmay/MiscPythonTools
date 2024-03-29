import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

DIRPATH = "D:/AYUSH Documents/MSU/12_SPRING 2024/ECE 407/Lab3/"

suptitle_font = {'family': 'sans', 'color': '#212529', 'weight': 'bold', 'size': 16}
label_font = {'family': 'sans', 'color': '#495057', 'weight': 'normal', 'style':'oblique', 'size': 10}
title_font = {'family': 'sans', 'color': '#212529', 'weight': 'normal', 'size': 12}

colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]
marker1 = dict(linestyle='-', linewidth=1.5, marker='h', markersize=7, color=colors[0], markerfacecolor=colors[2])
marker2 = dict(linestyle='-', linewidth=1.5, marker='H', markersize=7, color=colors[4], markerfacecolor=colors[1])
markero = dict(linestyle='-', linewidth=1.5, marker='o', markersize=5, color=colors[0], markerfacecolor=colors[2])
markerO = dict(linestyle='-', linewidth=1.5, marker='o', markersize=5, color=colors[2], markerfacecolor=colors[0])


def find_s2p_files(fn=None):
    """
    Find and list all S2P file in the directory path.
    Select a file to read the data from.

    @return None
    """
    # Find all the .s2p files in the directory
    files = os.listdir(DIRPATH)
    s2p_files = [f for f in files if f.endswith(".s2p")]
    
    print(f"[INFO] S2P Files Found: {len(s2p_files)}")
    print("="*50)
    for i,f in enumerate(s2p_files):
        print(f"\t- [{i:^3}] {f}")
    print("="*50)
    
    fnum = fn if (isinstance(fn,int)) else input("  >> Select File: ")
    fname = s2p_files[int(fnum)]
    print(f"[INFO] Reading File: {fname}")
    print("="*50)
    
    while True:
        try:
            data = read_s2p_data(fname)
            return (fname,data)
        except ValueError:
            print(f"[ERROR] Invalid input. Please enter a valid integer.")
            print("-"*50)
            fname = input("  >> Select File: ")
            print("="*50)


def read_s2p_data(fname):
    """
    Read the S2P file and return the data as a pandas dataframe.

    @param fname: str - The name of the S2P file to read.
    @return df  : pd.DataFrame - The data from the S2P file.
    """
    with open(DIRPATH + fname, 'r') as fp:
        df = pd.DataFrame(columns=["Freq (Hz)", "S11 (Real)", "S11 (Imag)", "S21 (Real)", "S21 (Imag)", "S12 (Real)", "S12 (Imag)", "S22 (Real)", "S22 (Imag)"])
        lines = fp.readlines()
        print(f"[OPTIONS]: {lines[0]}")
        for n,lin in enumerate(lines[1:]):
            lineData = lin.split()
            df.loc[n] = [float(lineData[0]), float(lineData[1]), float(lineData[2]), float(lineData[3]), float(lineData[4]), float(lineData[5]), float(lineData[6]), float(lineData[7]), float(lineData[8])]
        print(df.head())
    return df


def plot_all_params(data, fname, save=False, show=True):
    plot_s2p_data(data, fname, param="S11", save=save, show=show)
    plot_s2p_data(data, fname, param="S21", save=save, show=show)


def plot_s2p_data(data, fname, param="S11", save=False, show=True):
    """
    Plot the S2P data.

    @param data : pd.DataFrame - The S2P data to plot.
    @param save : bool - Whether to save the plot.
    @param show : bool - Whether to display the plot.
    @return None
    """
    # Plot the data
    # fig = plt.subplots(2,2, figsize=(10,6), facecolor='#f5f5f5')
    fig = plt.figure(figsize=(10,6), facecolor='#f5f5f5', dpi=100)
    fig.suptitle(f"Plot: S{param}-Plot | File: {fname}", fontdict=suptitle_font)

    gs = gridspec.GridSpec(4,8)
    ax0 = plt.subplot(gs[0:2,0:4])
    ax1 = plt.subplot(gs[2:4,0:4])
    ax2 = plt.subplot(gs[:,4:8])

    s11_mag = pd.Series(20*np.log10(np.abs(data[f"{param} (Real)"]+1j*data[f"{param} (Imag)"])))
    s11_ang = np.angle(data[f"{param} (Real)"]+1j*data[f"{param} (Imag)"], deg=True)
    s11_min_index = np.argmin(s11_mag)

    ax0.minorticks_on()
    ax0.grid(True, which='major', linestyle='--', linewidth=0.75, color='#cbcbcb')
    ax0.set_title(f"{param} Magnitude", fontdict=title_font)
    ax0.set_ylabel("Magnitude (dB)", fontdict=label_font)
    ax0.set_xlabel("Frequency (Hz)", fontdict=label_font)
    ax0.set_xlim(min(data["Freq (Hz)"]), max(data["Freq (Hz)"]))
    # Plot Magnitude
    ax0.plot(data["Freq (Hz)"], s11_mag, color=colors[0], label="Magnitude")
    ax0.axvline(x=data["Freq (Hz)"][s11_min_index], color='black', linestyle='--', linewidth=0.75, label="Min")
    ax0.axhline(y=s11_mag[s11_min_index], color='black', linestyle='--', linewidth=0.75)

    ax1.minorticks_on()
    ax1.grid(True, which='major', linestyle='--', linewidth=0.75, color='#cbcbcb')
    ax1.set_title(f"{param} Phase", fontdict=title_font)
    ax1.set_ylabel("Phase (deg)", fontdict=label_font)
    ax1.set_xlabel("Frequency (Hz)", fontdict=label_font)
    ax1.set_xlim(min(data["Freq (Hz)"]), max(data["Freq (Hz)"]))
    ax1.set_ylim(-200, 200)
    # Plot Phase
    ax1.plot(data["Freq (Hz)"], s11_ang, color=colors[1], label="Phase")
    ax1.axvline(x=data["Freq (Hz)"][s11_min_index], color='black', linestyle='--', linewidth=0.75)
    ax1.axhline(y=s11_ang[s11_min_index], color='black', linestyle='--', linewidth=0.75)
    ax1.set_yticks( np.linspace(-180, 180, 7) )

    ax2.minorticks_on()
    ax2.grid(True, which='major', linestyle='--', linewidth=0.75, color='#cbcbcb')
    ax2.set_title(f"{param} Polar", fontdict=title_font)
    ax2.set_ylabel("Imaginary", fontdict=label_font)
    ax2.set_xlabel("Real", fontdict=label_font)
    # Plot Polar Coordinates
    ax2.plot(data[f"{param} (Real)"], data[f"{param} (Imag)"], color=colors[2])
    ax2.plot(data[f"{param} (Real)"][0], data[f"{param} (Imag)"][0], **markero, label="Start")
    ax2.plot(data[f"{param} (Real)"][len(data)-1], data[f"{param} (Imag)"][len(data)-1], **markerO, label="End")
    ax2.plot(data[f"{param} (Real)"][s11_min_index], data[f"{param} (Imag)"][s11_min_index], **marker2, label="Min")
    ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.75)
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=0.75)
    
    # Adjust layout to prevent overlap
    fig.tight_layout()
    # ax0.legend(loc='lower right')
    # ax1.legend(loc='lower right')
    ax2.legend(loc='lower right')

    if show:
        plt.show()
    if save:
        fig.savefig(DIRPATH + f"Plots/{fname[:-4]}_{param}.png", dpi=300, bbox_inches='tight')
        print(f"[SAVE PLOT IMAGE]")
        print(f">> Image File:\t{DIRPATH}/Plots/{fname[:-4]}_{param}.png")


def main():
    """
    Main function to run the S2P plotter.
    """
    fname,data = find_s2p_files()
    plot_all_params(data, fname, save=False, show=True)

    # # Read the S2P file into a pandas dataframe
    # for i in range(8):
    #     fname,data = find_s2p_files(i)
    #     plot_all_params(data, fname, save=True, show=False)


if __name__ == "__main__":
    main()