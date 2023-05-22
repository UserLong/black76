# Overview

This project is based on FastAPI and sqlalchemy. Conda virtual environment is used too.

## Steps

### Build local environment

1. Install Python 3.8+;
2. Install Anaconda or Miniconda;
3. Copy the project to a folder;
4. Create a virtual environment in the projects folder: 
   `cd <dummy-folder>` (replace dummy-folder with your directory),
   then `conda env create -f environment.yml`.

### Start API
1. Activate virtual environment: `conda activate shell_env`;
2. Create database: `python src\setup_db.py`;
3. CD into src folder and kick off the server: `uvicorn main:app --reload`;
4. The server is running on http://127.0.0.1:8000/;
5. The API documentations is available at http://127.0.0.1:8000/docs#/.

### Run unit tests

1. CD into the tests folder, then run tests by using command `pytest` in the command line console.
