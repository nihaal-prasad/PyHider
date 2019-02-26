"""
PyHider Steganography Tool

This module is used to implement steganography tools into python. It requires the Pillow library (Python Imaging Library) in order to work on images and the bitarray library to work with bits.

Methods
-------
encodePNG(plaintext, imgFile, encoding='utf-8'):
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

    # This counter will be used to keep track of how many bits have been written
    counter = 0

    # RGB data for the new image
    new_img_data = []

    # Here is how this algorithm works:
    # 1.) We convert our message into bits of 1's and 0's
    # 2.) First we obtain the first pixel in the image
    # 3.) Then we get the RGB values of that pixel
    # 4.) We encode the bits of our message based on whether the individual RGB values are even or odd (even represents a 0 and odd represents a 1).
    #     This way, when we decode the message, we can look at the individual RGB values and figure out whether each bit of the message is a 1 or 0.
    # 5.) If the next bit in our message is a 0, but our current RGB value is odd, then we add one to the RGB value to make it even.
    #     We do the same thing if the current RGB value is even, but the next bit in our message is a 1
    # 6.) Then we move onto the next bit in the message and the next RGB value in the image

    # Loop through each pixel
    for y in range(0, height):
        for x in range(0, width):
            # Get the red, green, and blue values for the pixel
            rgb = img.getpixel((x, y))

            # This list will contain the edited rgb values
            new_rgb = []
            
            # Loop through each of the RGB values
            for value in rgb:
                # This will be the value that will be appended to the new_rgb list
                new_value = value

                # Check if we still have to write another bit to the image
                if(counter < len(message)):
                    # If the next bit in the message does not correspond with the bit represented by the pixel, then change the pixel
                    if(message[counter] != value % 2):
                        # Adding one will change even numbers to odd numbers and odd numbers to even numbers
                        new_value = new_value + 1
                        
                        # If the RGB value is 255, and we're supposed to add one, then just subtract one instead
                        # This is done because RGB values cannot be greater than 255, so we subtract one instead of adding one
                        # Both values end up being even, so it doesn't really matter whether we add or subtract one
                        if(value == 255): new_value = 254
                    
                    # Increment the counter
                    counter = counter + 1

                # Else, make the rest of the RGB values even numbers so that they all represent zeros
                # Zeros are used to represent the NULL terminator, which is important because the decoder needs to know where to stop
                else:
                    # If the next bit is not even, then change the pixel
                    if(value % 2 != 0):
                        # Adding one will change this to be an even number
                        new_value = new_value + 1

                        # If the RGB value is 255, and we're supposed to add one, then just subtract one instead
                        # This is done because RGB values cannot be greater than 255, so we subtract one instead of adding one
                        # Both values end up being even, so it doesn't really matter whether we add or subtract one
                        if(value == 255): new_value = 254

                # Append the new RGB value to the new_rgb list
                new_rgb.append(new_value)

            # Write down the RGB values in the new image
            # Values are converted into a tuple because putdata() only works with tuples
            new_img_data.append(tuple(new_rgb))

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

    # This counter is used to identify a NULL character (eight 0's), which will be used to represent the end of the string
    counter = 0

    # These are the bits that make up the message
    bits = []

    # Get the width and height in pixels
    width, height = img.size

    # Here is how this algorithm works:
    # 1.) We obtain the first pixel in the image
    # 2.) Then we unpack the RGB values and loop through each value
    # 3.) Then we check whether the value is even or odd. If it is even, append zero to the bits list. If it is odd, append one to the bits list
    # 4.) Break out of the loops if we find eight zeros in a row because eight zeros in a row is our terminating value
    # 5.) Afterwards, convert the bits list into a string, and return that string

    # Read each pixel
    for y in range(0, height):
        for x in range(0, width):
            # Get the red, green, and blue values for the pixel
            rgb = img.getpixel((x, y))

            # Loop through each of the RGB values
            for value in rgb:
                # Get the binary value, which is based on whether this particular RGB value is even or odd
                binary = value % 2

                # Add the appropriate binary value to the bits list
                bits.append(binary)

                # If there is a zero, add to the counter variable so that it can identify a NULL value (seven 0's in a row)
                # If there is something other than a zero, than this clearly isn't a NULL value, so reset the counter
                if(binary == 0): counter = counter + 1
                else: counter = 0

                # Check if eight zeros have been found (our terminating value) and break the inner loop if there are seven zeros
                if(counter >= 8): break
            # Check if eight zeros have been found (our terminating value) and break the middle loop if there are seven zeros
            if(counter >= 8): break
        # Check if eight zeros have been found (our terminating value) and break the outer loop if there are seven zeros
        if(counter >= 8): break

    # Convert the message to string format and return it
    output = bitarray.bitarray(bits).tostring()
    return output[:len(output) - 1] # Slices the last character because the last character is always a null character (\x00)
