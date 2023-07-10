import numpy as np
import os
import nibabel as nib
import sys

filename = sys.argv[1]
maskname = sys.argv[2]
outloc = sys.argv[3]

# load image
image = nib.load(filename)
data = image.get_fdata()

masknib = nib.load(maskname)
mask = image.get_fdata()
new_data = np.zeros(data.shape)
for x in np.arange(0,data.shape[0]):
	for y in np.arange(0, data.shape[1]):
		for z in np.arange(0,data.shape[2]):
			if(mask[x,y,z] < 142 and mask[x,y,z] > 140):
				new_data[x,y,z,:]=data[x,y,z,:]
				print(data[x,y,z,:])
clipped_img = nib.Nifti1Image(new_data, image.affine, image.header)
nib.save(clipped_img, outloc)
