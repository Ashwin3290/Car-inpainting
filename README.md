#  Car Color Studio

A professional-grade application for virtually recoloring car images with AI-powered precision.

![Car Recolor Sample](assets/image)

##  Features

- **Smart Color Transform**: Advanced AI-powered car recoloring with intelligent mask generation
- **Real-time Preview**: See changes instantly with our advanced preview system
- **Professional Results**: High-quality output suitable for professional use
- **User-Friendly Interface**: Intuitive Streamlit-based UI with modern design
- **Color Customization**: Choose from preset colors or create your own custom color
- **Processing History**: Track and revisit your previous transformations

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/car-color-studio.git
   cd car-color-studio
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the masking server:
   - The application uses a masking server to generate car masks
   - Run the masking server in a separate process:
   ```bash
   python -m masking_server
   ```
   - Note: For best results, run the masking server on a machine with GPU support

4. Run the application:
   ```bash
   streamlit run app.py
   ```

##  Architecture

The project consists of several key components:

1. **Streamlit UI (`app.py`)**: The main user interface built with Streamlit
2. **Car Recolor Service (`car_recolor_service.py`)**: Core service that manages the recoloring process
3. **Recolor Engine (`recolor.py`)**: Handles the color transformation algorithms
4. **Masking Server (`masking_server.ipynb`)**: AI-powered service for generating car masks

### How It Works

1. The user uploads a car image through the Streamlit interface
2. The image is sent to the masking server which identifies the car and generates a mask
3. The recolor engine analyzes the car's color properties
4. The user selects a target color
5. The recolor engine transforms the car to the new color while preserving lighting, reflections, and details
6. The result is displayed and can be downloaded by the user

##  Color Transformation Process

Our color transformation technique uses a sophisticated approach that:

1. Analyzes the car's original color patterns using K-means clustering
2. Identifies the dominant color and brightness patterns
3. Intelligently remaps colors while preserving lighting and reflections
4. Handles special cases like dark cars, extremely bright or dark target colors
5. Preserves the original image's details and texture

##  AI Mask Generation

The mask generation system uses a combination of advanced computer vision techniques:

- Grounding DINO for zero-shot object detection
- Segment Anything Model (SAM) for precise segmentation
- Custom-trained car part detection model
- Intelligent filtering of unpaintable areas (windows, lights, grille, etc.)

##  Project Structure

```
├── app.py                   # Main Streamlit application
├── car_recolor_service.py   # Service for handling recoloring requests
├── recolor.py               # Core recoloring algorithm
├── masking_server.ipynb     # Notebook for running the mask generation server
├── requirements.txt         # Python dependencies
├── images/                  # Directory for storing images
│   ├── processed/           # Original uploaded images
│   ├── masks/               # Generated car masks
│   ├── analyses/            # Color analysis data
│   └── output/              # Final recolored images
└── assets/                  # Static assets for the application
```

##  Advanced Configuration

You can customize the application behavior by modifying:

- Base directory for image storage
- API URL for the masking server
- Color preset options
- Analysis parameters in the recolor engine
