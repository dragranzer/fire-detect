from keras.applications import xception
from keras.preprocessing import image
import cv2
import numpy as np
import os
import tensorflow as tf

#masking function
def create_mask_for_plant(image):
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_hsv = np.array([0,0,250])
    upper_hsv = np.array([250,255,255])
    
    mask = cv2.inRange(image_hsv, lower_hsv, upper_hsv)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    return mask

#image segmentation function
def segment_image(image):
    mask = create_mask_for_plant(image)
    output = cv2.bitwise_and(image, image, mask = mask)
    return output/255

#sharpen the image
def sharpen_image(image):
    image_blurred = cv2.GaussianBlur(image, (0, 0), 3)
    image_sharp = cv2.addWeighted(image, 1.5, image_blurred, -0.5, 0)
    return image_sharp

# function to get an image
def read_img(filepath, size):
    img = tf.keras.utils.load_img(filepath, target_size=size)
    #convert image to array
    img = image.img_to_array(img)
    return img

def read_and_process_image(img):
  #read image
  #img = read_img(data_folder, file,(INPUT_SIZE,INPUT_SIZE))
  #masking and segmentation
  image_segmented = segment_image(img)
  #sharpen
  image_sharpen = sharpen_image(image_segmented)
  print(image_sharpen.shape)
  x = xception.preprocess_input(np.expand_dims(image_sharpen.copy(), axis=0))

  xception_bf = tf.keras.models.load_model("/home/ivannizar/KC_app/models/15082022-model_xception.h5")
  feature = xception_bf.predict(x, batch_size=32, verbose=1)

  return feature