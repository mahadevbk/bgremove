import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Dev's Background Remover", layout="centered")
st.title("🖼️ Dev's Background Remover")
st.write("Upload an image and tune the background removal settings for better results.")

# Upload image
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.subheader("📷 Original Image")
    st.image(image, use_container_width=True)

    st.sidebar.header("🛠️ Removal Settings")

    # Toggle alpha matting
    use_alpha_matting = st.sidebar.checkbox("Use Alpha Matting", value=False)
    st.sidebar.caption(
        "Alpha matting improves edge quality, especially for hair or soft objects, but takes more time."
    )

    if use_alpha_matting:
        foreground_threshold = st.sidebar.slider(
            "Foreground Threshold", 0, 255, 240
        )
        st.sidebar.caption(
            "Pixels brighter than this are assumed to be definite foreground (e.g., skin, clothes)."
        )

        background_threshold = st.sidebar.slider(
            "Background Threshold", 0, 255, 10
        )
        st.sidebar.caption(
            "Pixels darker than this are assumed to be background (e.g., shadows, black clothing)."
        )

        erode_size = st.sidebar.slider(
            "Erode Size", 0, 20, 10
        )
        st.sidebar.caption(
            "Removes thin edges from the mask. Helps clean up borders around the subject."
        )
    else:
        foreground_threshold = 240
        background_threshold = 10
        erode_size = 10

    post_process_mask = st.sidebar.checkbox("Post-process Mask", value=False)
    st.sidebar.caption(
        "Applies slight cleanup to reduce noise and improve edge smoothness."
    )

    with st.spinner("Removing background..."):
        input_bytes = io.BytesIO()
        image.save(input_bytes, format="PNG")
        input_bytes = input_bytes.getvalue()

        output_bytes = remove(
            input_bytes,
            alpha_matting=use_alpha_matting,
            alpha_matting_foreground_threshold=foreground_threshold,
            alpha_matting_background_threshold=background_threshold,
            alpha_matting_erode_size=erode_size,
            post_process_mask=post_process_mask
        )

        output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    st.subheader("🎯 Image with Background Removed")
    st.image(output_image, use_container_width=True)

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

st.info("Built with ❤️ using [Streamlit](https://streamlit.io/) — free and open source. [Other Scripts by dev](https://devs-scripts.streamlit.app/) on Streamlit.")
