# Steganography-PNG-random
LSB-replacement algorithm with pseudo-random allocation

The pixels are modified with a pseudo-random allocation using a combination of 3 pseudo-random values of 3, 2, and 3 bits respectively. The distance (jump) between two modified pixels is calculated as follows and the LSB-replacement are as follow:


To avoid hiding the data always from the first pixel, the algorithm applies the following mechanism:

The necessary space needed to hide the data is:
- General case:
- Worst case (all the jumps have a distance of 255):

