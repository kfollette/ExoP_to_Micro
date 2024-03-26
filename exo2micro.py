#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image, ImageOps, ImageChops
import numpy as np, matplotlib.pyplot as plt
import os, glob
from scipy.optimize import minimize 
from scipy import ndimage


# In[ ]:


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
    #Gets the current working directory
    cwd = os.getcwd()
    New_Folder = 'Analyzed_Images'
    if not os.path.exists(os.path.join(cwd, New_Folder)):
        os.mkdir(os.path.join(cwd, New_Folder))
    Images = glob.glob("*.tif")

    list0 = []
    list1 = []
    list2 = []

    for file in Images:
        if 'ch00' in file:
            list0.append(file)
        elif 'ch02' in file:
            list1.append(file)
        elif 'ch01' in file:
            list2.append(file)

    return list0, list1, list2


# In[ ]:


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
    im0 = [Image.open(file) for file in list0]
    im1 = [Image.open(file) for file in list1]
    im2 = [Image.open(file) for file in list2]

    array_orig0 = [np.array(im) for im in im0]
    array_orig1 = [np.array(im) for im in im1]
    array_orig2 = [np.array(im) for im in im2]

    array_sub0 = [np.zeros_like(arr) for arr in array_orig0]
    array_sub1 = [np.zeros_like(arr) for arr in array_orig1]
    array_sub2 = [np.zeros_like(arr) for arr in array_orig2]
    
    return im0, im1, im2, array_orig0, array_orig1, array_orig2, array_sub0, array_sub1, array_sub2


# In[ ]:


def filter_nan_gaussian_conserving(arr, sigma):
    """Apply a gaussian filter to an array with nans.

    Intensity is only shifted between not-nan pixels and is hence conserved.
    The intensity redistribution with respect to each single point
    is done by the weights of available pixels according
    to a gaussian distribution.
    All nans in arr, stay nans in gauss.
    """
    
    nan_msk = np.isnan(arr)
    loss = np.zeros(arr.shape)
    loss[nan_msk] = 1
    loss = ndimage.gaussian_filter(
            loss, sigma=sigma, mode='constant', cval=1)

    gauss = arr.astype(float)  # Convert to float type
    gauss[nan_msk] = 0
    gauss = ndimage.gaussian_filter(
            gauss, sigma=sigma, mode='constant', cval=0)
    gauss[nan_msk] = np.nan

    gauss += loss * arr

    return gauss


# In[5]:


def mask_and_optimize(blue, red, green):
    """
    Apply masking and optimization to subtract the scaled red channel from the green channel.

    This function applies a mask to the red channel and optimizes a scaling factor 'B' such that 
    when the scaled red channel is subtracted from the green channel, the residuals are minimized.

    Parameters:
    - blue (numpy.ndarray): Blue channel image array.
    - red (numpy.ndarray): Red channel image array.
    - green (numpy.ndarray): Green channel image array.

    Returns:
    - numpy.ndarray: Image array resulting from subtracting the scaled red channel from the green channel.
    """
    blue = np.array(blue)
    red = np.array(red)
    green = np.array(green)
    
    # Convert NaN values to 0
    blue = np.nan_to_num(blue)
    red = np.nan_to_num(red)
    green = np.nan_to_num(green)
    mask= mask_em(blue,red,green)
    
    # Initial guess for the parameter B
    initial_guess = [2.0]
    # Bounds for B
    bounds = ((0, None),)
    thresh = 50
    # Optimize the parameters
    result = minimize(residuals_squared, initial_guess, args=(blue, red, green,mask, thresh), bounds=bounds)
    B_opt = result.x[0]
    masked_red = red[:,:,0] * mask
    masked_green= green[:,:,1] * mask
    sub_green = green - B_opt*masked_red
    
    return masked_red, masked_green, sub_green 


# In[2]:


def mask_em(blue, red, green):
    """
    Create a mask based on the red channel of an image.

    This function generates a binary mask where pixels are set to 1 if the corresponding pixel
    in the red channel is non-zero and 0 otherwise. NaN values are assigned to pixels where the 
    red channel is zero.

    Parameters:
    - blue (numpy.ndarray): Blue channel image array.
    - red (numpy.ndarray): Red channel image array.
    - green (numpy.ndarray): Green channel image array.

    Returns:
    - numpy.ndarray: Binary mask array with the same shape as the input images."""
    # Creates a mask
    mask = np.zeros_like(red,dtype=np.float)
    for i in range(mask.shape[0]):
        for j in range (mask.shape[0]):
            if mask[0][i, j, 1] != 0:
                mask[0][i, j, :] = 1
            else: 
                mask[0][i, j, :] = np.nan
    return mask


# In[3]:


def residuals_squared(params, blue, red, green,mask, thresh):
    """
    Calculate the mean of squared residuals after applying a given mask and threshold.

    Parameters:
    - params (list): List of parameters. Expected to contain a single value representing the scaling factor 'B'.
    - blue (numpy.ndarray): Blue channel image array.
    - red (numpy.ndarray): Red channel image array.
    - green (numpy.ndarray): Green channel image array.
    - mask (numpy.ndarray): Binary mask array with the same shape as the input images.
    - thresh (float): Threshold value for residual squared to zero out high residuals.

    Returns:
    - float: Mean of squared residuals after thresholding.
    """
    B = params[0]
    resids = []
   
    masked_red = red * mask
    
    # Mask green image
    masked_green = green * mask
    
    # Apply mask and calculate residuals squared
    imresid = masked_green - B * masked_red
    resids = np.square(imresid)
    
    # Apply thresholding
    resids[resids > thresh] = 0
    
    # Calculate mean of squared residuals
    mean_resids = np.mean(resids)
    
    return mean_resids


# In[4]:


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
    path = os.getcwd()
    New_Folder = "Analyzed_Images"
    
    if sub02 is not None and sub00 is not None:
        mask = np.zeros((512, 512, 3))
        mask[:, :, 1] = sub00[:, :, 2] 
        sub02[mask == 0] = 0
        combined = sub00 + sub02
        comp = Image.fromarray((combined).astype(np.uint8))
        comp.save(os.path.join(path, New_Folder, f"{list0[0].split('_')[0]}comp.tif"))
    
    if sub00 is not None:
        pro00 = Image.fromarray((sub00).astype(np.uint8))
        pro00.save(os.path.join(path, New_Folder, f"{list0[0].split('_')[0]}pro00.tif"))
    
    if sub02 is not None:
        pro02 = Image.fromarray((sub02).astype(np.uint8))
        pro02.save(os.path.join(path, New_Folder, f"{list0[0].split('_')[0]}pro02.tif"))


# In[ ]:





# In[ ]:




