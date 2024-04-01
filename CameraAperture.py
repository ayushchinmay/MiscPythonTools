import matplotlib.pyplot as plt

def calculate_data(focalLength):
	apertureStops = [1.2, 1.4, 1.8, 2.0, 2.2, 2.8, 3.2, 3.5, 4.5, 5.0, 5.6]
	Dia25mm = [round((25/i),2) for i in apertureStops]
	Dia35mm = [round((35/i),2) for i in apertureStops]
	Dia50mm = [round((50/i),2) for i in apertureStops]
	fig, axs = plt.subplots(3)
	axs[0].plot(apertureStops, Dia25mm)
	axs[1].plot(apertureStops, Dia35mm)
	axs[2].plot(apertureStops, Dia50mm)
	for i in range(len(apertureStops)):
		axs[0].annotate(str((apertureStops[i], Dia25mm[i])), (apertureStops[i], Dia25mm[i]))
		axs[1].annotate(str((apertureStops[i], Dia35mm[i])), (apertureStops[i], Dia35mm[i]))
		axs[2].annotate(str((apertureStops[i], Dia50mm[i])), (apertureStops[i], Dia50mm[i]))
	plt.show()


def menu():
	cropFactors = {'Canon':1.6, 'Fuji':1.5, 'Nikon':1.5, 'Olympus':2.0}
	cropFactors = [1.6, 1.5, 1.5, 2.0, 1] # Canon, Fuji, Nikon, Olympus, Full Frame

	print(" >> CAMERA APERTURE CALCULATOR << ")
	ch = 'y'
	while ch!='n':
		try:
			focalLength = int(input("\nEnter Focal Length [mm]: "))
			aperture = float(input("Enter the largest Aperture: "))

			cropSensor = int(input("What Camera?:\n\t[1] Canon\n\t[2] Fuji\n\t[3] Nikon\n\t[4] Olympus\n\t[0] N/A\n\t[9] Full Frame\nEnter your Choice: "))
			if (cropSensor == 0):
				cropFocalLength = 36/focalLength
			else:
				cropFocalLength = focalLength*cropFactors[cropSensor]

			apertureDia = cropFocalLength/aperture
			print(f">> Aperture Diameter at f/{aperture} for f={focalLength}mm = {apertureDia}mm")
			ch = input("\nCalculate More? (y/n)...").lower()
		except TypeError:
			print("\n>> Invalid Input. Please Try Again.\n")
			continue


def main():
	calculate_data(35)


if __name__ == '__main__':
	main()