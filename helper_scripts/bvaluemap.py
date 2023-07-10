import nibabel as nib
import numpy as np

import sys

dwiimagename = sys.argv[1]
dwiimage = nib.load(dwiimagename)
dwiimageobj = dwiimage.get_fdata()
aff = dwiimage.affine

b0imagename = sys.argv[2]
b0image = nib.load(b0imagename)
b0imageobj = b0image.get_fdata()

savelocation = sys.argv[3]

dwiimageshape = dwiimageobj.shape
b0imageshape = b0imageobj.shape

oldb = 700
newb = 1000

D = -1/(oldb)

norm = np.zeros(dwiimageshape)

for vol in np.arange(0,dwiimageobj.shape[3]):
	print(vol)
	norm[:,:,:,vol] = dwiimageobj[:,:,:,vol]/b0imageobj	

print(norm.shape)
D = D*np.log(norm)

S = np.exp(-newb * D)
outimage = np.zeros(dwiimageshape)

for vol in np.arange(0,dwiimageobj.shape[3]):
	print(vol)
	outimage[:,:,:,vol] = S[:,:,:,vol]*b0imageobj

print(S.shape)
nib.save(nib.Nifti1Image(outimage, aff),savelocation)

