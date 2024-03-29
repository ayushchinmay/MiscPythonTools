import os
import matplotlib.pyplot as plt
import numpy as np
import h5py

### PATHS ###
#** Please update the path to directory containing the .H5 files**#
PATH_H5 = "D:/AYUSH Documents/MSU/12_SPRING 2024/ECE 407/Lab2/Data_h5/"

### GLOBALS ###
scopeData = dict()
label_font = {'family': 'sans', 'color': '#001524', 'weight': 'normal', 'style':'oblique', 'size': 12}
title_font = {'family': 'sans', 'color': '#15616d', 'weight': 'bold', 'size': 18}
colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

### FUNCTIONS ###
def read_h5_data(fname):
    """
    Read the h5 file and return the h5py file object
    param: fname: str: name of the h5 file
    return: h5py.File: h5 file object
    """
    # Rename the file if not in h5 format
    fn = PATH_H5 + fname + ".h5" if ".h5" not in fname else PATH_H5 + fname

    try:    # Read the h5 file
        print(f"[READ H5 DATA]")
        print(f">> File Name:\t{fname}")
        print(f">> File Path:\t{fn}\n")
        print(f"{'─'*(len(fname)+4)}\n│ {fname} │\n{'─'*(len(fname)+4)}")

        fh5 = h5py.File(fn, "r")
        return fh5

    except Exception as e:  # Error reading the h5 file
        print(f"\n>> [ERROR!] Error reading {fname}: {str(e)}\n")


def print_h5_tree(h5data, level=0):
    """
    Print the h5 file tree structure recursively
    param: h5data: h5py.File: h5 file to print
    param: level: int: level of the tree
    """

    if level==0:
        # print(f"{h5data.filename}\n{h5data}")
        pass

    for key in h5data.keys():   # Print the tree structure by iterating through the keys
        print("\t" * (level+1) + "└" + "─" * (level) + "─ " + key)

        if isinstance(h5data[key], h5py.Group): # If the key is a group, call the function recursively
            print_h5_tree(h5data[key], level + 1)
        else:                                   # If the key is a dataset, print the dataset and store it in a dictionary
            print("\t" * (level+1) + "└" + "─" * (level+1) + "─ " + str(h5data[key]))
            print("\t" * (level+2) + "└─> " + str(h5data[key][:5]))
            scopeData[str(key)] = h5data[key][()]


