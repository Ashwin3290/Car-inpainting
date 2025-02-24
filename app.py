import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_card import card
from PIL import Image
from datetime import datetime
from car_recolor_service import CarRecolorService
import io

# Configure page
st.set_page_config(
    page_title="Car Color Studio",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)
if 'recolor_service' not in st.session_state:
    st.session_state.recolor_service = CarRecolorService(
        base_dir="images",
        api_url="https://da6d-34-34-25-54.ngrok-free.app/"
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
        "settings": settings,
        "uuid": st.session_state.current_uuid  # Add the UUID to history
    }
    st.session_state.history.append(history_entry)

def main():
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
        
        # # Project info in sidebar
        # st.markdown("### About")
        # st.info(
        #     """
        #     🚗 Car Color Studio Pro
            
        #     Version: 1.0.0
        #     Last Updated: 2024-01-15
        #     """
        # )

    if selected == "Home":
        st.markdown('<h1 class="main-header">Car Color Studio</h1>', unsafe_allow_html=True)
        
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
                type=["jpg", "jpeg", "png","jiff"],
                help="Drag and drop or click to upload"
            )

        if uploaded_file is not None:
            # Check if this is a new file
            file_bytes = uploaded_file.getvalue()
            if 'current_image_hash' not in st.session_state or \
            st.session_state.current_image_hash != hash(file_bytes):
                # New image uploaded
                st.session_state.current_image_hash = hash(file_bytes)
                current_uuid = st.session_state.recolor_service.process_new_image(file_bytes,uploaded_file.name)
                st.session_state.current_uuid = current_uuid
            st.image(uploaded_file, caption="Original Image", use_container_width=False)

            # Show processing status
            status = st.session_state.recolor_service.get_processing_status()
            if not status['analysis_complete']:
                st.info("Processing image... Please wait.")
            

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

            # # Advanced Settings in an organized expander
            # with st.expander("Advanced Settings", expanded=False):
            #     settings_tabs = st.tabs(["Processing", "Effects", "Quality"])
                
            #     with settings_tabs[0]:
            #         preserve_luminance = st.toggle(
            #             "Preserve Original Luminance",
            #             value=True
            #         )
            #         reflection_threshold = st.slider(
            #             "Reflection Threshold",
            #             150, 250, 200
            #         )

            #     with settings_tabs[1]:
            #         gloss_level = st.slider(
            #             "Gloss Level",
            #             0, 100, 50
            #         )
            #         metallic_effect = st.slider(
            #             "Metallic Effect",
            #             0, 100, 0
            #         )

            #     with settings_tabs[2]:
            #         output_quality = st.select_slider(
            #             "Output Quality",
            #             options=["Draft", "Standard", "High", "Ultra"]
            #         )

            # Process button
        if st.button("Transform Color", use_container_width=True):
            if uploaded_file:
                # Convert the selected color to BGR format
                # This example assumes selected_color is in hex format (#RRGGBB)
                color = selected_color.lstrip('#')
                rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
                
                with st.spinner("Transforming color..."):
                    result = st.session_state.recolor_service.recolor_current_image(
                        target_color=rgb,
                        wait_timeout=90,
                    )
                    
                    if result['success']:
                        st.session_state.recolored_image = None
                        st.success("Transformation complete!")
                        # Display the recolored image
                        recolored_image = Image.open(result['image_path'])
                        st.session_state.recolored_image = recolored_image

            if 'recolored_image' in st.session_state:
                if st.session_state.recolored_image:
                    st.image(st.session_state.recolored_image , caption="Recolored Image", use_container_width=False)
                    # if st.button("Download", use_container_width=True):
                    #     recolored_image.save(f"{uploaded_file.name}_recolored.png")
                    #     with open("recolored_image.png", "rb") as file:
                    #         st.download_button(file,f"{uploaded_file.name}_recolored.png", "Download Recolored Image")
                            
                            # Save to history
                    save_history(
                        original_image=uploaded_file,
                        recolored_image=recolored_image,
                        color=selected_color,
                        settings={
                        #     'preserve_luminance': preserve_luminance,
                        #     'reflection_threshold': reflection_threshold,
                        #     'gloss_level': gloss_level,
                        #     'metallic_effect': metallic_effect,
                        #     'output_quality': output_quality
                        }
                    )
                else:
                    st.error(f"Error: {result['message']}")
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
                        # Convert PIL Image to bytes for download
                        img_bytes = io.BytesIO()
                        entry["recolored_image"].save(img_bytes, format='PNG')
                        
                        st.download_button(
                            label="Download Recolored Image",
                            data=img_bytes.getvalue(),
                            file_name="recolored_image.png",
                            mime="image/png",
                            key=f"download_{entry['timestamp']}"
                        )
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