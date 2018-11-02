# Embed string: python stegotool.py <image file> "<message in quotes>"
# Decode string: python stegotool.py <image file>

# TODO: Make this work with other image formats as well
# TODO: Add an option to use this with huffman encoding
# TODO: Check to make sure that the message does not go over the image's space limit
# TODO: Add an option to change the exported file's name

import sys
from PIL import Image

# Converts the string into bits
def strToBits(string):
     result = [] # The output
     for byte in bytearray(string, 'ascii'): # Loop through each byte in the string
         # Check if the length of the byte is six, and add a zero at the beginning to make the length 7
         # This is done so that we can have every single byte have a length of 7 (important for the bitsToStr method)
         if(len(list(bin(byte)[2:])) == 6): result.append('0')

         # Loop through each bit in the byte
         for bit in list(bin(byte)[2:]):
             result.append(bit) # Append to the result
     return result # Return the result        

def bitsToStr(bits):
    result = "" # The string result that will be returned
    for byteStart in range(0, len(bits), 7): # Loop through each byte (with a step of 7 because ascii value has 7 bits)
        value = "" # This will be 7 bits in string representation (required to be a string in order to convert to ascii)
        for x in bits[byteStart:byteStart+7]: # Loop through each bit in the byte
            value+=x # Add to the value
        result += chr(int(value, 2)) # Add to the result
    return result # Return the result

# Encode the string into the image
def encode():
    print('Encoding message...')

    # Open the image
    img = Image.open(sys.argv[1]).convert('RGB')

    # Get the message
    message = strToBits(sys.argv[2])

    # Get the width and height in pixels
    width, height = img.size

    # Counter for the message
    counter = 0

    # RGB data for the new image
    new_img_data = []

    # Loop through each pixel
    for y in range(0, height):
        for x in range(0, width):
            # Get the red, green, and blue values for the pixel
            r, g, b = img.getpixel((x, y))

            # Continue writing our message in the red value if we have not yet finished
            if(counter < len(message)):
                if(message[counter] == '0'):
                    if(r % 2 != 0): r = r + 1
                elif(message[counter] == '1'):
                    if(r % 2 != 1): r = r + 1
                counter = counter + 1
            elif(counter >= len(message)): # If we have finished our message, put down zeros to indicate the end of message
                if(r % 2 != 0): r = r + 1
                counter = counter + 1

            # Continue writing our message in the green value if we have not yet finished
            if(counter < len(message)):
                if(message[counter] == '0'):
                    if(g % 2 != 0): g = g + 1
                elif(message[counter] == '1'):
                    if(g % 2 != 1): g = g + 1
                counter = counter + 1
            elif(counter >= len(message)): # If we have finished our message, put down zeros to indicate the end of message
                if(g % 2 != 0): g = g + 1
                counter = counter + 1

            # Continue writing our message in the blue value if we have not yet finished
            if(counter < len(message)):
                if(message[counter] == '0'):
                    if(b % 2 != 0): b = b + 1
                elif(message[counter] == '1'):
                    if(b % 2 != 1): b = b + 1
                counter = counter + 1
            elif(counter >= len(message)): # If we have finished our message, put down zeros to indicate the end of message
                if(b % 2 != 0): b = b + 1
                counter = counter + 1

            # Write down the RGB values in the new image
            new_img_data.append((r, g, b))

    # Save the new image
    print('Saving new image as steg.png')
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_img_data)
    new_img.save('steg.png')

# Decode the string from the image
def decode():
    # Open the image
    img = Image.open(sys.argv[1]).convert('RGB')

    # This counter is used to figure out if the string has ended or not
    # Every time a 1 appears, the counter will be incremented (7 consecutive ones means an end of string has occurred)
    # Every time a 0 appears, the counter will be reset
    counter = 0

    # These are the bits that make up the message
    bits = []

    # Get the width and height in pixels
    width, height = img.size

    # Read each pixel
    for y in range(0, height):
        for x in range(0, width):
            # Get the red, green, and blue values for the pixel
            r, g, b = img.getpixel((x, y))

            # Add r to the bits list
            bits.append(str(r % 2))
            bits.append(str(g % 2))
            bits.append(str(b % 2))

            # Change the counter for the r value
            if(r % 2 == 0): counter = counter + 1
            else: counter = 0

            # Change the counter for the g value
            if(g % 2 == 0): counter = counter + 1
            else: counter = 0

            # Change the counter for the b value
            if(b % 2 == 0): counter = counter + 1
            else: counter = 0

            # Check if seven zeros have been found (our terminating value) and break if it has
            if(counter >= 7): break
        # Check if seven zeros have been found (our terminating value) and break if it has
        if(counter >= 7): break

    # Print out the message in ascii format
    print('Decoded message:')
    print(bitsToStr(bits))

# Check how many arguments there are
if(len(sys.argv) == 3): # If there are three arguments, we are encoding a string
    encode()
elif(len(sys.argv) == 2): # If there are two arguments, we are decoding a string
    decode()
