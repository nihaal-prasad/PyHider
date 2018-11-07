# PyHider
PyHider is a steganography tool that I am currently building in Python. This tool is currently a work in progress that allows you to write hidden messages in files without anyone knowing that there is a hidden message in that file.

### Dependencies
PyHider requires that you have [Pillow](https://python-pillow.org/) installed on your machine. The easiest way to install Pillow is to type in "pip install pillow" in terminal. The Pillow library is required in order to read and manipulate image files.

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

    decodePNG(imgFile:str) -> str
        Decodes a message from a given PNG image using steganography. Takes an image file as an input.
        
        Parameters
        ----------
        imgFile: A string representing the location of a PNG file that contains an encoded message
    
    encodePNG(encode:str, imgFile:str) -> <module 'PIL.Image' from '/usr/lib/python3/dist-packages/PIL/Image.py'>
        Encodes a given message into the given PNG file using steganography. Returns a new PIL Image file with the message encoded into it.
        
        Parameters
        ----------
        encode: The input string that will be encoded into the image
        imgFile: A string representing the location of a PNG file that will be used to encode the message
