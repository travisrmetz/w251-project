import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale

image_dir='/w251-project/stars/images'

def load_image(image_path, dim=(224,224)):
  """
  Loads a single image as a Numpy array and resizes it as
  desired.  The default dimensions are consistent with
  those expected by the VGG models.  

  Args:
    image_path: str pointing to the file

    dim: Two-element tuple giving the desired height
         and width of the processed image

  Returns:
    image:  A single-channel Numpy array
    """
  image = cv2.imread(image_path, 0)
  image = cv2.resize(image, dim)#, interpolation = cv2.INTER_AREA)
  return image

def build_input(image_dir):
  """
  Loads all of the images into a single numpy array.
  Assumes that there are 101 equally-spaced images
  spanning lattitudes from 35N to 45N.  

  Args:
    image_dir: str giving name of the image directory

  Returns:
    X:  A 3-dimensional numpy array containing the
        images. Image height and width are set by
        `load_images` and default to 224 x 224.
    
    y:  A 1-dimensional numpy array of target lattitudes.
    """
  X = []
  print('about to do listdir') 
  files = os.listdir(image_dir)
  print('finished listdir')
  print(files)
  for file in files:
    if file[-4:] == '.png':
      image_path = os.path.join(image_dir, file)
      image = load_image(image_path)
      X.append(image)
  return (np.array(X) / 255)

def build_labels(image_dir):
  files = os.listdir(image_dir)
  y = []
  for file in files:
    if file[-4:] == '.png':
      file_split = file.split('+')
      lat = float(file_split[0])
      long = float(file_split[1])
      y.append((lat, long))
  return np.array(y)

file_name='43.20383241355868+-68.24170969718236+2020-05-25T00:59:02.png'
sample_file=os.path.join(image_dir,file_name)
print (sample_file)
sample_image = load_image(sample_file)
plt.imshow(sample_image)
print(sample_image.shape)