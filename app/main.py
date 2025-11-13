import subprocess
import threading
import time

from dotenv import load_dotenv

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend server...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "0.0.0.0", "--port", "8000"], check=True)
    
    except CustomException as ce:
        logger.error(f"Custom exception in backend: {ce}")
        raise CustomException("Failed to start backend server.", ce)
    

def run_frontend():
    try:
        logger.info("Starting frontend server...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py", "--server.port=8501"], check=True)
    
    except CustomException as ce:
        logger.error(f"Custom exception in frontend: {ce}")
        raise CustomException("Failed to start frontend server.", ce)
    

if __name__ == "__main__":
    try:
        threading.Thread(target=run_backend).start()
        time.sleep(2)
        run_frontend()
    
    except CustomException as e:
        logger.exception(f"Custom exception occurred: {str(e)}")



