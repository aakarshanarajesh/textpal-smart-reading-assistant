#!/usr/bin/env python3
"""
TextPal System Requirements Checker
Verifies all dependencies and provides setup guidance
"""

import sys
import subprocess
import platform
import os


class Color:
    """Terminal colors"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Color.BLUE}{Color.BOLD}{'='*60}{Color.END}")
    print(f"{Color.BLUE}{Color.BOLD}{text}{Color.END}")
    print(f"{Color.BLUE}{Color.BOLD}{'='*60}{Color.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Color.GREEN}✅ {text}{Color.END}")


def print_error(text):
    """Print error message"""
    print(f"{Color.RED}❌ {text}{Color.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Color.YELLOW}⚠️  {text}{Color.END}")


def print_info(text):
    """Print info message"""
    print(f"{Color.BLUE}ℹ️  {text}{Color.END}")


def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Current: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor} meets requirements (3.8+)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} is too old!")
        print_info("Please install Python 3.8 or higher")
        return False


def check_os():
    """Check operating system"""
    print_header("Checking Operating System")
    
    os_name = platform.system()
    os_version = platform.release()
    
    print(f"OS: {os_name} {os_version}")
    print(f"Architecture: {platform.machine()}")
    
    supported = os_name in ['Windows', 'Darwin', 'Linux']
    if supported:
        print_success(f"{os_name} is supported")
    else:
        print_warning(f"{os_name} may not be fully supported")
    
    return supported


def check_required_commands():
    """Check if required commands are available"""
    print_header("Checking Required Commands")
    
    commands = {
        'git': 'Git (version control)',
        'pip': 'Pip (package manager)',
    }
    
    all_found = True
    for cmd, description in commands.items():
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                print_success(f"{description}: {result.stdout.strip()}")
            else:
                print_warning(f"{description}: Found but may not work correctly")
        except FileNotFoundError:
            print_error(f"{description}: Not found in PATH")
            all_found = False
        except Exception as e:
            print_warning(f"{description}: Error checking - {e}")
    
    return all_found


def check_disk_space():
    """Check available disk space"""
    print_header("Checking Disk Space")
    
    try:
        import shutil
        disk = shutil.disk_usage('/')
        free_gb = disk.free / (1024**3)
        total_gb = disk.total / (1024**3)
        
        print(f"Total: {total_gb:.1f} GB")
        print(f"Free: {free_gb:.1f} GB")
        
        if free_gb >= 5:
            print_success("Sufficient disk space available (5GB+ needed)")
            return True
        else:
            print_warning(f"Low disk space ({free_gb:.1f}GB available)")
            print_info("Models require ~2GB, project ~3GB")
            return False
    except Exception as e:
        print_warning(f"Could not check disk space: {e}")
        return True


def check_ram():
    """Check available RAM"""
    print_header("Checking RAM")
    
    try:
        import psutil
        ram = psutil.virtual_memory()
        ram_gb = ram.total / (1024**3)
        free_gb = ram.available / (1024**3)
        
        print(f"Total: {ram_gb:.1f} GB")
        print(f"Available: {free_gb:.1f} GB")
        
        if ram_gb >= 4:
            print_success(f"Sufficient RAM ({ram_gb:.1f}GB)")
            return True
        else:
            print_warning(f"Limited RAM ({ram_gb:.1f}GB) - may be slow")
            return False
    except ImportError:
        print_info("psutil not installed - skipping RAM check")
        print_info("Run: pip install psutil")
        return True
    except Exception as e:
        print_warning(f"Could not check RAM: {e}")
        return True


def setup_virtual_environment():
    """Guide through virtual environment setup"""
    print_header("Virtual Environment Setup")
    
    os_name = platform.system()
    
    if os_name == 'Windows':
        commands = [
            "python -m venv venv",
            "venv\\Scripts\\activate",
            "pip install -r requirements.txt"
        ]
        explanation = """
Commands to run (Windows):
    1. Create: python -m venv venv
    2. Activate: venv\\Scripts\\activate
    3. Install: pip install -r requirements.txt
    4. Run: python app.py
"""
    else:
        commands = [
            "python3 -m venv venv",
            "source venv/bin/activate",
            "pip install -r requirements.txt"
        ]
        explanation = """
Commands to run (macOS/Linux):
    1. Create: python3 -m venv venv
    2. Activate: source venv/bin/activate
    3. Install: pip install -r requirements.txt
    4. Run: python app.py
"""
    
    print(explanation)
    return commands


def check_internet_connection():
    """Check internet connection"""
    print_header("Checking Internet Connection")
    
    try:
        import urllib.request
        urllib.request.urlopen('http://www.google.com', timeout=2)
        print_success("Internet connection is available")
        return True
    except:
        print_warning("Could not verify internet connection")
        print_info("Note: Internet is required to download models")
        return False


def generate_report():
    """Generate setup report"""
    print_header("TextPal System Requirements Report")
    
    checks = {
        'Python Version': check_python_version(),
        'Operating System': check_os(),
        'Commands': check_required_commands(),
        'Disk Space': check_disk_space(),
        'RAM': check_ram(),
        'Internet': check_internet_connection(),
    }
    
    print_header("Summary")
    
    for check, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check}")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print_success("\nYour system is ready for TextPal!")
        print_info("\nNext steps:")
        print_info("1. Review QUICKSTART.md for setup instructions")
        print_info("2. Run: python app.py")
        print_info("3. Open: http://localhost:5000")
    else:
        print_warning("\nSome checks failed. Please address issues above.")
        print_info("Review requirements in README.md")
    
    return passed == total


def main():
    """Main function"""
    print(f"\n{Color.BOLD}TextPal - System Requirements Checker{Color.END}")
    print(f"{Color.BOLD}Version 1.0{Color.END}\n")
    
    try:
        success = generate_report()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_warning("\n\nCheck interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
