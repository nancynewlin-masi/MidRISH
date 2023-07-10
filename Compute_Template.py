# Code to get LineaRISH transformation to move subjects at site A to site B. 
# Will calculate the transformation in site A space and apply in site A.
# Creates template to apply to each subject at each site.
# load libraries

# Prior to this script, user must have run Calculate_RISH_Features.sh, then registered all RISH features to MNI space. 
# This script will scrape the directories defined in PATH_A and PATH_B for files named 

import os
import nibabel as nib
import numpy as np


path ="/nfs/masi/newlinnr/midrish/VMAP/"
rish0imagesA = []
rish2imagesA = []
rish4imagesA = []
rish6imagesA = []

nibmask = nib.load('/nfs/masi/newlinnr/cr3/mni_icbm152_t1_tal_nlin_sym_09a_mask.nii');
mask = nibmask.get_fdata()

print("Searching [",path,"] directory for files names rish0_mni.nii.gz, rish2_mni.nii.gz, rish4_mni.nii.gz and rish6_mni.nii.gz")

for root, dirs, files in os.walk(path):
	for file in files:
		if(file.endswith("rish_norm_0_mni.nii.gz")):
			nibimage = nib.load(os.path.join(root,file))
			imagedata = nibimage.get_fdata()
			aff = nibimage.affine
			rish0imagesA.append(np.array(imagedata))

		if(file.endswith("rish_norm_2_mni.nii.gz")):
			nibimage = nib.load(os.path.join(root,file))
			imagedata = nibimage.get_fdata()
			rish2imagesA.append(np.array(imagedata))

		if(file.endswith("rish_norm_4_mni.nii.gz")):
			nibimage = nib.load(os.path.join(root,file))
			imagedata = nibimage.get_fdata()
			rish4imagesA.append(np.array(imagedata))

#		if(file.endswith("rish_norm_6_mni.nii.gz")):
#			nibimage = nib.load(os.path.join(root,file))
#			imagedata = nibimage.get_fdata()
#			rish6imagesA.append(np.array(imagedata))



rish0imagesA = np.array(rish0imagesA)
rish2imagesA = np.array(rish2imagesA)
rish4imagesA = np.array(rish4imagesA)
#rish6imagesA = np.array(rish6imagesA)


print("Generating RISH template for",rish0imagesA.shape[0],"subjects.")
numsubjectsA = rish0imagesA.shape[0]
if numsubjectsA==0:
	raise Exception("No files found in directory [",path,"]. Exiting.")

# Do same thing for BLSA
# Calculate square root
# Multiply by new SH 
# visualize


# all expected values have same shape as image (voxels)
# sum across subjects
expected_A_i0 = sum(rish0imagesA) / numsubjectsA
expected_A_i2 = sum(rish2imagesA) / numsubjectsA
expected_A_i4 = sum(rish4imagesA) / numsubjectsA
#expected_A_i6 = sum(rish6imagesA) / numsubjectsA

print("Dimensions of expected value for RISH 0th order:", expected_A_i0.shape)

nib.save(nib.Nifti1Image(expected_A_i0, aff),'/nfs/masi/newlinnr/cr3/expected_A_i0_mni.nii.gz')
#path ="/nfs/masi/newlinnr/masivar/scanner3/"
#path ="/nfs/masi/newlinnr/VMAP_cr3/"
#path ="/nfs/masi/newlinnr/midrish/ADNI/SiteB/"
path ="/nfs/masi/newlinnr/midrish/BLSA/"
rish0imagesB = []
rish2imagesB = []
rish4imagesB = []
#rish6imagesB = []


print("Searching [",path,"] directory for files names rish0_mni.nii.gz, rish0_mni.nii.gz, rish0_mni.nii.gz and rish0_mni.nii.gz")

for root, dirs, files in os.walk(path):
	for file in files:
		if(file.endswith("rish_norm_0_mni.nii.gz")):
			nibimage = nib.load(os.path.join(root,file))
			imagedata = nibimage.get_fdata()
			rish0imagesB.append(np.array(imagedata))

		if(file.endswith("rish_norm_2_mni.nii.gz")):
			nibimage = nib.load(os.path.join(root,file))
			imagedata = nibimage.get_fdata()
			rish2imagesB.append(np.array(imagedata))

		if(file.endswith("rish_norm_4_mni.nii.gz")):
			nibimage = nib.load(os.path.join(root,file))
			imagedata = nibimage.get_fdata()
			rish4imagesB.append(np.array(imagedata))

