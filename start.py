import subprocess
import sys
import time

def main():
    print("🚀 Starting Focus AI News Command Center...")
    print("===========================================")
    
    # Commands to run
    fastapi_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"]
    celery_cmd = [sys.executable, "-m", "celery", "-A", "app.workers.celery_app", "worker", "--loglevel=info", "-P", "solo"]
    streamlit_cmd = [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.headless", "true"]
    
    processes = []
    
    try:
        print("[1/3] Starting FastAPI Backend (Port 8000)...")
        p_fastapi = subprocess.Popen(fastapi_cmd)
        processes.append(p_fastapi)
        
        print("[2/3] Starting Celery Worker...")
        p_celery = subprocess.Popen(celery_cmd)
        processes.append(p_celery)
        
        # Give backend a moment to start before launching frontend
        time.sleep(2)
        
        print("[3/3] Starting Streamlit Studio (Port 8501)...")
        p_streamlit = subprocess.Popen(streamlit_cmd)
        processes.append(p_streamlit)
        
        print("\n✅ All services running! Access the studio at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop all services.\n")
        
        # Wait for any process to complete (blocks here)
        for p in processes:
            p.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        for p in processes:
            try:
                p.terminate()
            except Exception:
                pass
        for p in processes:
            p.wait()
        print("✅ Shutdown complete.")

if __name__ == "__main__":
    main()
