# Quick Python Tools
## 1. [ColorGradient](https://github.com/ayushchinmay/MiscPythonTools/blob/main/ColorGradient/colorGrad.py)
- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/colorGrad_ex1.png" width="600">
- Interpolates the provided list of colors with a specified number of steps to create a discrete gradient.
- Displays the discretized color gradient using Matplotlib.

## 2. Misc MatPlotLib Data Plotters
1. [Calibration Data Plotter](https://github.com/ayushchinmay/MiscPythonTools/blob/main/DataPlotters/calPlotter.py) <.cal>
	- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/calPlot_ex1.png" width="480">
	- Plots the calibration data received from [NanoVNA](https://nanovna.com/).

2. [CSV Data Plotter](https://github.com/ayushchinmay/MiscPythonTools/blob/main/DataPlotters/csvDataPlotter.py) <.csv>
	- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/csvPlot_ex1.png" width="480">
	- Plots the CSV data obtained from an oscilloscope.

3. [H5 Data Plotter](https://github.com/ayushchinmay/MiscPythonTools/blob/main/DataPlotters/h5DataPlotter.py) <.h5>
	- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/h5Plot_ex1.png" width="480">
	- Plots the binary file data (HDF5) saved from an oscilloscope.

4. [S2P Data Plotter](https://github.com/ayushchinmay/MiscPythonTools/blob/main/DataPlotters/s2pDataPlotter.py) <.s2p>
	- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/s2pPlot_ex1.png" width="480">
	- Plots the S-parameter data saved from [NanoVNA](https://nanovna.com/).

## 3. [PinholeFocus](https://github.com/ayushchinmay/MiscPythonTools/blob/main/PinholeFocus.py)
- Calculates the focal length of a pinhole camera with a specific pinhole diameter.
- Calculates the pinhole diameter for a specific focal length.
- For more information: [DIY Photography - Comprehensive Guide to Pinhole Photography](https://www.diyphotography.net/the-comprehensive-tech-guide-to-pinhole-photography/)

## 4. [Sieve of Eratosthenes](https://github.com/ayushchinmay/MiscPythonTools/blob/main/Sieve_of_Eratosthenes.py)
- Simple implementation of Sieve of Eratosthenes in Python
- Finds all prime numbers up to the given limit by  iteratively sieving out multiples of each prime number found within the range
- For more information: [Wikipedia: Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)

## 5. [Sin Square Wave](https://github.com/ayushchinmay/MiscPythonTools/blob/main/sinSquareWave.py)
- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/sineWaveSum.gif" width="480">
- Visualization of how summation of sine-waves can be used to create a square-wave

## 6. [Text to Speech Hourly Reminder](https://github.com/ayushchinmay/MiscPythonTools/blob/main/TTS/)
- Uses Google Text to Speech module to create audio files for each hour, which is then used to provide hourly reminders.

## 7. [Automatic Differentiation using Dual Numbers](https://github.com/ayushchinmay/MiscPythonTools/blob/main/DualNumbers.py)
- Implementation of a [Dual Number](https://en.wikipedia.org/wiki/Dual_number) class with supporting operations: ==, +, *, /, **, conjugate
- Dual Numbers are an extension of the real numbers, similar to complex numbers, but instead of using i (where i^2=-1), a new element is introduced
	- ε^2 = 0, ε != 0
 - Dual numbers are widely used in automatic differentiation (AD). Evaluating a function f(x) at a dual number x+ϵ naturally computes both the function value and its derivative.

## 8. [Power Sum Combinations Visualizer](https://github.com/ayushchinmay/MiscPythonTools/blob/main/PowerSumVisualizer.py)
- <img src="https://github.com/ayushchinmay/MiscPythonTools/blob/main/readme_img/powerSumVisualizer_ex1.png" width="600">
- PyQt6 application for visualizing unique combinations of power sums with interactive plotting.
- Computes all unique unordered pairs (a, b) such that a^power + b^power ≤ max_sum, for selectable powers (2, 3, 4, or 5).
- Plots the count of such combinations for each possible sum value up to the chosen threshold.
- Includes:
  - Interactive UI for selecting power and maximum sum limit.
  - Real-time progress updates.
  - Export functionality for plots (PNG) and data (CSV).
- Installation:
  - `pip install PyQt6 matplotlib numpy`
