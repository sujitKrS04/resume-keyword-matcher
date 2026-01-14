#!/bin/bash

# Resume Keyword Matcher - Unix/Linux/macOS Setup Script
# Run this script to set up the application

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "\n${CYAN}============================================================${NC}"
echo -e "${CYAN}  Resume Keyword Matcher - Setup Script${NC}"
echo -e "${CYAN}============================================================${NC}\n"

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.9+ first.${NC}"
    echo -e "${YELLOW}  Download from: https://www.python.org/downloads/${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/n): " response
    if [ "$response" = "y" ]; then
        rm -rf venv
        $PYTHON_CMD -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    else
        echo -e "${CYAN}Using existing virtual environment${NC}"
    fi
else
    $PYTHON_CMD -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install requirements
echo -e "\n${YELLOW}Installing dependencies...${NC}"
echo -e "${CYAN}This may take a few minutes...${NC}"
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install some dependencies${NC}"
    exit 1
fi

# Create .env file
echo -e "\n${YELLOW}Setting up environment file...${NC}"
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
    read -p "Do you want to overwrite it? (y/n): " response
    if [ "$response" = "y" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
    else
        echo -e "${CYAN}Keeping existing .env file${NC}"
    fi
else
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
fi

# Final instructions
echo -e "\n${CYAN}============================================================${NC}"
echo -e "${GREEN}  Setup Complete! 🎉${NC}"
echo -e "${CYAN}============================================================${NC}\n"

echo -e "${YELLOW}Next steps:${NC}\n"
echo -e "${NC}1. Edit the .env file and add your Gemini API key${NC}"
echo -e "   ${CYAN}Get your free API key from:${NC}"
echo -e "   ${CYAN}https://makersuite.google.com/app/apikey${NC}\n"

echo -e "${NC}2. Activate the virtual environment:${NC}"
echo -e "   ${CYAN}source venv/bin/activate${NC}\n"

echo -e "${NC}3. Run the application:${NC}"
echo -e "   ${CYAN}streamlit run app.py${NC}\n"

echo -e "${NC}4. Open your browser and visit:${NC}"
echo -e "   ${CYAN}http://localhost:8501${NC}\n"

echo -e "${CYAN}============================================================${NC}"
echo -e "${GREEN}  Happy resume optimizing! 🚀${NC}"
echo -e "${CYAN}============================================================${NC}\n"

# Ask if user wants to run the app now
read -p "Would you like to run the application now? (y/n): " run_now
if [ "$run_now" = "y" ]; then
    echo -e "\n${YELLOW}Starting application...${NC}\n"
    streamlit run app.py
fi
