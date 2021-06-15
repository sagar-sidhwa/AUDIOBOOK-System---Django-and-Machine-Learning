# AUDIOBOOK:speaker::books:-System---Django-and-Machine-Learning

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   


# Code Requirements

## Libraries Needed
- gTTS
- pygame
- PILLOW
- pytesseract
- os
- glob
- fitz
- PyPDF2
- FPDF

## What steps you have to follow?

 - Download my Repository
 - Open Visual Studio Code and Terminal
 - Cut the folder 'Tesseract-OCR' and paste it into your 'C:\Program Files' Folder 
 - run 'python manage.py runserver'

## Notes

There are about 45 million blind people and 135 million visually impaired people worldwide.
Disability of visual text reading has a huge impact on the quality of life for visually disabled
people. We are going to propose an approach to create an portable text to speech converter.This
system can help the visually impaired people or any person to learn from audio read-back of any
scanned text, by converting the uploaded pdf to image,extracting the text from image,and
converting the text to audio as mp3 file.

Our goal is to convert a given text image into a string of text, saving it to a file and to hear what
is written in the image through audio.

For this, we need to import some Libraries

1. Pytesseract(Python-tesseract) : It is an optical character recognition (OCR) tool for
python sponsored by google Open source OCR module Tesseract is used as a basis for
the implementation of a text reading system.

2. pyttsx3 : It is an offline cross-platform Text-to-Speech library.When the OCR process is
complete it produces a string of text which is displayed on the user interface screen

3. Python Imaging Library (PIL) :Pillow is built on top of PIL (Python Image Library). PIL is one
of the important modules for image processing in Python. It adds image processing
capabilities to your Python interpreter

4. Django : It is a python web framework that encourages rapid development and clean,
pragmatic design.

Optical Character Recognition involves the detection of text content on images and translation of
the images to encoded text that the computer can easily understand. An image containing text is
scanned and analyzed in order to identify the characters in it. Upon identification, the character is
converted to machine-encoded text.

The Uploaded Pdf is first converted to image and then the image is first scanned and the text and
graphics elements are converted into a bitmap, which is essentially a matrix of black and white
dots. The image is then pre-processed where the brightness and contrast are adjusted to enhance
the accuracy of the process.

The image is now split into zones identifying the areas of interest such as where the images or
text are and this helps kickoff the extraction process. The areas containing text can now be
broken down further into lines and words and characters and now the software is able to match
the characters through comparison and various detection algorithms. The final result is the text in
the image that we're given.
