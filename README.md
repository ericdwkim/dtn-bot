### Web Bot - DTN Filing 
**Using Conda:**

1. Open a command-line interface (such as Anaconda Prompt or Terminal).
2. Navigate to the directory where your `requirements.txt` file is located:
   ```bash
   cd path/to/directory
   ```
3. Create a new conda environment (optional but recommended for isolation):
   ```bash
   conda create --name myenv
   ```
4. Activate the conda environment:
   ```bash
   conda activate myenv
   ```
5. Install the packages from `requirements.txt`:
   ```bash
   conda install --file requirements.txt
   ```

**Using venv (Python's built-in virtual environment module):**

1. Open a command-line interface (such as Terminal or Command Prompt).
2. Navigate to the directory where your `requirements.txt` file is located:
   ```bash
   cd path/to/directory
   ```
3. Create a new virtual environment:
   ```bash
   python -m venv myenv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```
5. Install the packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

Feel free to replace `myenv` with the desired name for your environment.

