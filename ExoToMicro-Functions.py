#Imports the necessary python libraries
from PIL import Image, ImageOps, ImageChops
import numpy as np, matplotlib.pyplot as plt
import os, glob

#Gets the current working directory
cwd = os.getcwd()

#imports/opens the images 
def findfiles():
    """
    PURPOSE
    Goes through the current working directory within the Jupyter Notebook directory to find ch00/blue, ch01/red, 
    and ch02/green image files.

    REQUIRED INPUTS
    N/A
    

    OPTIONAL INPUTS
    N/A

    OUTPUTS
    list0 = list that contains the ch00/blue images
    list1 = list that contains the ch01/red images
    list2 = list that contains the ch02/green images

    
    written by Jess Labossiere October 2023
    """
    
    #Creates a new folder called Analyzed Images within the current working directory
    New_Folder = 'Analyzed Images'
    if not(os.path.exists(cwd + '/' + New_Folder)):
        os.mkdir(cwd + '/' + New_Folder)
    Images = glob.glob("*.tif")

    #Finds ch00/blue, ch01/red, and ch02/green images
    list0 = []
    list1 = []
    list2 = []
    
    for file in Images:
        print(file)
        if 'ch00' in file:
            list0.append(Image.open(file))     #opens ch00/blue images into list
        elif 'ch01' in file:
            list1.append(Image.open(file))     #opens ch01/red images into list
        elif 'ch02' in file:
            list2.append(Image.open(file))     #opens ch02/green images into list
        else:
            print('Please add the images that you want to be analyzed within the file location that this Jupyter Notebook resides.')
            break
    return(list0, list1, list2)



#imports/opens the images 
def imtolist(list0, list1, list2):
    """
    PURPOSE
    Takes each of the color images and opens these images into a list. Then, a numpy array is created out of the tif images. 
    Finally, an array is created of the size of the image arrays, that contains only zeros.

    REQUIRED INPUTS
    list0 = list that contains the ch00/blue images
    list1 = list that contains the ch001/red images
    list2 = list that contains the ch02/green images


    OPTIONAL INPUTS
    list0 = list that contains the ch00/blue images
    list1 = list that contains the ch001/red images
    list2 = list that contains the ch02/green images

    OUTPUTS
    im1 = list that contains the ch001/red images
    im2 = list that contains the ch002/green images
    im0 = list that contains the ch00/blue images
    array_orig1 = numpy array containing the the red tif images
    array_orig2 = numpy array containing the the green tif images
    array_orig0 = numpy array containing the the blue tif images
    array_sub1 = numpy array with the size of the red image array containing only zeros
    array_sub2 = numpy array with the size of the green image array containing only zeros
    array_sub0 = numpy array with the size of the blue image array containing only zeros

    written by Jess Labossiere October 2023
    """

    imlist = []
    imlist.append(list0)
    imlist.append(list1)
    imlist.append(list2)
    
    array_orig = []
    array_sub = []
    length = len(imlist)
    for i in range(length):
        array_orig.append(np.array(imlist[i]))              #makes an numpy array out of the tif images
        array_sub.append(np.zeros((length,length,3)))         #creates an array of the size of the image arrays, with only zeros



def mineralsub(list0, list1, list2):
    """
    PURPOSE
    Subtracts the red mineral image from the blue and green cell images. 

    REQUIRED INPUTS
    list0 = list that contains the ch00/blue images
    list1 = list that contains the ch001/red images
    list2 = list that contains the ch02/green images

    OPTIONAL INPUTS
    list0 = list that contains the ch00/blue images
    list1 = list that contains the ch001/red images
    list2 = list that contains the ch02/green images

    OUTPUTS
    sub00 = ch00/blue image with the ch00/red image subtracted 
    sub02 = ch02/green image with the ch00/red image subtracted
    
    written by Jess Labossiere October 2023
    """
    #finding red image
    for i in range(length):   
        if(array_orig[i][:,:,0].any() != 0):
            r_array = array_orig[i][:,:,0]

    #subtracting mineral image from cell images
    if 'r_array' in locals():
        for i in range(length): 
            if(array_orig[i][:,:,2].any() != 0):
                array_sub[i][:,:,2] = r_array               #fills the third column in the array with the red values
                sub00 = array_orig[i] - array_sub[i]        #subtracts the zero array from the blue image array
                sub00[sub00<0] = 0                          #any negative values get set to 0
            elif(array_orig[i][:,:,1].any() != 0):
                array_sub[i][:,:,1] = r_array
                sub02 = array_orig[i] - array_sub[i]
                sub02[sub02<0] = 0




def maskandsave(list0, list1, list2):
    """
    PURPOSE
    Masks the green image. Then, saves three images: the processed green image, the processed blue image, 
    and a combined processed green and blue image.

    REQUIRED INPUTS
    list1 = list that contains the red images
    list2 = list that contains the green images
    list3 = list that contains the blue images

    OPTIONAL INPUTS
    list1 = list that contains the red images
    list2 = list that contains the green images
    list3 = list that contains the blue images

    OUTPUTS
    comp = combined processed image
    pro00 = blue processed image
    pro02 = green processed image

    written by Jess Labossiere October 2023
    """
    #Masking the green image + saving images
    if 'sub02' and 'sub00' in locals():
        mask = np.zeros((512,512,3))
        mask[:,:,1] = sub00[:,:,2] 
        sub02[mask == 0] = 0
        combined = sub00 + sub02
        comp = Image.fromarray((combined).astype(np.uint8))        #returns the numpy array into tiff file format
        comp.save(path + '/' + New_Folder + '/' + List[0].split("_")[0] + 'comp.tif')
    if 'sub00' in locals():
        pro00 = Image.fromarray((sub00).astype(np.uint8))        #returns the numpy array into tiff file format
        pro00.save(path + '/' + New_Folder + '/' + List[0].split("_")[0] + 'pro00.tif')           #saves the image
    if 'sub02' in locals():
        pro02 = Image.fromarray((sub02).astype(np.uint8))
        pro02.save(path + '/' + New_Folder + '/' + List[0].split("_")[0] + 'pro02.tif')