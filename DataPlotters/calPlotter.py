import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator

DIRPATH = "C:/Users/ayush/Downloads/NanoVNASaver.win.x64/"

suptitle_font = {'family': 'sans', 'color': '#212529', 'weight': 'bold', 'size': 16}
label_font = {'family': 'sans', 'color': '#495057', 'weight': 'normal', 'style':'oblique', 'size': 10}
title_font = {'family': 'sans', 'color': '#212529', 'weight': 'normal', 'size': 12}

colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5", "#f78104"]


def read_cal_file(fname):
    """
    Read the CAL file and return the data as a pandas dataframe.

    @param fname: str - The name of the S2P file to read.
    @return df  : pd.DataFrame - The data from the S2P file.
    """
    with open(DIRPATH + fname, 'r') as fp:
        df = pd.DataFrame(columns=["Freq (Hz)", "Short (Real)", "Short (Imag)", "Open (Real)", "Open (Imag)", "Load (Real)", "Load (Imag)", "Through (Real)", "Through (Imag)", "ThroughRefl (Real)", "ThroughRefl (Imag)", "Isolation (Real)", "Isolation (Imag)"])
        lines = fp.readlines()

        print(f"[OPTIONS]: {lines[2]}")
        for n,lin in enumerate(lines[3:]):
            lineData = lin.split()
            df.loc[n] = [float(lineData[0]), float(lineData[1]), float(lineData[2]), float(lineData[3]), float(lineData[4]), float(lineData[5]), float(lineData[6]), float(lineData[7]), float(lineData[8]), float(lineData[9]), float(lineData[10]), float(lineData[11]), float(lineData[12])]
            # print(lineData)
        print(df.head())
    return df


def plot_cal_data(data, save=False, show=True):
    """
    Plot the S2P data.
    """
    # Plot the data
    # fig = plt.subplots(2,2, figsize=(10,6), facecolor='#f5f5f5')
    fig = plt.figure(figsize=(10,6), facecolor='#f5f5f5', dpi=100)
    fig.suptitle(f"Calibration Data", fontdict=suptitle_font)

    # gs = gridspec.GridSpec(4,8)
    axs = fig.subplots(6,1, sharex=True)

    # axs[0].set_title("Short", fontdict=title_font)
    axs[0].set_xlim(min(data["Freq (Hz)"]), max(data["Freq (Hz)"]))
    axs[5].set_xlabel("Frequency (Hz)", fontdict=label_font)
    axs[3].set_ylabel("Complex Value", fontdict=label_font)

    axs[0].plot(data["Freq (Hz)"], data["Short (Real)"]+1j*data["Short (Imag)"], color=colors[0], label="Short")
    axs[1].plot(data["Freq (Hz)"], data["Open (Real)"]+1j*data["Open (Imag)"], color=colors[1], label="Open")
    axs[2].plot(data["Freq (Hz)"], data["Load (Real)"]+1j*data["Load (Imag)"], color=colors[2], label="Load")
    axs[3].plot(data["Freq (Hz)"], data["Through (Real)"]+1j*data["Through (Imag)"], color=colors[3], label="Through")
    axs[4].plot(data["Freq (Hz)"], data["ThroughRefl (Real)"]+1j*data["ThroughRefl (Imag)"], color=colors[4], label="ThroughRefl")
    axs[5].plot(data["Freq (Hz)"], data["Isolation (Real)"]+1j*data["Isolation (Imag)"], color=colors[5], label="Isolation")
    
    # Adjust layout to prevent overlap
    fig.tight_layout()
    for i in range(6):
        axs[i].minorticks_on()
        axs[i].grid(True, which='major', linestyle='--', linewidth=0.75, color='#cbcbcb')
        axs[i].legend(loc='upper left')

    if show:
        plt.show()
    if save:
        fig.savefig(DIRPATH + f"calPlot.png", dpi=300, bbox_inches='tight')
        print(f"[SAVE PLOT IMAGE]")
        print(f">> Image File:\t{DIRPATH}calPlot.png")


def main():
    """
    Main function to run the S2P plotter.
    """
    data = read_cal_file("CalibrationFile.cal")
    plot_cal_data(data, save=False, show=True)


if __name__ == "__main__":
    main()