def roll_n_avg(data, window=3):
    """
    Compute the sliding average of the data by shifting the data left and right by 1 for each window
    param: data: np.array: data to compute the sliding average
    param: window: int: size of the sliding window
    return: np.array: sliding average of the data
    """
    ndata = np.zeros(len(data))
    if window % 2 == 0: window += 1
    for i in range(1, (window-1)//2+1):
        ndata += np.roll(data,i) + np.roll(data,-i)
    return (ndata + data) / window


def plot_data(fname, save=False, show=True):
    """
    Plot the time vs voltage data
    param: data: pd.DataFrame: dataframe containing time and voltage data
    """
    # Initialize the figure and axis
    print(f"[PLOT CHANNEL DATA]:\t{len(scopeData)} Channels")
    fig,axs = plt.subplots(nrows=len(scopeData), ncols=1, figsize=(12,3*len(scopeData)), facecolor='#f5f5f5', constrained_layout=True) #, sharex=True
    fig.suptitle(f"Oscilloscope Capture: {fname}", weight='bold', size=14, color='#626262')
    axs = [axs] if len(scopeData) == 1 else axs # Convert to list if only one channel

    # Variables for subplots and channels
    chan, splt = 1, 0

    while splt <= len(scopeData) and chan <= 4: # Plot the data for each channel
        try:    # Try to plot the channel data
            axs[splt].plot(scopeData[f"Channel {chan} Data"], label=f"CHAN-{chan}", color=colors[splt], linewidth=1.45)

            # Plot Smoothed Data
            rolln = roll_n_avg(scopeData[f"Channel {chan} Data"], 15)
            axs[splt].plot(rolln, label="AVG-15", color="#101010", linewidth=0.65, linestyle="-")

            axs[splt].minorticks_on()
            axs[splt].grid(True, which='major', linestyle='--', linewidth=0.5, color='#bcbcbc')
            axs[splt].set_xlim(0, len(scopeData[f"Channel {chan} Data"]))
            # axs[splt].set_ylim(min(scopeData[f"Channel {chan} Data"]), max(scopeData[f"Channel {chan} Data"]))
            axs[splt].set_xlabel("Time (s)", fontdict=label_font)
            axs[splt].set_ylabel("Amplitude (V)", fontdict=label_font)
            axs[splt].legend(loc='upper right')

            # Annotation: Peak-to-Peak Voltage
            Vmin = min(scopeData[f"Channel {chan} Data"])
            Vmax = max(scopeData[f"Channel {chan} Data"])
            Vpp = Vmax-Vmin
            axs[splt].axhline(y=Vmax, color='#555555', linestyle='-.', linewidth=0.85)
            axs[splt].axhline(y=Vmin, color='#555555', linestyle='-.', linewidth=0.85)
            # axs[splt].annotate(f"Peak-to-Peak: {Vpp:.2f}V", xy=(30, (Vmin+Vmax)/2), xycoords='data', fontsize=10, color='black')
            # Arrow from text to Vmax
            axs[splt].annotate("", xy=(150, Vmax), xytext=(150, Vmin), xycoords='data', arrowprops=dict(arrowstyle='<->', color='#555555'))
            axs[splt].text(40, (Vmin+Vmax)/2, f"Peak-to-Peak: {Vpp:.2f}V", color='#555555', bbox=dict(facecolor='white', edgecolor='#555555'))

            # print(f"[PLOTTING] Channel-{chan}, Subplot-{splt}")
            chan += 1
            splt += 1
        except:     # If the channel does not exist, skip to the next channel
            # print(f"[SKIP] Channel-{chan}, Subplot-{splt}")
            chan += 1 

    if save:    # Save the plot as a png file
        if not os.path.exists(PATH_H5 + "plotPNG"):
            os.makedirs(PATH_H5 + "plotPNG")

        plt.savefig(PATH_H5 + f"plotPNG/{fname.split('.')[0]}.png", dpi=600, bbox_inches='tight')
        print(f"[SAVE PLOT IMAGE]:\t{len(scopeData)} Channels")
        print(f">> Image File:\t{PATH_H5}/{fname.split('.')[0]}.png")
    print("─"*100 + "\n")  

    if show:    # Show the plot
        plt.show()



def read_plot_save_all_h5_files():
    """
    Read all the h5 files in the directory and plot the data
    """
    dirlist = os.listdir(PATH_H5)
    print(f"[READING DIRECTORY]")
    print(f">> Directory:\t{PATH_H5}\n>> Total Files:\t{sum('.h5' in fil for fil in dirlist)}")

    print(f">> Files: \n")
    for i in range(1, len(dirlist)):
        print(f"\t- {dirlist[i]}", end="\n" if (i)%6==0 else "\t")
    print()

    # print(*dirlist[1:], sep="\n\t- ")
    print("─"*150 + "\n")
    
    for fil in dirlist:
        if ".h5" in fil:
            h5data = read_h5_data(fil)            # Read the h5 file
            print_h5_tree(h5data)                   # Print the h5 file tree
            print("─"*100)  
            plot_data(fil, save=True, show=False)   # Plot the data


def main():
    # fname = "scope_2.h5"
    # h5data = read_h5_data(fname)            # Read the h5 file
    # print_h5_tree(h5data)                   # Print the h5 file tree
    # plot_data(fname, save=True, show=True)   # Plot the data
    read_plot_save_all_h5_files()
    

if __name__ == "__main__":
    main()