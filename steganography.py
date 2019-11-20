from PIL import Image
import sys
import random
import time

def twist(n):
	new = ""
	i = 0
	j = len(n)-1
	while i < j-i:
		new += n[i] + n[j-i]
		i +=1
	return new
	
def lsb(colour, binN, count_letter,N):
	result = colour
	result = result | N
	if bin(result)[2:].zfill(8)[7:] == "0": #lsb of the component is 0
		result = result | int(binN[count_letter])
	else:
		if int(binN[count_letter]) == 0: #the digit of the message is 0
			result = result & int(254)
		else:
			result = result & int(255)
	return result
	
def encode():
	f = open(str(sys.argv[2]),"r") # message to hide
	text = f.read()
	f.close()
	if len(text) == 0: # message without characters
		return 0
	image = Image.open(sys.argv[1]) # cover image
	pix = image.load()
	width, height = image.size #size of the image
	if (((len(text)*3)-1)*255)+255 > width*height:
		return -1
	# Value of every character of the hidden message in binary expressed in 8 bits + bits of control
	# Control bits are 0 if is not the last character, otherwise it is 1.
	binary = "" # string of hidden message in binary + control bits.
	for i in range(len(text)):
		binary = binary + bin(ord(text[i]))[2:].zfill(8)
		if i == len(text)-1:
			binary = binary + "1" # control bit set to 1 (last case)
		else:
			binary = binary + "0" # control bit set to 0
	if image.mode == "RGB": #image has RGB pixels
		rgba = 0
	else:
		rgba = 1 # image has RGBA pixels
	count_letter = 0 # number of the letter of the message
	span = 1
	for j in range(0,height):
		for i in range(0,width):
			if rgba == 1:
				RGBA = image.getpixel((i,j)) #current pixel
				R,G,B,A = RGBA
			else:
				RGB = image.getpixel((i,j)) #current pixel
				R,G,B = RGB
			if span == 1:
				if count_letter < len(binary):
					if j == 0 and i == 0:
						twister = bin(random.randint(0,7))[2:].zfill(3) + bin(random.randint(1,3))[2:].zfill(2) + bin(random.randint(0,7))[2:].zfill(3)
						twister = twist(twister)
						R = R | int(twister[3:][:3],2) #second fragment
						G = G | int(twister[6:],2) # third fragment
						B = B | int(twister[:3],2) # first fragment
					else:
						newR = random.randint(0,7)
						R = lsb(R,binary,count_letter,newR)
						count_letter = count_letter + 1

						newG = random.randint(2,3)
						G = lsb(G,binary,count_letter,newG)
						count_letter = count_letter + 1

						newB = random.randint(0,7)
						B = lsb(B,binary,count_letter,newB)
						count_letter = count_letter + 1
						
					if count_letter != len(binary): #not last character
						span = int(bin(B)[2:].zfill(8)[5:] + bin(R)[2:].zfill(8)[5:] + bin(G)[2:].zfill(8)[6:],2)
			else:
				span = span - 1
				R = R | random.randint(0,7)
				G = G | random.randint(0,7)
				B = B | random.randint(0,3)
			if rgba == 1:
				pix[i,j] = eval("(" + str(R) + ", " + str(G) + ", " + str(B) + ", " + str(A) + ")") 
			else:
				pix[i,j] = eval("(" + str(R) + ", " + str(G) + ", " + str(B) + ")")
				
	image.save(sys.argv[3]) #new image with the hidden message
	return 1

def split(input, size): #splits a string in n digits
	return [input[start:start+size] for start in range(0, len(input), size)]
def decode():
	image = Image.open(sys.argv[2]) # image to decode the hidden message
	width, height = image.size # size of the image
	pixel_count = 1 #every 3 pixels we check control bit
	string = "" #will be the result
	end = 0
	span = 1
	for j in range(0,height):
		if end == 1: #we finished (control bit = 1)
			break
		for i in range(0,width):
			if span == 1:
				if image.mode == "RGBA":
					RGBA = image.getpixel((i,j))
					R,G,B,A = RGBA
				else:
					RGB = image.getpixel((i,j))
					R,G,B = RGB
				if i==0 and j==0:
					span = int(bin(B)[2:].zfill(8)[5:] + bin(R)[2:].zfill(8)[5:] + bin(G)[2:].zfill(8)[6:],2)
				else:
					string = string + bin(R)[2:].zfill(8)[7:] #append the lsb of the component
					string = string + bin(G)[2:].zfill(8)[7:] #append the lsb of the component
					if pixel_count < 3: # B doesn't have a control bit
						string = string + bin(B)[2:].zfill(8)[7:]
						span = int(bin(B)[2:].zfill(8)[5:] + bin(R)[2:].zfill(8)[5:] + bin(G)[2:].zfill(8)[6:],2)
						pixel_count = pixel_count + 1
					else: # B has a control bit
						if str(bin(B)[2:].zfill(8)[7:]) == "1": # we finished the message
							end = 1
							break
						else: #we still have message to extract
							span = int(bin(B)[2:].zfill(8)[5:] + bin(R)[2:].zfill(8)[5:] + bin(G)[2:].zfill(8)[6:],2)
							pixel_count = 1
			else:
				span = span - 1
	listing = split(string, 8)
	print ''.join(str(chr(int(i,2))) for i in listing), # print the result with ASCII characters

if len(sys.argv) >= 2:
	if sys.argv[1] == "--h":
		if len(sys.argv) == 2:
			print "Usage: To encode a message: steganography.py [original image] [text file]"
			print "		Example: python steganography.py original-image.png message.txt"
			print "Usage: To decode the message: steganography.py --decode [modified image]"
			print "		Ejemplo: python steganography.py --decode modified.png"
		else:
			print "The input is not correct. Use the option --h to see the available options."
	elif sys.argv[1] != "--h" and sys.argv[1] != "--decode":
		if len(sys.argv) != 4:
			print "The input is not correct. Use the option --h to see the available options."
		else:
			start_time = time.time()
			res = encode()
			if res > 0:
				print "Congratulations, the image " + sys.argv[3] +  " was created with the hidden message."
			elif res < 0:
				print "Message too long. Try with a bigger image."
			else:
				print "The text file is empty."
			print "Execution Time: %s seconds." % (time.time() - start_time)
	elif sys.argv[1] == "--decode":
		if len(sys.argv) != 3:
			print "The input is not correct. Use the option --h to see the available options."
		else: 
			decode()
	else:
		print "The input is not correct. Use the option --h to see the available options."
else:
	print "The input is not correct. Use the option --h to see the available options."

