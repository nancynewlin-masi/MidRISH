export DWI=${1}
export BVEC=${2}
export BVAL=${3}
export MASK=${4}
export OUTDIR=${5}

export SH=${OUTDIR}/sh_norm.nii.gz
export SH_ORDER=4

#echo "B-Value map for BLSA"
python3.8 bvaluemap.py ${DWI} ${OUTDIR}/b0.nii.gz ${OUTDIR}/dwi_b1000.nii.gz
export DWI=${OUTDIR}/dwi_b1000.nii.gz
export BVAL=1000.bval

# Spherical harmonic decomposition (calculated by least-squares linear fitting to amplitude data (diffusion signal))
rm ${OUTDIR}/sh_b4correction.nii.gz # clean previous attempts 
echo "Spherical harmonic decomposition: amp2sh ${DWI} ${SH}"
amp2sh ${DWI} ${OUTDIR}/sh_b4correction.nii.gz  -fslgrad ${BVEC} ${BVAL} -normalise -lmax ${SH_ORDER}

rm ${SH}
echo "Fix the basis functions using dipy2mrtrix"
python3.8 dipy2mrtrix.py ${OUTDIR}/sh_b4correction.nii.gz ${SH}

echo "Remove ${OUTDIR}/sh_b4correction.nii.gz"
rm ${OUTDIR}/sh_b4correction.nii.gz

# Calculate Rotationally Invariant Spherical harmonic features
echo "Calculate RISH features"
python3.8  calculaterish.py ${OUTDIR} ${SH_ORDER} ${SH}
rm  ${OUTDIR}/dwi_b1000.nii.gz
