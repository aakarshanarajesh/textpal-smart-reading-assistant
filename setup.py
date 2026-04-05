#!/usr/bin/env python
"""
TextPal Quick Start Script
Runs all necessary setup and starts the application
"""

import os
import sys
import subprocess
import platform


def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n{'='*60}")
    print(f"📌 {description}")
    print(f"{'='*60}")
    print(f"Running: {cmd}\n")
    
    try:
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"❌ Error running: {description}")
            return False
        print(f"✅ {description} completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🚀 Smart Reading Assistant (TextPal)")
    print("Quick Start Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Determine OS
    os_type = platform.system()
    print(f"✅ Operating System: {os_type}")
    
    # Step 1: Create virtual environment
    if os_type == "Windows":
        venv_cmd = "python -m venv venv && venv\\Scripts\\activate"
        activate_cmd = "venv\\Scripts\\activate"
    else:
        venv_cmd = "python3 -m venv venv && source venv/bin/activate"
        activate_cmd = "source venv/bin/activate"
    
    print("\n1️⃣ Creating virtual environment...")
    if os_type == "Windows":
        os.system("python -m venv venv")
    else:
        os.system("python3 -m venv venv")
    print("✅ Virtual environment created")
    
    # Step 2: Install dependencies
    print("\n2️⃣ Installing dependencies...")
    if os_type == "Windows":
        pip_cmd = "venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_cmd = "venv/bin/pip install -r requirements.txt"
    
    os.system(pip_cmd)
    print("✅ Dependencies installed")
    
    # Step 3: Create uploads directory
    print("\n3️⃣ Creating upload directory...")
    os.makedirs("uploads", exist_ok=True)
    print("✅ Upload directory created")
    
    # Step 4: Copy .env file
    print("\n4️⃣ Setting up configuration...")
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Configuration file created (.env)")
        else:
            print("⚠️  .env file not found, using defaults")
    else:
        print("✅ Configuration file (.env) already exists")
    
    # Step 5: Show instructions
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print("\nTo start the application, run:\n")
    
    if os_type == "Windows":
        print("  1. Activate virtual environment:")
        print("     venv\\Scripts\\activate")
        print("  2. Run the application:")
        print("     python app.py")
    else:
        print("  1. Activate virtual environment:")
        print("     source venv/bin/activate")
        print("  2. Run the application:")
        print("     python app.py")
    
    print("\n🌐 The application will be available at:")
    print("   http://localhost:5000")
    print("\n" + "="*60)
    print("📚 For more information, see README.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
