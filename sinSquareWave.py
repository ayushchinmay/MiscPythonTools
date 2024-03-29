import matplotlib.ticker as tck
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Signal Configuration
num_points = 100000
num_frames = 100
min_x = -np.pi/2
max_x = np.pi/2

# Time Configuration
t = np.linspace(min_x, max_x, num_points)   # Time vector
sine_sum = np.zeros(t.size)                 # Summation of sine waves

# Plot Configuration
colors = ['#cf4e53', '#5794a0','#ddab3b', '#75a338', "#7c4cc5"]

fig, ax = plt.subplots(facecolor='#f5f5f5')
fig.suptitle('Sine Wave Summation')
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_xlim((min_x, max_x))
ax.set_ylim(-1, 1)
ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
ax.xaxis.set_major_locator(tck.MultipleLocator(base=0.5))
ax.grid(True, linestyle='--', linewidth=0.75, color='#cbcbcb')
# Plot the signals
line_s = ax.plot(t, sine_sum, color=colors[2], label='Sine Wave')[0]
line = ax.plot(t, sine_sum, color=colors[0], label='Sum of Sines')[0]
ax.legend(loc='lower right')

def update(frame):
    global sine_sum
    if frame == 0:  # Clear the plot
        sine_sum = np.zeros(t.size)

    # Get new data
    ax.set_title(f'frequency = 2π·{2*frame+1}·t rad/sec')
    sine = np.sin(2 * np.pi * t * (2*frame + 1))/(2*frame+1)
    sine_sum += sine

    # Update the plot
    line_s.set_ydata(sine)
    line.set_ydata(sine_sum)

    return (line, line_s)
    
ani = animation.FuncAnimation(fig, update, frames=range(num_frames), interval=250, repeat=False)
plt.show()