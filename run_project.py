import os
import sys
import subprocess
import time
import signal
import atexit

processes = []

def kill_process_tree(proc):
    """Recursively kills process tree on Windows/Unix."""
    if proc is None or proc.poll() is not None:
        return
    try:
        if os.name == 'nt':
            # Windows process tree kill
            subprocess.call(f"taskkill /F /T /PID {proc.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc.terminate()
            proc.wait(timeout=2)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

def cleanup_all_processes():
    """Guarantees all child processes (FastAPI, LangGraph, React Frontend) are stopped on exit."""
    if not processes:
        return
    print("\n[Shutting Down]: Terminating all background server processes cleanly...")
    for name, proc in processes:
        print(f"  - Stopping {name} (PID: {proc.pid if proc else 'N/A'})...")
        kill_process_tree(proc)
    print("[Shutting Down]: All background processes terminated.")

# Register cleanup handler for exit, SIGINT, SIGTERM
atexit.register(cleanup_all_processes)

def signal_handler(sig, frame):
    cleanup_all_processes()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    print("==================================================================")
    print("  Starting Interview Preparation Assistant Multi-Agent System    ")
    print("==================================================================")
    
    # Set UTF-8 encoding environment variable
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    # Read ports from environment variables
    backend_port = os.getenv("BACKEND_PORT", "8000")
    frontend_port = os.getenv("FRONTEND_PORT", "5173")
    langgraph_port = os.getenv("LANGGRAPH_PORT", "2024")
    
    try:
        # 1. Start FastAPI Backend Server
        print(f"\n[1/3] Launching FastAPI Backend Server (http://localhost:{backend_port}/docs)...")
        backend_cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload", "--port", str(backend_port)]
        backend_proc = subprocess.Popen(backend_cmd, env=env)
        processes.append(("FastAPI Backend", backend_proc))
        time.sleep(2)
        
        # 2. Start LangGraph Studio Dev Server
        print(f"[2/3] Launching LangGraph Studio Visual Server (http://127.0.0.1:{langgraph_port})...")
        langgraph_cmd = f"langgraph dev --port {langgraph_port} --no-browser"
        langgraph_proc = subprocess.Popen(langgraph_cmd, shell=True, env=env)
        processes.append(("LangGraph Studio", langgraph_proc))
        time.sleep(2)
        
        # 3. Start React Frontend Server
        print(f"[3/3] Launching React Frontend App (http://localhost:{frontend_port})...")
        frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
        frontend_cmd = "npm run dev"
        frontend_proc = subprocess.Popen(frontend_cmd, cwd=frontend_dir, shell=True, env=env)
        processes.append(("React Frontend", frontend_proc))
        
        print("\n==================================================================")
        print("  ALL SERVICES ARE LIVE AND RUNNING!                             ")
        print("==================================================================")
        print(f"  - React Frontend:    http://localhost:{frontend_port}")
        print(f"  - FastAPI API Docs:  http://localhost:{backend_port}/docs")
        print(f"  - LangGraph Studio:  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:{langgraph_port}")
        print("  - LangSmith Tracing: https://smith.langchain.com")
        print("==================================================================")
        print("  Press Ctrl+C in this terminal to stop all running services.")
        print("==================================================================\n")
        
        # Keep master process alive and monitor subprocesses cleanly
        notified = set()
        while True:
            time.sleep(2)
            for name, proc in processes:
                if proc.poll() is not None and name not in notified:
                    print(f"[Notice]: Process '{name}' stopped with exit code {proc.poll()}")
                    notified.add(name)
                    
    except KeyboardInterrupt:
        cleanup_all_processes()
        sys.exit(0)

if __name__ == "__main__":
    main()
