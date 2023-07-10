export DWI=${1}
export BVEC=${2}
export BVAL=${3}
export MASK=${4} # mask in DWI space
export T1=${5}
export OUTDIR=${6} # location to store fa, md, ad and tensor images
export ID=${7} # name of template to apply

export MAX_ORDER=4 # change depending on distribution of b-vector directions on the sphere

# get B0
echo "Checking for B0 file..."
if test -f "${OUTDIR}/b0.nii.gz"; then
        echo "CHECK: B0 found. Proceeding to next step."
else
        echo "CHECK FAILED: B0 not found. Making now..."
            dwiextract ${DWI} -fslgrad ${BVEC} ${BVAL} - -bzero | mrmath - mean ${OUTDIR}/b0.nii.gz -axis 3
        echo "FIXED: Made B0"
fi

# Transpose bvecs
if test -f "${OUTDIR}/transposed_bvecs.bvec"; then
        echo "Already transposed bvecs - continue"
else
        echo "Transposing bvec file to be used in resampling SH to DWI"
        python -c "import sys; print('\n'.join(' '.join(c) for c in zip(*(l.split() for l in sys.stdin.readlines() if l.strip()))))" < ${BVEC} >  ${OUTDIR}/transposed_bvecs.bvec
fi

export B0=${OUTDIR}/b0.nii.gz
echo "Get SH from DWI (control)"
amp2sh ${DWI} ${OUTDIR}/sh_uncorrected.nii.gz -fslgrad ${BVEC} ${BVAL} -force -lmax ${MAX_ORDER} -normalise

rm ${OUTDIR}/sh_norm.nii.gz

echo "Correct Basis"
python3.8 dipy2mrtrix.py ${OUTDIR}/sh_uncorrected.nii.gz ${OUTDIR}/sh_norm.nii.gz

echo "Clean uncorrected SH ${OUTDIR}/sh_uncorrected.nii.gz"
rm ${OUTDIR}/sh_uncorrected.nii.gz

echo "Get SF from SH (control)"
sh2amp ${OUTDIR}/sh_norm.nii.gz ${OUTDIR}/transposed_bvecs.bvec  ${OUTDIR}/sf_control_nob0.nii.gz  -fslgrad ${BVEC} ${BVAL} -nonnegative  -force
python3.8 replace_b0s_ones.py --from ${DWI} --to ${OUTDIR}/sf_control_nob0.nii.gz  --output ${OUTDIR}/sf_control.nii.gz --bvecs ${BVEC} --bvals ${BVAL}

echo "Register template to subj space"
#python3.8 /nfs/masi/newlinnr/midrish/registertemplate2subj.py ${OUTDIR}/b0.nii.gz ${T1} ${OUTDIR} ${ID}
echo "EPI Reg B0->T1"
bet ${T1} ${OUTDIR}/T1_bet.nii.gz

epi_reg --epi=${OUTDIR}/b0.nii.gz --t1=${T1} --t1brain=${OUTDIR}/T1_bet.nii.gz --out=${OUTDIR}/b02t1

echo "Convert transform to go in oppisite direction"
convert_xfm -omat ${OUTDIR}/t12b0.mat -inverse ${OUTDIR}/b02t1.mat

echo "registration step 1: MNI->T1"
python3.8 registerMNI2T1.py ${T1} ${OUTDIR} ${ID}

echo "Apply transform to atlas"
flirt -in ${OUTDIR}/template_i0_T1.nii.gz -ref ${OUTDIR}/b0.nii.gz -applyxfm -init ${OUTDIR}/t12b0.mat -interp nearestneighbour -out ${OUTDIR}/template_i0_subj_norm.nii.gz
flirt -in ${OUTDIR}/template_i2_T1.nii.gz -ref ${OUTDIR}/b0.nii.gz -applyxfm -init ${OUTDIR}/t12b0.mat -interp nearestneighbour -out ${OUTDIR}/template_i2_subj_norm.nii.gz
flirt -in ${OUTDIR}/template_i4_T1.nii.gz -ref ${OUTDIR}/b0.nii.gz -applyxfm -init ${OUTDIR}/t12b0.mat -interp nearestneighbour -out ${OUTDIR}/template_i4_subj_norm.nii.gz


