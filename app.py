import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.switch_page_button import switch_page
from streamlit_card import card
from streamlit_image_comparison import image_comparison
import cv2
import numpy as np
from pathlib import Path
import tempfile
from PIL import Image
import io
from datetime import datetime
import json
import time
# Configure page
st.set_page_config(
    page_title="Car Color Studio Pro",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f0f2f6 0%, #ffffff 100%);
    }
    .main-header {
        font-size: 3rem !important;
        font-weight: 700;
        background: linear-gradient(45deg, #1e3799, #0c2461);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stButton>button {
        background: linear-gradient(45deg, #1e3799, #0c2461);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def save_history(original_image, recolored_image, color, settings):
    """Save processing history to session state"""
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_entry = {
        "timestamp": timestamp,
        "original_image": original_image,
        "recolored_image": recolored_image,
        "color": color,
        "settings": settings
    }
    st.session_state.history.append(history_entry)

def main():
    transformed_img = Image.open("D:/Car-inpainting/assets/car_recolored.png")
    if "transformed_image" not in st.session_state:
        st.session_state.transformed_image = False
    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Home", "Color Studio", "History", "Settings", "Help"],
            icons=["house", "palette", "clock-history", "gear", "question-circle"],
            menu_icon="cast",
            default_index=0,
        )
        
        add_vertical_space(2)
        
        # Project info in sidebar
        st.markdown("### About")
        st.info(
            """
            🚗 Car Color Studio Pro
            
            Version: 1.0.0
            Last Updated: 2024-01-15
            """
        )

    if selected == "Home":
        st.markdown('<h1 class="main-header">Car Color Studio Pro</h1>', unsafe_allow_html=True)
        
        # Feature cards using streamlit_card
        col1, col2, col3 = st.columns(3)
        
        with col1:
            card(
                title="Smart Color Transform",
                text="Advanced AI-powered car recoloring with intelligent mask generation",
                image="https://via.placeholder.com/300x200",
                url=None
            )
        
        with col2:
            card(
                title="Real-time Preview",
                text="See changes instantly with our advanced preview system",
                image="https://via.placeholder.com/300x200",
                url=None
            )
            
        with col3:
            card(
                title="Professional Results",
                text="High-quality output suitable for professional use",
                image="https://via.placeholder.com/300x200",
                url=None
            )

    elif selected == "Color Studio":
        colored_header(
            label="Color Studio",
            description="Transform your car's appearance with professional-grade recoloring",
            color_name="blue-70"
        )

        # Main processing interface
        col1, col2 = st.columns([3, 2])

        with col1:
            # Image upload with drag and drop
            uploaded_file = st.file_uploader(
                "Upload Car Image",
                type=["jpg", "jpeg", "png"],
                help="Drag and drop or click to upload"
            )

            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Original Image", use_container_width=True)

            

        with col2:
            # Advanced color selection
            st.markdown("### Color Configuration")
            
            color_mode = st.radio(
                "Select Color Mode",
                ["Preset Colors", "Custom Color", "Color Palette"]
            )

            if color_mode == "Preset Colors":
                color_presets = {
                    "Midnight Black": "#000000",
                    "Arctic White": "#FFFFFF",
                    "Racing Red": "#FF0000",
                    "Ocean Blue": "#0000FF",
                    "Forest Green": "#008000",
                    "Sunset Orange": "#FFA500",
                    "Royal Purple": "#800080",
                }
                selected_preset = st.selectbox(
                    "Choose a preset color",
                    list(color_presets.keys())
                )
                selected_color = color_presets[selected_preset]

            elif color_mode == "Custom Color":
                selected_color = st.color_picker(
                    "Pick a custom color",
                    "#0000FF"
                )

            else:  # Color Palette
                st.markdown("Generate harmonious color combinations")
                base_color = st.color_picker("Base Color", "#0000FF")
                st.markdown("### Generated Palette")
                # Here you could add code to generate color palettes

            # Advanced Settings in an organized expander
            with st.expander("Advanced Settings", expanded=False):
                settings_tabs = st.tabs(["Processing", "Effects", "Quality"])
                
                with settings_tabs[0]:
                    preserve_luminance = st.toggle(
                        "Preserve Original Luminance",
                        value=True
                    )
                    reflection_threshold = st.slider(
                        "Reflection Threshold",
                        150, 250, 200
                    )

                with settings_tabs[1]:
                    gloss_level = st.slider(
                        "Gloss Level",
                        0, 100, 50
                    )
                    metallic_effect = st.slider(
                        "Metallic Effect",
                        0, 100, 0
                    )

                with settings_tabs[2]:
                    output_quality = st.select_slider(
                        "Output Quality",
                        options=["Draft", "Standard", "High", "Ultra"]
                    )

            # Process button
            if st.button("Transform Color", use_container_width=True):
                if uploaded_file:
                    with st.spinner("Processing your image..."):
                        time.sleep(40) # Simulating the processing time
                        with col1:
                            st.image(transformed_img, caption="Transformed Image", use_container_width=True)
                        st.success("Transformation complete!")
                else:
                    st.warning("Please upload an image first")

    elif selected == "History":
        colored_header(
            label="Processing History",
            description="View and compare your previous transformations",
            color_name="blue-70"
        )

        if 'history' in st.session_state and st.session_state.history:
            for entry in st.session_state.history:
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(entry["original_image"], caption="Original")
                    with col2:
                        st.image(entry["recolored_image"], caption="Recolored")
                    st.markdown(f"**Processed at:** {entry['timestamp']}")
                    st.divider()
        else:
            st.info("No processing history available yet")

    elif selected == "Settings":
        colored_header(
            label="Settings",
            description="Configure your workspace preferences",
            color_name="blue-70"
        )
        
        # Settings interface
        st.markdown("### Application Settings")
        
        tabs = st.tabs(["General", "Processing", "Storage"])
        
        with tabs[0]:
            st.toggle("Dark Mode", value=False)
            st.toggle("Auto-save Results", value=True)
            st.number_input("Max History Items", min_value=5, max_value=50, value=10)

        with tabs[1]:
            st.selectbox(
                "Default Color Mode",
                ["Preset Colors", "Custom Color", "Color Palette"]
            )
            st.selectbox(
                "Default Quality",
                ["Draft", "Standard", "High", "Ultra"]
            )

        with tabs[2]:
            st.text_input("Export Directory", value="./exports")
            st.toggle("Compress History", value=True)
            if st.button("Clear History"):
                if 'history' in st.session_state:
                    st.session_state.history = []
                st.success("History cleared successfully")

    else:  # Help section
        colored_header(
            label="Help & Documentation",
            description="Learn how to use Car Color Studio Pro",
            color_name="blue-70"
        )
        
        st.markdown("""
        ### Quick Start Guide
        
        1. **Upload Your Image**
           - Click the upload button or drag and drop your image
           - Supported formats: JPG, JPEG, PNG
        
        2. **Choose Your Color**
           - Select from preset colors
           - Use the color picker for custom colors
           - Try the color palette generator
        
        3. **Adjust Settings**
           - Fine-tune processing parameters
           - Adjust quality settings
           - Configure special effects
        
        4. **Process and Save**
           - Click 'Transform Color' to process
           - Download your result
           - View history anytime
        """)

        # FAQ Section
        st.markdown("### Frequently Asked Questions")
        with st.expander("What image formats are supported?"):
            st.write("We support JPG, JPEG, and PNG formats.")

        with st.expander("How do I get the best results?"):
            st.write("For best results, use high-quality images in good lighting...")

        with st.expander("Can I batch process multiple images?"):
            st.write("Batch processing is coming in a future update...")

if __name__ == "__main__":
    main()