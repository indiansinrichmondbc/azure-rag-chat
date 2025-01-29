@echo off
REM Activate the virtual environment
call .venv\Scripts\activate

REM Run Streamlit
streamlit run app.py
