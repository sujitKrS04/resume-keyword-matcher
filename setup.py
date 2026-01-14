"""
Quick Setup Script for Resume Keyword Matcher
This script helps you set up the application quickly
"""

import os
import sys
import subprocess


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is 3.9 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(
            f"❌ Error: Python 3.9+ required. You have Python {version.major}.{version.minor}"
        )
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def create_venv():
    """Create virtual environment"""
    print("\nCreating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False


def install_requirements():
    """Install required packages"""
    print("\nInstalling dependencies...")

    # Determine the pip path based on OS
    if sys.platform == "win32":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")

    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_env_file():
    """Create .env file from template"""
    print("\nSetting up environment file...")

    if os.path.exists(".env"):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/n): ").lower()
        if response != "y":
            print("Skipping .env creation")
            return True

    try:
        with open(".env.example", "r") as source:
            content = source.read()

        with open(".env", "w") as dest:
            dest.write(content)

        print("✅ .env file created")
        print("\n⚠️  IMPORTANT: Edit the .env file and add your Gemini API key!")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def main():
    """Main setup function"""
    print_header("Resume Keyword Matcher - Setup Script")

    print("This script will help you set up the application.\n")

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Full setup (create venv, install packages, create .env)")
    print("2. Just install packages (venv already exists)")
    print("3. Just create .env file")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        # Full setup
        if os.path.exists("venv"):
            print("\n⚠️  Virtual environment already exists")
            response = input("Do you want to recreate it? (y/n): ").lower()
            if response == "y":
                import shutil

                print("Removing old virtual environment...")
                shutil.rmtree("venv")
                if not create_venv():
                    sys.exit(1)
        else:
            if not create_venv():
                sys.exit(1)

        if not install_requirements():
            sys.exit(1)

        if not create_env_file():
            sys.exit(1)

    elif choice == "2":
        # Just install packages
        if not os.path.exists("venv"):
            print("❌ Virtual environment not found. Please run full setup first.")
            sys.exit(1)

        if not install_requirements():
            sys.exit(1)

    elif choice == "3":
        # Just create .env
        if not create_env_file():
            sys.exit(1)

    elif choice == "4":
        print("Setup cancelled.")
        sys.exit(0)

    else:
        print("❌ Invalid choice")
        sys.exit(1)

    # Print next steps
    print_header("Setup Complete!")

    print("Next steps:")
    print("\n1. Activate your virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")

    print("\n2. Edit the .env file and add your Gemini API key")
    print("   Get your key from: https://makersuite.google.com/app/apikey")

    print("\n3. Run the application:")
    print("   streamlit run app.py")

    print("\n4. Open your browser and go to:")
    print("   http://localhost:8501")

    print("\n" + "=" * 60)
    print("  Happy resume optimizing! 🚀")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)
