import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Background Remover", layout="centered")

st.title("🖼️ Background Remover App")
st.write("Upload an image, and we'll remove its background for you!")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("Removing background..."):
        # Convert image to bytes
        input_bytes = io.BytesIO()
        image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()

        # Remove background
        output_bytes = remove(input_bytes)
        output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    st.image(output_image, caption="Image without Background", use_column_width=True)
    
    # Download button
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    st.download_button(
        label="📥 Download Image",
        data=output_buffer.getvalue(),
        file_name="no_background.png",
        mime="image/png"
    )
