"""
Created on Fri Aug  7 03:14:52 2020
@author: Vanditha Rao

Highly inspired from https://github.com/sicara/tf-explain

This script allows the user to implement occlusion sensitivity. Image file can
be of any format.

This script requires that tensorflow and OpenCV be installed within the python
environment you are running this script in.

Here, tensorflow version 2.2, cv2 version 4.2.0 and python version 3.7.7 is
used. This file is imported as a module and contains functions which implement
occlusion sensitivity

"""

import numpy as np
import cv2
import math

class OcclusionSensitivity:
    
    """
    Perform Occlusion Sensitivity for a given input
    
    """
    
    def __init__(self, batch_size = None):
        
        self.batch_size = batch_size
        
    def apply_grey_patch(self, img, h, w, patch_size,
                         occluding_pixel, occluding_stride):
       
        """
        Replace a part of the image with a grey patch.
        
        Args:
            
            img: numpy.ndarray
            Input image
            
            h: int
            Top Left X position of the applied box
            
            w: int
            Top Left Y position of the applied box
            
            patch_size: int
            Size of patch to apply
            
            occluding_pixel: float
            the pixel value of the patched area  
                
            occluding_stride: float
            the amount of movement of the grey patch over the image
            
        
        Returns:
            
            patched_image: numpy.ndarray
            image with grey patch
        """
        
        width, height, _ = img.shape
        
        h_start = h * occluding_stride
        w_start = w * occluding_stride
    
        h_end = min(height, h_start + patch_size)
        w_end = min(width, w_start + patch_size)
    
        # Getting the image copy, applying the occluding window and classifying it again:
        
        patched_image = np.copy(img)
        patched_image[h_start:h_end, w_start:w_end,:] =  occluding_pixel      
        
        return patched_image   
    
    
    def explain(self,
                original_img,
                aug_img,
                model,
                class_index,
                patch_size,
                occluding_stride,
                occluding_pixel,
                colormap='viridis',):
        
        """
        Compute sensitivity map on a given image for a specific class index.
        
        Args:
           
            model: tf.keras.Model
            the model to inspect
            
            img: numpy.ndarray
            Input image
            
            class_index: int
            Index of targeted class
            
            patch_size: int
            Size of patch to apply on the image
            
            occluding_pixel: float
            the pixel value of the patched area  
                
            occluding_stride: float
            the amount of movement of the grey patch over the image
        
        Returns:
            
            sensitivity_map: np.ndarray
            Sensitivity map with shape (H, W)
        """
    
        width, height, _ = aug_img.shape
        
        output_height = int(math.ceil((height-patch_size) / occluding_stride + 1))
        output_width = int(math.ceil((width-patch_size) / occluding_stride + 1))
        
        sensitivity_map = np.zeros((output_height, output_width))
        
        patches = [self.apply_grey_patch(aug_img, h, w, patch_size, occluding_pixel,
                                         occluding_stride)
                   for h in range(output_height)
                   for w in range(output_width)]
        
        coordinates = [(index_y, index_x)
               for index_x in range(sensitivity_map.shape[1])
               for index_y in range(sensitivity_map.shape[0])]
        
        out = model.predict(np.array(patches), self.batch_size)
        
        target_class_predictions = [prediction[class_index]
                                    for prediction in out]

        for (index_x, index_y), confidence in zip(coordinates, target_class_predictions):
            
            sensitivity_map[index_y, index_x] = confidence
            
        sensitivity_map = cv2.resize(sensitivity_map, (original_img.shape[1], original_img.shape[0]))
        
        return sensitivity_map
