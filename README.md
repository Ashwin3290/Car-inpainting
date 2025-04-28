# Car Color Studio

A professional-grade application for virtually recoloring car images with AI-powered precision.

## Features

- **Smart Color Transform**: Advanced AI-powered car recoloring with intelligent mask generation
- **Real-time Preview**: See changes instantly with our advanced preview system
- **Professional Results**: High-quality output suitable for professional use
- **User-Friendly Interface**: Intuitive Next.js interface with modern design
- **Color Customization**: Choose from preset colors or create your own custom color
- **Processing History**: Track and revisit your previous transformations

## Project Structure

This project consists of two main components:

- **Backend**: FastAPI application that handles image processing, analysis, and recoloring
- **Frontend**: Next.js application that provides the user interface

The system also uses an external AI masking service API to generate precise car masks.

## Tech Stack

### Backend
- FastAPI (Python web framework)
- OpenCV for image processing
- scikit-learn for color analysis
- Python 3.11+

### Frontend
- Next.js 14 with TypeScript
- React Query for data fetching
- Tailwind CSS for styling
- React Colorful for color selection

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Docker (optional)

### Setup and Installation

#### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

#### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

### Using Docker

You can also run the entire application using Docker Compose:

```bash
docker-compose up
```

This will start both the backend and frontend services.

## Architecture

### Backend Components

- **FastAPI Application**: Main web server that handles HTTP requests
- **Car Recolor Service**: Core service that orchestrates the recoloring process
- **Color Analysis**: Smart color transformation algorithms
- **External Masking API**: AI-powered service for generating car masks

### Frontend Components

- **Studio Page**: Main workspace for uploading and recoloring images
- **Color Selector**: UI for choosing colors with various methods
- **Image Uploader**: Component for uploading car images
- **History Page**: View and manage previous transformations

## Development

### Adding New Features

1. **Backend**:
   - Add new routes in `/app/api/routes/`
   - Implement new services in `/app/services/`
   - Update API documentation

2. **Frontend**:
   - Add new components in `/components/`
   - Create new pages in `/app/`
   - Update API client in `/lib/api/`

### Testing

- Backend: Use pytest for unit and integration tests
- Frontend: Use Jest and React Testing Library

## Deployment

### Backend

The backend can be deployed to any cloud provider that supports Docker containers:

1. Build the Docker image:
   ```bash
   docker build -t car-color-studio-backend ./backend
   ```

2. Deploy to your preferred cloud service (AWS, Google Cloud, Azure)

### Frontend

The Next.js frontend can be easily deployed to Vercel:

1. Push your code to a GitHub repository
2. Connect the repository to Vercel
3. Configure environment variables
4. Deploy

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
