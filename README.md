# PyHider
PyHider is a steganography tool that I am currently building in Python. This tool is currently a work in progress that allows you to write hidden messages in files without anyone knowing that there is a hidden message in that file.

### Dependencies
PyHider requires that you have [Pillow](https://python-pillow.org/) and [Bitarray](https://pypi.org/project/bitarray/) installed on your machine. The Pillow library is required in order to read and manipulate image files, and the bitarray library is required in order to read and manipulate bits of data. The easiest way to install these libraries is to type in "pip install [library]" in terminal.

### Usage
It is fairly easy to use this program in any Python project. Simply import the py_hider module into your project, and call whichever function you need to use.
For example:
```
Python 3.6.6 (default, Sep 12 2018, 18:26:19) 
[GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import py_hider
>>> encoded_img = py_hider.encodePNG('This will be encoded.', 'lol.png') # To encode something in PNG file
>>> encoded_img.save('encoded.png') # Save the file with the encoded message
>>> py_hider.decodePNG('encoded.png') # Decode a PNG file with a message embedded into it
'This will be encoded.'
```

### Functions
Unfortunately, since this project is still a work in progress, I only have two usable functions. However, more will be added in the near future.
```
decodePNG(imgFile:str) -> str
    - Usage: Decodes a message from a given PNG image using steganography.
    - imgFile: A string representing the location of an PNG file that contains a hidden message.
    - Output: A string representing the hidden message
    
encodePNG(plaintext:str, imgFile:str, encoding='utf-8') -> <module 'PIL.Image' from '/usr/lib/python3/dist-packages/PIL/Image.py'>
    - Usage: Encodes a given message into the given PNG file using steganography.
    - plaintext: The input string that will be encoded into the image.
    - imgFile: A string representing the location of an PNG file that will serve as the base image for steganography.
    - encoding: How the characters will be encoded in binary (default is 'utf-8', but 'ascii' or another common character encoding may also be used).
    - Output: A new Pillow Image file with the message encoded into it.
```
### How PNG Image Steganography Works
This image steganography algorithm uses LSB image steganography, which exploits the fact that humans cannot see the difference if you change the RGB values of a pixel by a 1 (ex. if you change a pixel RGB values from [123, 11, 57] to [124, 12, 58], humans will not notice a difference). Using this technique, a programmer can therefore state that an even number in an RGB value could represent a 0 and an odd number in an RGB could represent a 1. By changing the RGB values accordingly (usually by adding one) so that their divisibility by two correspond to ones and zeros, someone could implement an ascii or utf-8 message into an image without anybody else realizing that there is a message encoded into the image. For a more in depth definition, please [click here](https://en.wikipedia.org/wiki/Bit_numbering#Least_significant_bit_in_digital_steganography).
