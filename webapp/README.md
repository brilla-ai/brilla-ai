
# Brilla AI web application

This repository contains both the frontend and backend for the Brilla web application. The frontend is developed using the [Next.js](https://nextjs.org/) framework, while the backend is built with [FastAPI](https://fastapi.tiangolo.com/) and requires a PostgreSQL database.

## Project Structure

- **brilla-frontend/** - The frontend codebase (Next.js).
- **backend/** - The backend codebase (FastAPI).
- **webapp/** - Main folder containing both frontend and backend projects.

## Getting Started

### Prerequisites

- **Node.js** (for the frontend)
- **Python 3.8+** (for the backend)
- **PostgreSQL** (for the database)

### Cloning the Repository

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Change directory into the \`webapp\` folder:

   ```bash
   cd webapp
   ```

---

## Frontend Setup (Next.js)

### Steps to Run the Frontend

1. Navigate to the \`brilla-frontend\` folder:

   ```bash
   cd brilla-frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Create a \`.env\` file in the \`brilla-frontend\` folder with the following environment variables:

   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_WS_BASE_URL=ws://localhost:8000/websocket/ws
   ```

4. Start the development server:

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`.

---

## Backend Setup (FastAPI)

### Prerequisites

- **PostgreSQL** must be running locally.

### Steps to Run the Backend

1. Navigate to the \`backend\` folder:

   ```bash
   cd backend
   ```

2. Ensure PostgreSQL is running.

3. Install the backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a \`.env.dev\` file in the \`backend\` folder with the following content:

   ```
   DATABASE_URL_VALUE='postgresql+psycopg2://username:password@localhost:5432/brillaai'
   DEBUG=True
   ML_API_URL=<your-ml-api-url>
   ```

5. Start the FastAPI server for development:

   ```bash
   uvicorn main:app --reload
   ```

   The backend will be available at `http://localhost:8000`.

---

### Notes

- Be sure to update the `.env` files with your own configuration values.
- The backend requires a PostgreSQL database connection, so ensure your local environment is correctly set up.

