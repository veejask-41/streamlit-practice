import streamlit as st
import nibabel as nib
import tempfile
import os
import time
from itertools import cycle

st.title('MRI Enhance 3D')

input_image = st.file_uploader(
    "Upload MRI scan nifti file", accept_multiple_files=False, type=['nii', 'nii.gz']
)

if st.button('Generate', use_container_width=True):
    if input_image:
        with st.spinner('Processing...'):
            time.sleep(3)
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, input_image.name)
            with open(path, "wb") as f:
                f.write(input_image.getbuffer())
            input_mri = nib.load(path)
            # st.write('pixel dimensions : ' + str(input_mri.header['pixdim']))
            # st.write('data shape : ' + str(input_mri.header['dim']))
            # st.write('affine matrix : ' + str(input_mri.affine))
            input_mri_data = input_mri.get_fdata()
            input_mri_shape = input_mri_data.shape
            slice_0 = input_mri_data[input_mri_shape[0]//2, :, :]/input_mri_data.max()
            slice_1 = input_mri_data[:, input_mri_shape[1]//2, :]/input_mri_data.max()
            slice_2 = input_mri_data[:, :, input_mri_shape[2]//2]/input_mri_data.max()
            slices = [slice_0, slice_1, slice_2]
            
            # st.image(slices, width=150, clamp=True, channels='gray', use_column_width=True)

            cols = cycle(st.columns(3)) # st.columns here since it is out of beta at the time I'm writing this
            for idx, slice in enumerate(slices):
                next(cols).image(slice, width=150)

            with open(path, 'rb') as f:
                data = f.read()
                st.download_button(
                    'Download', data, input_image.name, mime="application/octet-stream ", use_container_width=True)


