# Steganography-PNG-random
LSB-replacement algorithm with pseudo-random allocation

# Dependencies

Dependencies can be insalled using the requirements.txt file

    pip install -r requirements.txt
    
# Usage
To encode a message: 

    python steganography.py [original image] [text file]

    Example: python steganography.py original-image.png message.txt
    
To decode the message: 

    python steganography.py --decode [modified image]

    Example: python steganography.py --decode modified.png
    
The pixels are modified with a pseudo-random allocation using a combination of 3 pseudo-random values of 3, 2, and 3 bits respectively. The distance (jump) between two modified pixels is calculated as follows and the LSB-replacement are as follow:

![alt text](https://github.com/brianma94/Steganography-PNG-random/blob/master/step1.png)
![alt text](https://github.com/brianma94/Steganography-PNG-random/blob/master/step2.png)
![alt text](https://github.com/brianma94/Steganography-PNG-random/blob/master/step3.png)


To avoid hiding the data always from the first pixel, the algorithm applies the following mechanism:
![alt text](https://github.com/brianma94/Steganography-PNG-random/blob/master/step4.png)

The necessary space needed to hide the data is:

N = Length of the message
J = Calculated jump value for eah modified pixel
- General case:

<img src="https://github.com/brianma94/Steganography-PNG-random/blob/master/formula_general.png" alt="alt text" width="300px" height="100px">

- Worst case (all the jumps have a distance of 255):

<img src="https://github.com/brianma94/Steganography-PNG-random/blob/master/formula_worstcase.png" alt="alt text" width="300px" height="100px">

To avoid the vulnerability of pathfinding with single colour images, all the pixels of the image will be modified with the same technique. The pixels without hidden data will be ignored in the decoding process.
