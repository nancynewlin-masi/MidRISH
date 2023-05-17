from cmath import nan
import sys
import nibabel as nib
import numpy as np

# Used https://mrtrix.readthedocs.io/en/latest/concepts/spherical_harmonics.html to determine which volumes corresponded to which harmonic orders.
# Specificually, see 'storage conventions' subsection. 

# Assumes there is already a sh file generated for this subject

template_filename = sys.argv[1]
sh_filename = sys.argv[2]
outlocation = sys.argv[3]

# load in template with dimensions (maxshorder, imagedim1, imagedim2,imagedim3)
template_nibimage = nib.load(template_filename)
template_imagedata = template_nibimage.get_fdata()
#template_imagedata = (template_imagedata) # * (template_imagedata > 0)
template_aff = template_nibimage.affine

# load in sh with dimensions ([special order number, i.e. order 6 => 28]], imagedim1, imagedim2,imagedim3)
sh_nibimage = nib.load(sh_filename)
sh_imagedata = sh_nibimage.get_fdata()
sh_imagedata = sh_imagedata
sh_aff = sh_nibimage.affine

# initialize output image
sh_outarray = sh_imagedata # np.zeros(sh_imagedata.shape)

# list of which harmonic order each volume is (hard coded for order 6)
#harmonicorder = np.array([0, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8])
#templateindex = np.array([0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

harmonicorder = np.array([0, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4])
templateindex = np.array([0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2])

for volume in np.arange(0,harmonicorder.shape[0]):
#    if harmonicorder[volume]<3:
        print('Inside Volume',volume,'template index',templateindex[volume],'and harmonic order', harmonicorder[volume])
#    if template_imagedata[templateindex[volume], :,:,:] > 0:
        sh_outarray[:,:,:,volume] = template_imagedata[:,:,:,templateindex[volume]] * sh_imagedata[:,:,:,volume]

sh_outarray = np.nan_to_num(sh_outarray)
print("Successfully harmonized SH coefficients.")
nib.save(nib.Nifti1Image(sh_outarray, sh_aff),outlocation)


    