echo "Apply Scaling to SH to get harmonized SH"
python3.8 combinetemplate.py ${OUTDIR}/template_i0_subj_norm.nii.gz ${OUTDIR}/template_i2_subj_norm.nii.gz ${OUTDIR}/template_i4_subj_norm.nii.gz ${OUTDIR}/template_combined_subj_norm.nii.gz
python3.8 apply_template_A2B.py ${OUTDIR}/template_combined_subj_norm.nii.gz  ${OUTDIR}/sh_norm.nii.gz ${OUTDIR}/sh_rish_norm.nii.gz
sh2amp ${OUTDIR}/sh_rish_norm.nii.gz ${OUTDIR}/transposed_bvecs.bvec  ${OUTDIR}/sf_rish_norm_nob0.nii.gz  -fslgrad ${BVEC} ${BVAL} -nonnegative  -force

echo "Apply Mid RISH scaling to SH to get harmonized SH"
python3.8 apply_template_A2mid.py ${OUTDIR}/template_combined_subj_norm.nii.gz  ${OUTDIR}/sh_norm.nii.gz ${OUTDIR}/sh_mid_norm.nii.gz
sh2amp ${OUTDIR}/sh_mid_norm.nii.gz ${OUTDIR}/transposed_bvecs.bvec  ${OUTDIR}/sf_mid_norm_nob0.nii.gz  -fslgrad ${BVEC} ${BVAL} -nonnegative  -force

echo "Get SF from harmonized SH"
python3.8 replace_b0s_ones.py --from ${DWI} --to ${OUTDIR}/sf_rish_norm_nob0.nii.gz  --output ${OUTDIR}/sf_rish_norm.nii.gz --bvecs ${BVEC} --bvals ${BVAL}
python3.8 replace_b0s_ones.py --from ${DWI} --to ${OUTDIR}/sf_mid_norm_nob0.nii.gz  --output ${OUTDIR}/sf_mid_norm.nii.gz --bvecs ${BVEC} --bvals ${BVAL}

echo "Get tensor from SF"
dwi2tensor ${OUTDIR}/sf_control.nii.gz ${OUTDIR}/tensor_control.nii.gz   --mask ${MASK} -fslgrad ${BVEC} ${BVAL} -force
dwi2tensor ${OUTDIR}/sf_rish_norm.nii.gz ${OUTDIR}/tensor_rish_norm.nii.gz --mask ${MASK} -fslgrad ${BVEC} ${BVAL}  -force
dwi2tensor ${OUTDIR}/sf_mid_norm.nii.gz ${OUTDIR}/tensor_mid_norm.nii.gz --mask ${MASK} -fslgrad ${BVEC} ${BVAL}  -force


echo "Get FA from tensor"
tensor2metric ${OUTDIR}/tensor_control.nii.gz --mask ${MASK} -fa ${OUTDIR}/fa_control.nii.gz -adc ${OUTDIR}/md_control.nii.gz -rd ${OUTDIR}/rd_control.nii.gz -ad ${OUTDIR}/ad_control.nii.gz -force
tensor2metric ${OUTDIR}/tensor_rish_norm.nii.gz --mask ${MASK} -fa ${OUTDIR}/fa_rish_norm.nii.gz -adc ${OUTDIR}/md_rish_norm.nii.gz -rd ${OUTDIR}/rd_rish_norm.nii.gz -ad ${OUTDIR}/ad_rish_norm.nii.gz  -force
tensor2metric ${OUTDIR}/tensor_mid_norm.nii.gz --mask ${MASK} -fa ${OUTDIR}/fa_mid_norm.nii.gz -adc ${OUTDIR}/md_mid_norm.nii.gz -rd ${OUTDIR}/rd_mid_norm.nii.gz -ad ${OUTDIR}/ad_mid_norm.nii.gz  -force
