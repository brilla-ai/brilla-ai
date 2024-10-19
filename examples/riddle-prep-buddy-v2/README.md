# Brilla-AI Riddle Prep Buddy - V2

A small tkinter application students can use to practice for the riddles section of the NSMQ.

## Installation and Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/brill-ai/brill-ai.git
    cd your-repo-name
    ```

2. **Create a Virtual Environment:**

    First, cd into the project directory: 
    ```bash
    cd riddle-prep-buddy-v2
    ```

    On macOS and Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the Server Notebook:**

    Open the `[Release] Riddle Prep App Server.ipynb` file, preferably in Colab if you don't have a GPU on your, follow the instructions to start the server, and copy the `ngrok` URL.

2. **Update `app.py`:**

    Paste the `ngrok` URL into the `BASE_URL` variable at the top of the `app.py` file.

3. **Run `app.py`:**

    ```bash
    python app.py
    ```
