"""
PyHider Steganography Tool

This module is used to implement steganography tools into python. It requires the Pillow library (Python Imaging Library) in order to work on images.

Methods
-------
_strToBits(string: str)
    Converts a string into a list of ascii 1's and 0's.
_bitsToStr(bits: list)
    Converts a list of ascii 1's and 0's into a string.
encodePNG(encode: str, imgFile: str)
    Encodes a given message into the given PNG file using steganography. Returns a new PIL Image file with the message encoded into it.
decodePNG(imgFile: str)
    Decodes a message from a given PNG image using steganography. Takes an image file as an input.
"""


import sys
from PIL import Image

def _strToBits(string: str) -> list:
     """Converts a string into a list of ascii 1's and 0's.
     
     Parameters
     ----------
     string: The input string that will be converted to a list of bits.
     """

     result = [] # The output
     for byte in bytearray(string, 'ascii'): # Loop through each byte in the string
         # Check if the length of the byte is six, and add a zero at the beginning to make the length 7
         # This is done so that we can have every single byte have a length of 7 (important for the bitsToStr method)
         if(len(list(bin(byte)[2:])) == 6): result.append('0')

         # Loop through each bit in the byte
         for bit in list(bin(byte)[2:]):
             result.append(bit) # Append to the result
     return result # Return the result        

def _bitsToStr(bits: list) -> str:
    """Converts a list of ascii 1's and 0's into a string.
    
    Parameters
    ----------
    bits: The list of bits that will be converted into a string.
    """

    result = "" # The string result that will be returned
    for byteStart in range(0, len(bits), 7): # Loop through each byte (with a step of 7 because ascii value has 7 bits)
        value = "" # This will be 7 bits in string representation (required to be a string in order to convert to ascii)
        for x in bits[byteStart:byteStart+7]: # Loop through each bit in the byte
            value+=x # Add to the value
        result += chr(int(value, 2)) # Add to the result
    return result # Return the result

def encodePNG(encode: str, imgFile: str) -> Image:
    """Encodes a given message into the given PNG file using steganography. Returns a new PIL Image file with the message encoded into it.
    
    Parameters
    ----------
    encode: The input string that will be encoded into the image
    imgFile: A string representing the location of a PNG file that will be used to encode the message
    """

    # Open the image
    img = Image.open(imgFile).convert('RGB')

    # Convert the message into bits
    message = _strToBits(encode)

    # Get the width and height of the image in pixels
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

    # Return the new image
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_img_data)
    return new_img

def decodePNG(imgFile: str) -> str:
    """Decodes a message from a given PNG image using steganography. Takes an image file as an input.
    
    Parameters
    ----------
    imgFile: A string representing the location of a PNG file that contains an encoded message
    """

    # Open the image
    img = Image.open(imgFile).convert('RGB')

    # This counter is used to identify a NULL character (seven 0's), which will be used to represent the end of the string
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

    # Convert the message to ascii format and return it
    output = _bitsToStr(bits)
    return output[:len(output)-1] # The last value is sliced because the last value is \x00 (string terminator)

# TODO: Make this work with GIF and JPEG as well
# TODO: Make this work with MP3 and MP4 files as well
# TODO: Add an option to use this with huffman encoding
# TODO: Add an option to use this with unicode
# TODO: Check to make sure that the message does not go over the image's space limit
# TODO: Add the option of using encryption
