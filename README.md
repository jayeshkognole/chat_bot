# Running the application locally

## Prerequisites

*   Python 3.9 or higher
*   Node.js 16 or higher
*   npm

## Gemini API Key

1.  Obtain a Gemini API key from [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey).
2.  Add the Gemini API key to the `config.ini` file in the `api-server` directory.

    ```ini
    [gemini]
    api_key = YOUR_GEMINI_API_KEY
    ```

## Installation

### Backend

1.  Navigate to the `api-server` directory.

    ```bash
    cd api-server
    ```

2.  Create a virtual environment.

    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment.

    ```bash
    venv\Scripts\activate   # Windows
    source venv/bin/activate  # macOS and Linux
    ```

4.  Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```

### Frontend

1.  Navigate to the `ui-server` directory.

    ```bash
    cd ui-server
    ```

2.  Install the dependencies.

    ```bash
    npm install
    ```

## Running the application

### Backend

1.  Navigate to the `api-server` directory.

    ```bash
    cd api-server
    ```

2.  Run the backend application.

    ```bash
    python app.py
    ```

### Frontend

1.  Navigate to the `ui-server` directory.

    ```bash
    cd ui-server
    ```

2.  Run the frontend application.

    ```bash
    npm start
    ```

The frontend will be available at `http://localhost:3000`.
The backend will be available at `http://localhost:5000`.

## Docker and Google Cloud Deployment

This project includes files for Docker and Google Cloud deployment:

*   `Dockerfile` in the `api-server` directory for the backend.
*   `Dockerfile` in the `ui-server` directory for the frontend.
*   `docker-compose.yml` for running both services locally with Docker Compose.
*   `deploy.sh` for deploying both services to Google Cloud Run.
