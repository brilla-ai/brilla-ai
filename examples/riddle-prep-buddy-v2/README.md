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

1. **Access to Server notebook:**

    Open the `Riddle_Prep_App_Server.ipynb` file, preferably in Colab if you don't have a GPU on your system, follow the instructions to start the server, and copy the `ngrok` URL.

    You may also find the same notebook via this link: `https://colab.research.google.com/drive/1staK1vtcI9ZMont9rxazCPn8E1nm1R5c?usp=sharing`

2. **Running the Server:**
    a. You will first of all need access to the TTS model. This is only accessible to AfricaAIED Hackathon participants.
    b. Request for access to TTS model here: `https://drive.google.com/drive/folders/1xfb5fmPVXladn6QiTSP-rK5JIAxnvuPJ?usp=drive_link`
    c. Once access has been granted, create a shortcut of the 'AfricaAIED-Hackathon' folder and place it in your root Googe Drive directory (My Drive).
    d. Connect to a GPU runtime on Colab (minimum T4).
    e. Follow the instructions in the notebook and execute the cells.
    f. Remember to have your ngrok URL handy.

3. **Update `app.py`:**

    Paste the `ngrok` URL into the `BASE_URL` variable at the top of the `app.py` file.

4. **Run `app.py`:**

    ```bash
    python app.py
    ```
