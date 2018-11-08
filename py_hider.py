"""
PyHider Steganography Tool

This module is used to implement steganography tools into python. It requires the Pillow library (Python Imaging Library) in order to work on images and the bitarray library to work with bits.

Methods
-------
encodePNG(plaintext, imgFile, encoding='ascii'):
    Encodes a given message into the given PNG file using steganography. Returns a new PIL Image file with the message encoded into it.
decodePNG(imgFile):
    Decodes a message from a given PNG image using steganography. Takes an image file as an input. Returns the decoded string.
"""


import sys
import bitarray
from PIL import Image

def encodePNG(plaintext: str, imgFile: str, encoding='utf-8') -> Image:
    """Encodes a given message into the given PNG file using steganography. Returns a new PIL Image file with the message encoded into it.
    
    Parameters
    ----------
    plaintext: The input string that will be encoded into the image
    imgFile: A string representing the location of a PNG file that will be used to encode the message
    encoding: How the characters will be encoded in binary (default is 'utf-8', but 'ascii' or another common character encoding may also be used)
    """

    # Open the image
    img = Image.open(imgFile).convert('RGB')

    # Convert the plaintext into a bitarray
    message = bitarray.bitarray()
    message.frombytes(plaintext.encode(encoding))

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
                if(not message[counter]):
                    if(r % 2 != 0): r = r + 1
                elif(message[counter]):
                    if(r % 2 != 1): r = r + 1
                counter = counter + 1
            elif(counter >= len(message)): # If we have finished our message, put down zeros to indicate the end of message
                if(r % 2 != 0): r = r + 1
                counter = counter + 1

            # Continue writing our message in the green value if we have not yet finished
            if(counter < len(message)):
                if(not message[counter]):
                    if(g % 2 != 0): g = g + 1
                elif(message[counter]):
                    if(g % 2 != 1): g = g + 1
                counter = counter + 1
            elif(counter >= len(message)): # If we have finished our message, put down zeros to indicate the end of message
                if(g % 2 != 0): g = g + 1
                counter = counter + 1

            # Continue writing our message in the blue value if we have not yet finished
            if(counter < len(message)):
                if(not message[counter]):
                    if(b % 2 != 0): b = b + 1
                elif(message[counter]):
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
            bits.append(r % 2)
            bits.append(g % 2)
            bits.append(b % 2) 

            # Change the counter for the r value
            if(r % 2 == 0): counter = counter + 1
            else: counter = 0

            # Change the counter for the g value
            if(g % 2 == 0): counter = counter + 1
            else: counter = 0

            # Change the counter for the b value
            if(b % 2 == 0): counter = counter + 1
            else: counter = 0

            # Check if seven zeros have been found (our terminating value) and break the inner loop if it has
            if(counter >= 7): break
        # Check if seven zeros have been found (our terminating value) and break the outer loop if it has
        if(counter >= 7): break

    # Convert the message to string format and return it
    output = bitarray.bitarray(bits).tostring()
    return output[:len(output) - 1] # Slices the last character because the last character is always a null character (\x00)

# TODO: Make this work with GIF and JPEG as well
# TODO: Encode images inside other images
# TODO: Make this work with MP3 and MP4 files as well
# TODO: Add an option to use this with huffman encoding
# TODO: Add an option to use this with run length encoding
# TODO: Check to make sure that the message does not go over the image's space limit
# TODO: Add the option of using encryption
