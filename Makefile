VENV=venv
FLASK_APP=app.py


# Install dependencies
install:
    # Install required packages from requirements.txt
    python -m pip install -r requirements.txt


# Run the Flask application
run:
    # Activate the virtual environment and run the Flask app
    .\$(VENV)\Scripts\activate && flask run --port 3000


# Clean up virtual environment
clean:
    # Clean up virtual environment
    rmdir /S /Q $(VENV)


# Reinstall all dependencies
reinstall: clean install



