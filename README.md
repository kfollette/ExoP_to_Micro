# README for the Exoplanets to Microbes project!

Follette Lab Project worked on by Jess Labossiere and Kinsey Cronin.

## Introduction
Exoplanets to Microbes is an inter-sectional project between the fields of Astronomy and Biology. The goal of this project is to create an algorithm that subtracts the mineral and organic matter signals, leaving just the microbial cells in the final image. Currently, we have created a working algorithm that subtracts these signals efficiently but we are continuing to update the code to provide a harsher subtraction.

## Installation
Please install Anaconda Navigator to your computer. Within Anaconda Navigator, please download and open Jupyter Notebook.  
How to install Anaconda Navigator:
- https://docs.anaconda.com/free/anaconda/

Once Anaconda Navigator is installed and running, run Jupyter Notebook which should open in whatever browser you use. Within the page that opens, click the upload button and select the "ExoToMicro-Tutorial.ipynb" file.  

Add any image files that you want to be analyzed into the directory in which your Jupyter Notebook files reside. The name of each of the images should end in "ch00", "ch01", or "ch02" in order for the code to recognize the images. Additionally, you should download "ExoToMicro-Functions.py" file and place this file in the same directory.  

How to add files to Jupyter Notebook Directory:
- Open File Explorer (Windows) or Finder (macOS)
- In the search bar, look up the name of the Jupyter Notebook file: "ExoToMicro.ipynb"
- Once in that directory, place all of the images you want to be analyzed within that directory and NOT within any extra folders.  


## Technologies
The Jupyter Notebook requires Python 3.8.8.

## What next?  
Right now the tiff to fits file function is not working correctly so we are unable to work with the images in DS9 (an astronomy software used frequently to work with images). 
Clean up and fix the background subtraction. 