#		if(file.endswith("rish_norm_6_mni.nii.gz")):
#			nibimage = nib.load(os.path.join(root,file))
#			imagedata = nibimage.get_fdata()
#			rish6imagesB.append(np.array(imagedata))



rish0imagesB = np.array(rish0imagesB)
rish2imagesB = np.array(rish2imagesB)
rish4imagesB = np.array(rish4imagesB)
#rish6imagesB = np.array(rish6imagesB)


numsubjectsB = rish0imagesB.shape[0]
print("Number of subjects from second site",numsubjectsB)
if numsubjectsA==0:
	raise Exception("No files found in directory [",path,"]. Exiting.")
expected_B_i0 = sum(rish0imagesB) / numsubjectsB
expected_B_i2 = sum(rish2imagesB) / numsubjectsB
expected_B_i4 = sum(rish4imagesB) / numsubjectsB
#expected_B_i6 = sum(rish6imagesB) / numsubjectsB



print("Saving expected values...")
nib.save(nib.Nifti1Image(expected_A_i0, aff),'/nfs/masi/newlinnr/midrish/templates/expected_VMAP_i0.nii.gz')
nib.save(nib.Nifti1Image(expected_A_i2, aff),'/nfs/masi/newlinnr/midrish/templates/expected_VMAP_i2.nii.gz')
nib.save(nib.Nifti1Image(expected_A_i4, aff),'/nfs/masi/newlinnr/midrish/templates/expected_VMAP_i4.nii.gz')
#nib.save(nib.Nifti1Image(expected_A_i6, aff),'/nfs/masi/newlinnr/midrish/templates/expected_VMAP_i6.nii.gz')

nib.save(nib.Nifti1Image(expected_B_i0, aff),'/nfs/masi/newlinnr/midrish/templates/expected_BLSA_correct_i0.nii.gz')
nib.save(nib.Nifti1Image(expected_B_i2, aff),'/nfs/masi/newlinnr/midrish/templates/expected_BLSA_correct_i2.nii.gz')
nib.save(nib.Nifti1Image(expected_B_i4, aff),'/nfs/masi/newlinnr/midrish/templates/expected_BLSA_correct_i4.nii.gz')
#nib.save(nib.Nifti1Image(expected_B_i6, aff),'/nfs/masi/newlinnr/midrish/templates/expected_BLSA_i6.nii.gz')

eps = 0.000001

template0 = np.sqrt(((expected_B_i0 + eps)/(expected_A_i0 + eps)))
template2 = np.sqrt(((expected_B_i2 + eps)/(expected_A_i2 + eps)))
template4 = np.sqrt(((expected_B_i4 + eps)/(expected_A_i4 + eps)))
#template6 = np.sqrt(((expected_B_i6 + eps)/(expected_A_i6 + eps)))

template0inv = np.sqrt(((expected_A_i0 + eps)/(expected_B_i0 + eps)))
template2inv = np.sqrt(((expected_A_i2 + eps)/(expected_B_i2 + eps)))
template4inv = np.sqrt(((expected_A_i4 + eps)/(expected_B_i4 + eps)))
#template6inv = np.sqrt(((expected_A_i6 + eps)/(expected_B_i6 + eps)))


for x in np.arange(0,template0.shape[0]):
	for y in np.arange(0,template0.shape[1]):
		for z in np.arange(0,template0.shape[2]):
			if expected_B_i0[x,y,z] == 0 or expected_A_i0[x,y,z] ==0:
				template0[x,y,z] = 0
				template2[x,y,z] = 0
				template4[x,y,z] = 0
#				template6[x,y,z] = 0
			if mask[x,y,z] == 0:
				template0[x,y,z] = 1
				template2[x,y,z] = 1
				template4[x,y,z] = 1
#				template6[x,y,z] = 1



# resultant template will have size (order=6, imagedim1, imagedim2, imagedim3)
#template = np.array([template0, template2, template4, template6])
numorder=3;
template = np.zeros((template0.shape[0], template0.shape[1], template0.shape[2], numorder))
template[:,:,:,0] = template0
template[:,:,:,1] = template2
template[:,:,:,2] = template4
#template[:,:,:,3] = template6

print('Template RISH0 shape',template0.shape)
print('Template shape',template.shape)

