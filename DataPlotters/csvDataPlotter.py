import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import lfilter


PATH = "D:/AYUSH Documents/MSU/12_SPRING 2024/ECE 407/Lab3/"


def read_data(fname):
    """
    Read data from the csv file and return the time and voltage arrays
    param: fname: str: name of the file to read
    """
    scope_data = pd.read_csv(PATH + fname, skiprows=1)
    print(scope_data)
    return scope_data


label_font = {'family': 'sans', 'color': '#001524', 'weight': 'normal', 'style':'oblique', 'size': 12}
title_font = {'family': 'sans', 'color': '#15616d', 'weight': 'bold', 'style':'normal', 'size': 14}

def plot_data(data, fn="test1.png", save=False):
    """
    Plot the time vs voltage data
    param: data: pd.DataFrame: dataframe containing time and voltage data
    """
    plt.figure(figsize=(10,6), facecolor='#e9ecef')
    plt.axhline(y=0, color='#3e3e3e', linewidth=1.25)
    plt.plot(data['second'], data['Volt'], color='#e56b6f', linewidth=1.25)

    n = 128  # the larger n is, the smoother curve will be
    smooth_data = lfilter([1.0 / n] * n, 1, data['Volt'])
    # plt.plot(data['second'], smooth_data, color='#1f7a8c', linewidth=0.85)


    plt.grid(True, which='major', linestyle='--', linewidth=0.5, color='#15616d')
    plt.minorticks_on()

    plt.title(f"Oscilloscope Capture: {fn}", fontdict=title_font)
    plt.xlim([data['second'].min(), data['second'].max()])
    plt.xlabel("Time (s)", fontdict=label_font)
    plt.ylabel("Amplitude (V)", fontdict=label_font)
    plt.legend(["GND", "CH-1", "Filtered"], loc='upper right')

    plt.annotate("X1 = 0.070s", xy=(0.070, 0), xytext=(0.075, 0.005), fontsize=10, color='black', arrowprops=dict(facecolor='black', arrowstyle='->'), bbox=dict(boxstyle='round', edgecolor='black', facecolor='white'))
    plt.annotate("X2 = -0.025s", xy=(-0.025, 0), xytext=(-0.050, 0.005), fontsize=10, color='black', arrowprops=dict(facecolor='black', arrowstyle='->'), bbox=dict(boxstyle='round', edgecolor='black', facecolor='white'))
    plt.axvline(x=0.070, color='blue', linestyle='--', linewidth=1)
    plt.axvline(x=-0.025, color='blue', linestyle='--', linewidth=1)


    if save:
        plt.savefig(PATH + f"{fn[:-4]}.png", dpi=600, bbox_inches='tight')
        print(f"Plot saved as {PATH}/{fn[:-4]}.png")

    plt.show()


def main():
    fn = "scope_0.csv"
    scope= read_data(fn)
    plot_data(scope, fn, 1)


if __name__ == "__main__":
    main()