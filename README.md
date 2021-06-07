# Motion model built form post-processed XCAT DVFs

## Introduction

The extensible anthropomorphic XCAT phantom can simulate respiratory motion using a given breathing trace. The trace 
defines the anterior-posterior and inferior-superior motion separately, and the output is either a deformed image, or a 
deformation vector field (DVF). To obtain consistent and invertible motion -- and a corresponding DVF -- post-processing 
of the XCAT generated DVFs was proposed by [Eiben et al](https://doi.org/10.1088/1361-6560/ab8533). This library 
provides a linear motion model built from post-processed XCAT DVFs and thus a simplified and faster way to simulate 
breathing motion when compared to generating and post-processing every XCAT DVF separately. This simplification is a 
compromise between speed and accuracy. The DVFs obtained from the motion model point from the first time-point to the 
n-th and are thus only suitable for push-interpolation but have the advantage that these preserve the sliding motion.

## Motion model generation

From a set of 2400 post-processed DVFs a sub-set of 25 DVFs was selected to fit a linear motion model to every voxel of 
the simulated anatomy by the means of least-squares fitting. The model then describes the deformation at every voxel 
with respect to the AP/SI breathing trace signal value. 

## Usage

The fitting results are saved in three nifti images, namely 
* `modelComp_ap.nii.gz`
* `modelComp_si.nii.gz`, and
* `modelComp_offset.nii.gz`

which are available in the release files of this repository. In addition, the anatomical image in HU values was saved 
and the log file to make the simulation reproducible with the XCAT phantom. The image represents the anatomy for an 
AP-value of 8.80 and an SI-value of -34.88. 

To generate a DVF for any other AP/SI value, use the files and the code as follows:
```python
import nibabel as nib
# Define where to find the images
apImgName = './modelComp_ap.nii.gz'
siImgName = './modelComp_si.nii.gz'
offsetImgName = './modelComp_offest.nii.gz'

outDVFImgName = './testOutDVF00.nii.gz'

# Generate the DVF composer (linear model)
dvfComp = DVFComposer(apImgName, siImgName, offsetImgName)

# Generate a DVF corresponding to the given surrogate signal values
# Consider the value that was used when fitting the motion model 
apVal = 8.8
siVal = -34.88
curDVF = dvfComp.getDVFFromAPandSISurrogates( apVal, siVal )

nib.save( curDVF, outDVFImgName )
```

A sensible range for AP and SI values are `AP=[0, 20]` and `SI=[-40,0]`.  

## Requirements

The *nibabel* library to load and save nifti images has to be installed.  

