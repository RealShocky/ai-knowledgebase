import os
import subprocess
import sys

def setup_backend():
    print("Setting up backend...")
    
    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "backend/venv"], check=True)
    
    # Activate virtual environment and install requirements
    if os.name == 'nt':  # Windows
        activate_script = "backend/venv/Scripts/activate"
        pip_path = "backend/venv/Scripts/pip"
    else:  # Unix/Linux
        activate_script = "backend/venv/bin/activate"
        pip_path = "backend/venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    
    # Initialize database
    if os.name == 'nt':
        python_path = "backend/venv/Scripts/python"
    else:
        python_path = "backend/venv/bin/python"
    
    subprocess.run([python_path, "backend/init_db.py"], check=True)
    
    print("Backend setup complete!")

def setup_frontend():
    print("Setting up frontend...")
    
    # Install frontend dependencies
    os.chdir("frontend")
    subprocess.run(["npm", "install"], check=True)
    os.chdir("..")
    
    print("Frontend setup complete!")

def main():
    # Create necessary directories if they don't exist
    os.makedirs("backend", exist_ok=True)
    os.makedirs("frontend", exist_ok=True)
    
    try:
        setup_backend()
        setup_frontend()
        print("\nSetup completed successfully!")
        print("\nTo start the application:")
        print("1. Start the backend server:")
        if os.name == 'nt':
            print("   backend\\venv\\Scripts\\python backend\\main.py")
        else:
            print("   backend/venv/bin/python backend/main.py")
        print("2. Start the frontend development server:")
        print("   cd frontend && npm start")
    except subprocess.CalledProcessError as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
