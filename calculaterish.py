import os
import numpy as np
import sys
import nibabel as nib

#sh = sys.argv[1]
order = int(sys.argv[2])
outdir = sys.argv[1]
sh = sys.argv[3]
# assumes that sh normalized is already by normalizedwi.py ${DWI} ${B0}

sh_nibimage = nib.load(sh);
sh_data = sh_nibimage.get_fdata();
sh_affine = sh_nibimage.affine;

startindex = {
	"0":0,
	"2":1,
	"4":6,
	"6":15,
	"8":28
}
endindex = {
	"0":1,
	"2":6,
	"4":15,
	"6":28,
	"8":45
}

for i in range(0,order+1,2):
	print("Calculating RISH for order",i)
	print("Start index:",startindex.get(str(i)),"End index",endindex.get(str(i)))
	
	rish_data = np.zeros((sh_data.shape[0],sh_data.shape[1], sh_data.shape[2]))
	for volume in np.arange(startindex.get(str(i)), endindex.get(str(i))):
		rish_data += np.power(sh_data[:,:,:,volume],2)
		print("Adding square of volume",volume," to order", i)	

	# Save rish volume
	out_image = nib.Nifti1Image(rish_data, sh_affine);
	out_location = outdir + "/rish_norm_" + str(i) + ".nii.gz"
	nib.save(out_image, out_location);
	print("Save RISH order",i," to ",out_location)
