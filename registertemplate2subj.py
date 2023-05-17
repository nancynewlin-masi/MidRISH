# Written with the help of chatgbt, given the "promptnancy.r.newlin@vanderbilt.edu write a script in python using antspy to stack a rigid and affine registration"
import nibabel as nib
import numpy as np
import sys

import ants
b0 = sys.argv[1]
T1= sys.argv[2]
mni = '/nfs/masi/newlinnr/cr3/MNI152NLinSym.nii'
outdir = sys.argv[3] # holds template images and output images
templateID = sys.argv[4]

print("Load images...")
# Load the images to be registered
mni_image = ants.image_read(mni)
T1_image = ants.image_read(T1)
b0_image = ants.image_read(b0)

# ADNI2blsa
template0="/nfs/masi/newlinnr/midrish/templates/template_"+templateID+"_mni_o0_norm.nii.gz"
template2="/nfs/masi/newlinnr/midrish/templates/template_"+templateID+"_mni_o2_norm.nii.gz"
template4="/nfs/masi/newlinnr/midrish/templates/template_"+templateID+"_mni_o4_norm.nii.gz"
template0_image = ants.image_read(template0)
template2_image = ants.image_read(template2)
template4_image = ants.image_read(template4)

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

print("Apply transforms to template0,2,and 4")
# Apply stacked transformation to moving image
#registered_image_template0 = ants.apply_transforms(fixed=b0_image, moving=template0_image, transformlist=[affine_transform['invtransforms'][0], rigid_transform['invtransforms'][0]])
#registered_image_template2 = ants.apply_transforms(fixed=b0_image, moving=template2_image, transformlist=[affine_transform['invtransforms'][0], rigid_transform['invtransforms'][0]])
#registered_image_template4 = ants.apply_transforms(fixed=b0_image, moving=template4_image, transformlist=[affine_transform['invtransforms'][0], rigid_transform['invtransforms'][0]])
registered_image_template0 = ants.apply_transforms(fixed=b0_image, moving=template0_image, transformlist=[rigid_transform['fwdtransforms'][0], affine_transform['fwdtransforms'][0]], whichtoinvert=[True]*len([affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]]))
registered_image_template2 = ants.apply_transforms(fixed=b0_image, moving=template2_image, transformlist=[rigid_transform['fwdtransforms'][0], affine_transform['fwdtransforms'][0]], whichtoinvert=[True]*len([affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]]))
registered_image_template4 = ants.apply_transforms(fixed=b0_image, moving=template4_image, transformlist=[rigid_transform['fwdtransforms'][0], affine_transform['fwdtransforms'][0]], whichtoinvert=[True]*len([affine_transform['fwdtransforms'][0], rigid_transform['fwdtransforms'][0]]))


print("Save registered images to ",outdir)
# Save the registered image
template0=""+outdir+"/template_i0_subj_norm.nii.gz"
template2=""+outdir+"/template_i2_subj_norm.nii.gz"
template4=""+outdir+"/template_i4_subj_norm.nii.gz"
aff = nib.load(b0).affine
nib.save(nib.Nifti1Image(registered_image_template0.numpy(), aff),template0)
nib.save(nib.Nifti1Image(registered_image_template2.numpy(), aff),template2)
nib.save(nib.Nifti1Image(registered_image_template4.numpy(), aff),template4)
#ants.image_write(registered_image_template0, template0)
#ants.image_write(registered_image_template2, template2)
#ants.image_write(registered_image_template4, template4)
