import nibabel as nib

class DVFComposer(object):
    
    
    def __init__( self, 
                  dvfCompAP_niftiImageFileName, 
                  dvfCompSI_niftiImageFileName, 
                  dvfCompOffset_niftiImageFileName ):
        '''
        Initialise the composer object that can generate a DVF from the AP and SI motion model components. 
        
        @param dvfCompAP_niftiImageFileName: String with the path to the AP (chest) motion model component
        @param dvfCompSI_niftiImageFileName: String with the path to the SI (diaphragm) motion model component
        @param dvfCompOffset_niftiImageFileName: String with the path to the offset motion model component
        '''
        
        # Load the image information
        try:
            self.niiCompAP     = nib.load( dvfCompAP_niftiImageFileName )
            self.niiCompSI     = nib.load( dvfCompSI_niftiImageFileName )
            self.niiCompOffset = nib.load( dvfCompOffset_niftiImageFileName )
        
        except:
            print( "Could not load nifti files." )
            self.niiCompAP     = None
            self.niiCompSI     = None
            self.niiCompOffset = None
        
        
        
    def getDVFFromAPandSISurrogates( self, surrValAP, surrValSI ):
        '''
        Generate a nifti DVF object from the model components.
        
        @note: The first call of this method triggers the image data to be read from disk
        
        @param surrValAP: AP (chest) displacement surrogate value 
        @param surrValSI: SI (diaphragm) displacement surrogate value
        
        @return: nifti-image (geometry and header taken from AP component) with the model predicted DVF 
        '''
        
        # Make sure all data was loaded correctly
        if (self.niiCompAP == None) or (self.niiCompSI == None) or (self.niiCompOffset == None) :
            print( "Model components not available. Exiting here. " )
            return
        
        # Calculate the output DVF from the model components
        outDVF = surrValAP * self.niiCompAP.get_fdata() + surrValSI * self.niiCompSI.get_fdata() + self.niiCompOffset.get_fdata()
        
        # Generate the nifti output image
        outNii = nib.Nifti2Image( outDVF, self.niiCompAP.affine )
        
        return outNii
        
        
        
        
    
    
if __name__ == '__main__':
    
    # Define where to find the images
    apImgName     = 'Q:/Data/ICR/XCAT/2019_10/DVF/motionModelFromDVF/modelComp_ap.nii.gz'
    siImgName     = 'Q:/Data/ICR/XCAT/2019_10/DVF/motionModelFromDVF/modelComp_si.nii.gz'
    offsetImgName = 'Q:/Data/ICR/XCAT/2019_10/DVF/motionModelFromDVF/modelComp_offest.nii.gz'
    
    outDVFImgName = 'Q:/Data/ICR/XCAT/2019_10/DVF/motionModelFromDVF/testOutDVF.nii.gz'
    
    # Generate the DVF composer (assuming simple linear model for now)
    dvfComp = DVFComposer (apImgName, siImgName, offsetImgName )
    
    # Generate a DVF corresponding to the given surrogate signal values
    # Consider the value that was used when fitting the motion model 
    apVal = 5.3
    siVal = -12.4
    curDVF  = dvfComp.getDVFFromAPandSISurrogates( apVal, siVal  )
    
    # Test if the second call is faster...
    curDVF  = dvfComp.getDVFFromAPandSISurrogates( apVal, siVal  )
    
    nib.save( curDVF, outDVFImgName )
    pass
    