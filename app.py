import streamlit as st
from PIL import Image
import io
from SteganoForApp import encode_image, decode_image


# Configure the app
st.set_page_config(page_title="Steganography Tool", layout="wide")
st.title("🔐 Image Steganography Tool")
st.markdown("""
    📩Hide secret messages in images 
""")
st.markdown("""
    📧Extract hidden messages .
""")
st.markdown("""
    ℹ️*For best results, use PNG images.*
""")

# Sidebar with mode selection
with st.sidebar:
    st.title("Settings🪄")
    mode = st.radio(
        "Select mode:",
        ["Encode (Hide Message)", "Decode (Extract Message)"],
        index=0
    )

# Main content area
uploaded_file = st.file_uploader(
    "Upload an image (PNG recommended):",
    type=["png", "jpg", "jpeg"],
    key="file_uploader"
)

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)  # Fixed deprecation warning

        if mode == "Encode (Hide Message)":
            st.subheader("Encode Message")
            secret_message = st.text_area(
                "Enter your secret message:",
                height=100,
                placeholder="Type your message here..."
            )
            
            if st.button("Encode Message", type="primary"):
                with st.spinner("Encoding message..."):
                    try:
                        encoded_image = encode_image(image.copy(), secret_message)
                        st.success("Message successfully encoded!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(encoded_image, caption="Encoded Image", use_container_width=True)  # Fixed
                        with col2:
                            buf = io.BytesIO()
                            encoded_image.save(buf, format="PNG")
                            st.download_button(
                                label="Download Encoded Image",
                                data=buf.getvalue(),
                                file_name="secret_image.png",
                                mime="image/png"
                            )
                    except ValueError as e:
                        st.error(f"Error: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")

        else:  # Decode mode
            st.subheader("Decode Message")
            if st.button("Decode Message", type="primary"):
                with st.spinner("Extracting message..."):
                    try:
                        hidden_text = decode_image(image.copy())
                        if hidden_text:
                            st.success("Hidden message found!")
                            st.text_area(
                                "Decoded Message",
                                value=hidden_text,
                                height=100,
                                disabled=True,
                                key="decoded_message"
                            )
                        else:
                            st.warning("No hidden message found in this image.")
                    except Exception as e:
                        st.error(f"Error during decoding: {str(e)}")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
else:
    st.info("Please upload an image to get started.")

# Footer
st.markdown("---")
st.caption("Image Steganography Tool | Created By Avinash Anand")