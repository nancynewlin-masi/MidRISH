import nibabel as nib
import numpy as np
import sys

#example: /nfs/masi/newlinnr/VMAP_cr3/028_VMAP_209306/template_subj.nii.gz
saveloc = sys.argv[4]

# read in template 0-6
o0 = nib.load(sys.argv[1]).get_fdata()
o2 = nib.load(sys.argv[2]).get_fdata()
o4 = nib.load(sys.argv[3]).get_fdata()
#o6 = nib.load(sys.argv[4]).get_fdata()
#o8 = nib.load(sys.argv[5]).get_fdata()


template0 = o0
numorder=5
template = np.zeros((template0.shape[0], template0.shape[1], template0.shape[2], numorder))
template[:,:,:,0] = o0
template[:,:,:,1] = o2
template[:,:,:,2] = o4
#template[:,:,:,3] = o6
#template[:,:,:,4] = o8


aff = nib.load(sys.argv[1]).affine
nib.save(nib.Nifti1Image(template, aff),saveloc)

print("Successfully combined template and saved at",saveloc)
