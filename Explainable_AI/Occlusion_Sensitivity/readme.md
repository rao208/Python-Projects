# **Occlusion sensitivity** #
<p align="justify">Occlusion sensitivity on skin lesion helps us to gain a high-level understanding of what image features a model uses, to make a particular classification. It also helps in providing sanity checks on the learning strategy and provides reasons why a model can misclassify an image. In the medical field, checking the reliability of the model is very important. Therefore, performing a sanity check is very crucial. The approach is to implement occlusion sensitivity on the given image is as follows:</p>

1. <p align="justify">A small area of the input image is perturbed by replacing it with a patch (typically a grey square). The patch slides over the entire image, as shown in Figure below</p>
2. <p align="justify">This patched image is given to the model for prediction, and the probability of the target class is saved.</p>
3. <p align="justify">The change in the probability for the target class is measured as a function of the patch position.</p>
4. <p align="justify">When the patch goes over the feature that is important for the correct classification of the image, the probability of the target class falls sharply because we are hiding the elements that degrade the performance. This region behind the patch is identified as a significant region. When the patch does not occlude the significant feature, the probability for the target class stays even or goes up.</p>
5. <p align="justify">The array of the probability of all the patched images for the target class is the heatmap, which is then superimposed on the input image. The size of the heatmap depends on the patch size and the amount of movement of the patch over the image.</p>  
<div align="center">
<img src="https://github.com/rao208/Explainable_AI/blob/master/Images/patches.svg" >
<p><b>Figure 1:</b> Grey patch over the image</b></div>  

![Alt Text](https://github.com/rao208/Explainable_AI/blob/master/Images/PATCH_64.gif) 
