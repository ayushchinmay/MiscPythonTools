import math

def focalLen():
	dPin = float(input("Enter Pinhole Diameter (in mm): "))
	fLen = (dPin/0.03679)**2
	fStop = int(fLen/dPin)

	print(f"\tFocal Length = {fLen:.1f} mm")
	print(f"\tf-Stop = {fStop}")
	return fLen


def dPinhole():
	fLen = float(input("Enter Focal Length (in mm): "))
	dPin = math.sqrt(fLen) * 0.03679
	fStop = int(fLen/dPin)

	print(f"\tPinhole Diameter = {dPin:.2f} mm")
	print(f"\tf-Stop = {fStop}")
	return dPin


def main():
	dPinhole()
	focalLen()


if __name__ == '__main__':
	main()