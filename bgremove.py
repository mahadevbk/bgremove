's import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Background Remover", layout="centered")
st.title("🖼️ Background Remover")
st.write("Upload an image and download it with the background removed (PNG with transparency).")

# Upload image
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.subheader("📷 Original Image")
    st.image(image, use_container_width=True)

    with st.spinner("Removing background..."):
        # Convert to bytes
        input_bytes = io.BytesIO()
        image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()

        # Remove background
        output_bytes = remove(input_bytes)
        output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    st.subheader("🎯 Image with Background Removed")
    st.image(output_image, use_container_width=True)

    # Download button
    download_buffer = io.BytesIO()
    output_image.save(download_buffer, format="PNG")
    st.download_button(
        label="📥 Download PNG",
        data=download_buffer.getvalue(),
        file_name="no_background.png",
        mime="image/png"
    )
else:
    st.info("Please upload an image file to begin.")
