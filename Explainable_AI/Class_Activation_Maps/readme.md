# **Class activation maps** #

<p align="justify">Class activation maps are used to localize the skin lesion of the most likely class for the input image predicted by the model. This method works with CNN architecture that uses Global Average Pooling (GAP) Layer.</p>  
  
To generate class activation maps, we perform the following two steps:  

1. <p align="justify">The softmax layer outputs probabilities for the seven classes. The argmax function over all the probabilities results in the most likely class for the image. The weights connected between the global average pooling layer and the softmax layer, i.e., the weights w<sub>1</sub>, w<sub>2</sub>,. . . , w<sub>n+1</sub> of that class are extracted. Next, the feature maps from the last convolution layer are extracted. Hence, for n feature maps before the global average pooling layer, we get n weights connecting between the GAP layer and the Softmax layer.</p>  
2. <p align="justify">Each feature map is multiplied with the corresponding weight, as shown in Figure below. The weight signifies the importance of the individual channel in the feature map. The final weighted sum is the heatmap of the class predicted. The size of the heatmap is the size of the feature map. The heatmap is first resized to the input image size, and then it is overlaid on top of the input to obtain results from CAM, as shown in Figure below.</p>
<div align="center">
<img src="https://github.com/rao208/Explainable_AI/blob/master/Images/CAM-1.svg" >
<p>Approach for Class Activation Maps</p>
</div>  
