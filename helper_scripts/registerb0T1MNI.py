# Written with the help of chatgbt, given the "promptnancy.r.newlin@vanderbilt.edu write a script in python using antspy to stack a rigid and affine registration"
import nibabel as nib
import numpy as np
import sys

import ants
b0 = sys.argv[1]
T1= sys.argv[2]
mni = '/nfs/masi/newlinnr/cr3/MNI152NLinSym.nii'
outdir = sys.argv[3] # holds rish images and output images

print("Load images...")
# Load the images to be registered
mni_image = ants.image_read(mni)
T1_image = ants.image_read(T1)
b0_image = ants.image_read(b0)


rish0=""+outdir+"/rish_norm_0.nii.gz"
rish2=""+outdir+"/rish_norm_2.nii.gz"
rish4=""+outdir+"/rish_norm_4.nii.gz"
rish0_image = ants.image_read(rish0)
rish2_image = ants.image_read(rish2)
rish4_image = ants.image_read(rish4)

print("Start rigit transform b0->T1...")
# Run rigid registration
rigid_transform = ants.registration(fixed=T1_image, moving=b0_image, type_of_transform='Rigid')

print("Start affine transform T1->MNI...")
# Run affine registration
affine_transform = ants.registration(fixed=mni_image, moving=T1_image, type_of_transform='Affine',
                                     initial_transform=rigid_transform['fwdtransforms'][0])

print("Combine both transforms...")
# Combine transformations
#stacked_transform = ants.apply_transforms(fixed=mni_image, moving=b0_image,
#                                          transformlist=[affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]])

print("Apply transforms to rish0,2,and 4")
# Apply stacked transformation to moving image
registered_image_rish0 = ants.apply_transforms(fixed=mni_image, moving=rish0_image, transformlist=[affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]])
registered_image_rish2 = ants.apply_transforms(fixed=mni_image, moving=rish2_image, transformlist=[affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]])
registered_image_rish4 = ants.apply_transforms(fixed=mni_image, moving=rish4_image, transformlist=[affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]])


print("Save registered images to ",outdir)
# Save the registered image
rish0=""+outdir+"/rish_norm_0_mni.nii.gz"
rish2=""+outdir+"/rish_norm_2_mni.nii.gz"
rish4=""+outdir+"/rish_norm_4_mni.nii.gz"
aff = nib.load(mni).affine
nib.save(nib.Nifti1Image(registered_image_rish0.numpy(), aff),rish0)
nib.save(nib.Nifti1Image(registered_image_rish2.numpy(), aff),rish2)
nib.save(nib.Nifti1Image(registered_image_rish4.numpy(), aff),rish4)
#ants.image_write(registered_image_rish0, rish0)
#ants.image_write(registered_image_rish2, rish2)
#ants.image_write(registered_image_rish4, rish4)
