"""
Build React and integrate with Django
Run this script to build production React app
"""
import os
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FRONTEND_DIR = BASE_DIR / 'frontend'
BUILD_DIR = FRONTEND_DIR / 'build'
BACKEND_DIR = BASE_DIR / 'backend'
BACKEND_STATIC = BACKEND_DIR / 'staticfiles'

def build_react():
    """Build React production bundle"""
    print("🔨 Building React production bundle...")
    
    os.chdir(FRONTEND_DIR)
    
    if not (FRONTEND_DIR / 'node_modules').exists():
        print("📦 Installing npm dependencies...")
        subprocess.run(['npm', 'install'], check=True)
    

    print("  Building React app...")
    subprocess.run(['npm', 'run', 'build'], check=True)
    
    print("✅ React build complete!")
 
    print("\n📦 Collecting Django static files...")
    os.chdir(BACKEND_DIR)
    subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)
    
    print("\n✅ Build complete! You can now run:")
    print("   cd backend")
    print("   python manage.py runserver")
    print("\n🌐 Access the app at: http://localhost:8000")

if __name__ == '__main__':
    try:
        build_react()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)