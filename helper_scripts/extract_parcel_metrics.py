import os
import numpy as np
import sys
import nibabel as nib

# assumes that atlas and fa map are in the same space (pre-registered)

atlas = sys.argv[1];
fa_map = sys.argv[2];
md_map = sys.argv[3];
ad_map = sys.argv[4];
rd_map = sys.argv[5];
subj = sys.argv[6];

atlas_nibimage = nib.load(atlas);
atlas_data = atlas_nibimage.get_fdata();
atlas_affine = atlas_nibimage.affine;

fa_nibimage = nib.load(fa_map);
fa_data = fa_nibimage.get_fdata();
fa_affine  = fa_nibimage.affine;

md_nibimage = nib.load(md_map);
md_data = md_nibimage.get_fdata();
md_affine  = md_nibimage.affine;

rd_nibimage = nib.load(rd_map);
rd_data = rd_nibimage.get_fdata();
rd_affine  = rd_nibimage.affine;


out_data = np.zeros(atlas_data.shape);
#mask = 1*(atlas_data == 140) + 1*(atlas_data == 52);
#mask = 1*(atlas_data == 4) + 1*(atlas_data == 5) + 1*(atlas_data == 6);
#mask = 1*(atlas_data == 44) + 1*(atlas_data == 45);
mask = 1*(atlas_data == 47) + 1*(atlas_data == 48);
#mask = 1*(atlas_data == 90);
#mask = 1*(atlas_data == 23) +  1*(atlas_data == 24) +  1*(atlas_data == 25) +  1*(atlas_data == 26) +  1*(atlas_data == 27) +  1*(atlas_data == 28)
x = mask*fa_data;
y = mask*md_data;
z = mask*rd_data;

#y = y[y!=0];
#y = md_data[atlas_data==141]
#print(subj,':MD', np.nanmean(y));
#for i in np.arange(0,208,1):
#	y = 1*(atlas_data==i)*md_data;
#	y = y[y!=0];
#	print(i, np.nanmean(y));
	

#for yi in y:
#	print(yi)
print(subj, ': FA', np.nansum(x)/np.nansum(mask), ',MD', np.nansum(y)/np.nansum(mask), ',RD', np.nansum(z)/np.nansum(mask));
#out_data = y;
#out_image = nib.Nifti1Image(out_data, md_affine);
#out_location = '/nfs/masi/newlinnr/midrish/blsa_genubody.nii.gz'
#nib.save(out_image, out_location);