nib.save(nib.Nifti1Image(template, aff),'/nfs/masi/newlinnr/midrish/templates/template_vmap2blsa2corr_mni_norm.nii.gz')
nib.save(nib.Nifti1Image(template0, aff),'/nfs/masi/newlinnr/midrish/templates/template_vmap2blsa2corr_mni_o0_norm.nii.gz')
nib.save(nib.Nifti1Image(template2, aff),'/nfs/masi/newlinnr/midrish/templates/template_vmap2blsa2corr_mni_o2_norm.nii.gz')
nib.save(nib.Nifti1Image(template4, aff),'/nfs/masi/newlinnr/midrish/templates/template_vmap2blsa2corr_mni_o4_norm.nii.gz')
#nib.save(nib.Nifti1Image(template6, aff),'/nfs/masi/newlinnr/midrish/templates/template_vmap2blsa_mni_o6_norm.nii.gz')

nib.save(nib.Nifti1Image(template0inv, aff),'/nfs/masi/newlinnr/midrish/templates/template_blsa22vmapcorr_mni_o0_norm.nii.gz')
nib.save(nib.Nifti1Image(template2inv, aff),'/nfs/masi/newlinnr/midrish/templates/template_blsa22vmapcorr_mni_o2_norm.nii.gz')
nib.save(nib.Nifti1Image(template4inv, aff),'/nfs/masi/newlinnr/midrish/templates/template_blsa22vmapcorr_mni_o4_norm.nii.gz')
#nib.save(nib.Nifti1Image(template6inv, aff),'/nfs/masi/newlinnr/midrish/templates/template_blsa2vmap_mni_o6_norm.nii.gz')

"""
# needs to be of shape (numsubjects, imagedim1, imagedim2, imagedim3) so that sums across subjects to get (imagedim1, imagedim2)
# divide by total number of subjects
# Combine into one template of size (rish order, imagedim1, imagedim2, imagedim3)
# save as template

differenceA2B_i0 = expected_B_i0 - expected_A_i0;
differenceA2B_i2 = expected_B_i2 - expected_A_i2;
differenceA2B_i4 = expected_B_i4 - expected_A_i4;
differenceA2B_i6 = expected_B_i6 - expected_A_i6;
differenceA2B_i8 = expected_B_i8 - expected_A_i8;

differenceB2A_i0 = expected_A_i0 - expected_B_i0;
differenceB2A_i2 = expected_A_i2 - expected_B_i2;
differenceB2A_i4 = expected_A_i4 - expected_B_i4;
differenceB2A_i6 = expected_A_i6 - expected_B_i6;
differenceB2A_i8 = expected_A_i8 - expected_B_i8;

print("Saving difference maps...")
nib.save(nib.Nifti1Image(differenceA2B_i0, aff),'/nfs/masi/newlinnr/midrish/templates/difference_A2B_i0_med.nii.gz')
nib.save(nib.Nifti1Image(differenceA2B_i2, aff),'/nfs/masi/newlinnr/midrish/templates/difference_A2B_i2_med.nii.gz')
nib.save(nib.Nifti1Image(differenceA2B_i4, aff),'/nfs/masi/newlinnr/midrish/templates/difference_A2B_i4_med.nii.gz')
nib.save(nib.Nifti1Image(differenceA2B_i6, aff),'/nfs/masi/newlinnr/midrish/templates/difference_A2B_i6_med.nii.gz')
nib.save(nib.Nifti1Image(differenceA2B_i8, aff),'/nfs/masi/newlinnr/midrish/templates/difference_A2B_i8_med.nii.gz')

nib.save(nib.Nifti1Image(differenceB2A_i0, aff),'/nfs/masi/newlinnr/midrish/templates/difference_B2A_i0_med.nii.gz')
nib.save(nib.Nifti1Image(differenceB2A_i2, aff),'/nfs/masi/newlinnr/midrish/templates/difference_B2A_i2_med.nii.gz')
nib.save(nib.Nifti1Image(differenceB2A_i4, aff),'/nfs/masi/newlinnr/midrish/templates/difference_B2A_i4_med.nii.gz')
nib.save(nib.Nifti1Image(differenceB2A_i6, aff),'/nfs/masi/newlinnr/midrish/templates/difference_B2A_i6_med.nii.gz')
nib.save(nib.Nifti1Image(differenceB2A_i8, aff),'/nfs/masi/newlinnr/midrish/templates/difference_B2A_i8_med.nii.gz')

"""
