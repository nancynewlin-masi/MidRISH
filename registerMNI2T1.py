# Written with the help of chatgbt, given the "promptnancy.r.newlin@vanderbilt.edu write a script in python using antspy to stack a rigid and affine registration"
import nibabel as nib
import numpy as np
import sys
#python3.8 registerMNI2T1.py ${T1} ${OUTDIR} 
import ants
T1= sys.argv[1]
mni = '/nfs/masi/newlinnr/cr3/MNI152NLinSym.nii'
outdir = sys.argv[2] # holds template images and output images
templateID = sys.argv[3]

print("Load images...")
# Load the images to be registered
mni_image = ants.image_read(mni)
T1_image = ants.image_read(T1)
#b0_image = ants.image_read(b0)

# ADNI2blsa
template0="/nfs/masi/newlinnr/midrish/templates/template_"+templateID+"_mni_o0_norm.nii.gz"
template2="/nfs/masi/newlinnr/midrish/templates/template_"+templateID+"_mni_o2_norm.nii.gz"
template4="/nfs/masi/newlinnr/midrish/templates/template_"+templateID+"_mni_o4_norm.nii.gz"
template0_image = ants.image_read(template0)
template2_image = ants.image_read(template2)
template4_image = ants.image_read(template4)

print("Start rigit transform b0->T1...")
# Run rigid registration
#rigid_transform = ants.registration(fixed=T1_image, moving=b0_image, type_of_transform='Rigid')

print("Start affine transform T1->MNI...")
# Run affine registration
affine_transform = ants.registration(fixed=mni_image, moving=T1_image, type_of_transform='Affine')
                                        

print("Apply transforms to template0,2,and 4")
registered_image_template0 = ants.apply_transforms(fixed=T1_image, moving=template0_image, transformlist=[affine_transform['fwdtransforms'][0]], whichtoinvert=[True])
registered_image_template2 = ants.apply_transforms(fixed=T1_image, moving=template2_image, transformlist=[affine_transform['fwdtransforms'][0]], whichtoinvert=[True])
registered_image_template4 = ants.apply_transforms(fixed=T1_image, moving=template4_image, transformlist=[affine_transform['fwdtransforms'][0]], whichtoinvert=[True])


print("Save registered images to ",outdir)
# Save the registered image  ${OUTDIR}/template_i0_T1.nii.gz
template0=""+outdir+"/template_i0_T1.nii.gz"
template2=""+outdir+"/template_i2_T1.nii.gz"
template4=""+outdir+"/template_i4_T1.nii.gz"
aff = nib.load(T1).affine
nib.save(nib.Nifti1Image(registered_image_template0.numpy(), aff),template0)
nib.save(nib.Nifti1Image(registered_image_template2.numpy(), aff),template2)
nib.save(nib.Nifti1Image(registered_image_template4.numpy(), aff),template4)
#ants.image_write(registered_image_template0, template0)
#ants.image_write(registered_image_template2, template2)
#ants.image_write(registered_image_template4, template4)
