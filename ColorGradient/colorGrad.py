"""
DESCRIPTION :   Python script to create a color gradient between two given colors

AUTHOR      :   Ayush Chinmay
CREATED     :   29 Nov 2023
MODIFIED    :   02 Nov 2023

? CHANGELOG ?
    * [29 Nov 2023]
        - [x] initial commit
    * [02 Dec 2023]
        - [X] Calculate gradient between two colors
        - [X] Use 5 colors to create a gradient
        - [X] Create a color-map and display it

! TODO !
        - [ ] Apply the color-map to a monochrome image
        - [ ] Save the colorified-image
        - [ ] Create an interactive GUI for the script
"""

##========[ MODULES ]========##
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import plotly.express as px

class RGB:
	"""
	Represents an 8-bit color in the RGB color-space
	"""
	# Class variables
	def __init__(self, r=255, g=255, b=255):
		self.r = r
		self.g = g
		self.b = b
		self.hx = f"#{self.r:02x}{self.g:02x}{self.b:02x}"

	# Class methods
	def __str__(self):			# String representation of the object
			return f"({self.r}, {self.g}, {self.b})"
		
	def __repr__(self):
		return f"RGB({self.r}, {self.g}, {self.b})"
	
	def __add__(self, other):	# Addition of two RGB objects
			return RGB(min(255,self.r + other.r), min(255,self.g + other.g), min(255,self.b + other.b))

	def __sub__(self, other):	# Subtraction of two RGB objects
			return RGB(abs(self.r - other.r), abs(self.g - other.g), abs(self.b - other.b))
	
	def __mul__(self, other):	# Multiplication of two RGB objects
		return RGB(min(255, self.r * other), min(255, self.g * other), min(255, self.b * other))
	
	def __floordiv__(self, num): # Division of two RGB objects
		if num == 0:
			return RGB(0, 0, 0)
		return RGB(self.r // num, self.g // num, self.b // num)

	def __eq__(self, other):	 # Equality of two RGB objects
		return self.r == other.r and self.g == other.g and self.b == other.b
	
	def invert(self):			# Inverts the color
		return RGB(255 - self.r, 255 - self.g, 255 - self.b)
	
	def mix(self, other):		 # Mixes two RGB objects
		return RGB((self.r + other.r)//2, (self.g + other.g)//2, (self.b + other.b)//2)
	
	def setHex(self, hx):	 	 # Sets the color from a hex value
		self.r, self.g, self.b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
		self.hx = hx.lower()
		return self

	def toHex(self):		 	# Returns the hex value of the color
		return self.hx

	def toRGB(self):			# Returns the RGB value of the color
		return (self.r, self.g, self.b)
		

##========[ FUNCTIONS ]========##
def interpolate_color(color1, color2, steps):
	"""
	Interpolates between two colors and returns a list of colors
	"""
	# Create a list of colors
	colorList = []
	
	# Calculate the difference between the two colors
	for i in range(1,steps+1):
		r = int(color1.r + i/(steps) * (color2.r - color1.r))
		g = int(color1.g + i/(steps) * (color2.g - color1.g))
		b = int(color1.b + i/(steps) * (color2.b - color1.b))
		# print(f"{r}, {g}, {b}")
		colorList.append(RGB(r, g, b))

	print(f"Colors ({len(colorList)}) >> [", end="")
	print(*[clr.toHex() for clr in colorList], sep=', ', end=']')
	print("")
	return colorList


def generate_gradient(colors, show=False, img=False):
	"""
	Creates a color map from a list of colors
	"""
	# Create the array for the color-map
	if img:	# If the color-map is to be used as an image
		grad_arr = np.zeros(shape=(128, 512, 3), dtype=np.uint8)
		stepSize = 512//len(colors)
		# Fill the array with the colors
		for i in range(len(colors)):
			grad_arr[:, i*stepSize:(i+1)*stepSize] = colors[i].toRGB()
		print(grad_arr)
		
		# Create an image from the array and display it
		grad_img = Image.fromarray(grad_arr)
		if show:
			fig = px.imshow(grad_img, title="COLOR GRADIENT [IMG]")
			fig.show()
		return grad_img

	else:	# If the color-map is to be used as a list
		grad_arr = np.zeros(shape=(1, len(colors), 3), dtype=np.uint8)
		# Fill the array with the colors
		for i in range(len(colors)):
			grad_arr[:, i] = colors[i].toRGB()
		
		# Plot the color-map as a list
		if show:
			fig = px.imshow(grad_arr, title="COLOR GRADIENT [LST]")
			fig.update_layout(title="COLOR GRADIENT", title_x=0.5, title_font={"size":25})
			# fig.update_layout(title_subtitle=f"{colors[0].toHex()} -> {colors[-1].toHex()}")
			fig.update_xaxes(title_text=f"{colors[0].toHex()} -> {colors[-1].toHex()}", title_font={"size":14}, nticks=2*len(colors))
			fig.update_yaxes(showticklabels=False)
			
			for i in range(len(colors)):
				inv_color = "#ffffff" if colors[i].r + colors[i].g + colors[i].b < 384 else "#000000"
				fig.add_annotation(x=i, y=0, text=f"{colors[i].toHex()}", font=dict(color=inv_color, family="Courier New, monospace", size=16), showarrow=False, yshift=-20)
				fig.add_annotation(x=i, y=0, text=f"{colors[i]}", font=dict(color=inv_color, family="Courier New, monospace", size=12), showarrow=False, yshift=-40)

			fig.show()
		return grad_arr



def load_image(fn, show=False):
    """
    Loads the image and returns it as a numpy array
    """
    # Load the image and convert it to a numpy array
    img = Image.open(fn)
    img_arr = np.asarray(img)
    print(f"Image Dimensions: {img_arr.shape}")

    if show:
        # Display the image
        plt.figure(figsize=(6,4))
        plt.imshow(img)
        plt.show()
    return img_arr


def split_channels(img_arr):
	"""
	Splits the image into its RGB channels
	"""
	# Create a list of the channels
	channels = []
	for i in range(3):
		channels.append(img_arr[:,:,i])

	# Display the channels
	fig, axs = plt.subplots(1, 3, figsize=(12,4))
	for i in range(3):
		axs[i].imshow(channels[i])
		axs[i].set_title(f"Channel {i+1}")
	plt.show()


def colorify_image(img, colorMap):
	"""
	Applies the color-map to the image
	"""
	# Create a new image array
	colorified_img = np.zeros(shape=img.shape, dtype=np.uint8)

	# Apply the color-map to the image
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			colorified_img[i][j] = colorMap[img[i][j]]
	
	# Create an image from the array and display it
	colorified_img = Image.fromarray(colorified_img)
	fig = px.imshow(colorified_img)
	fig.show()
	return colorified_img


def main():
	# split_channels(load_image("bird.png"))
	cnt_flg = 'y'
	print("  -------------------------------  ")
	print("[]----[ GRADIENT GENERATOR ]-----[]")
	print("  -------------------------------  ")
	while (cnt_flg != 'n'):
		col1 = input("\t[INPUT] Color 1 <#hex>: ")
		col2 = input("\t[INPUT] Color 2 <#hex>: ")
		steps = int(input("\t[INPUT] No. of Steps <int>: ")) 

		col1 = f"#{col1}" if not col1.startswith("#") else col1
		col2 = f"#{col2}" if not col2.startswith("#") else col2

		color1 = RGB().setHex(col1)
		color2 = RGB().setHex(col2)
		generate_gradient(interpolate_color(color1, color2, steps), show=True)
		cnt_flg = input("\nContinue? (y/n)... ").lower()


if __name__ == '__main__':
	main()