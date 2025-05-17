#!/bin/bash

# Define colors with richer palette
GREEN='\033[0;38;5;82m'
BLUE='\033[0;38;5;39m'
YELLOW='\033[0;38;5;220m'
RED='\033[0;38;5;196m'
CYAN='\033[0;38;5;51m'
PURPLE='\033[0;38;5;135m'
ORANGE='\033[0;38;5;208m'
PINK='\033[0;echo -e "${BLUE}To build the application later, run:${NC}"
    echo -e "${PURPLE}cd $PROJECT_DIR && ./env/bin/pyinstaller main.spec${NC}";5;213m'
NC='\033[0m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
BLINK='\033[5m'

# Clear the terminal
clear

# Draw fancy app logo
echo -e "${CYAN}${BOLD}"
echo ' ┌─────────────────────────────────────────────────┐'
echo ' │                                                 │'
echo ' │   ███████╗██╗  ██╗██████╗  ██████╗  ██████╗     │'
echo ' │   ██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔═══██╗    │'
echo ' │   ███████╗███████║██████╔╝██║   ██║██║   ██║    │'
echo ' │   ╚════██║██╔══██║██╔══██╗██║   ██║██║   ██║    │'
echo ' │   ███████║██║  ██║██║  ██║╚██████╔╝╚██████╔╝    │'
echo ' │   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝     │'
echo ' │                                                 │'
echo ' │             ███╗   ███╗██╗███████╗              │'
echo ' │             ████╗ ████║██║██╔════╝              │'
echo ' │             ██╔████╔██║██║█████╗                │'
echo ' │             ██║╚██╔╝██║██║██╔══╝                │'
echo ' │             ██║ ╚═╝ ██║██║███████╗              │'
echo ' │             ╚═╝     ╚═╝╚═╝╚══════╝              │'
echo ' │                                                 │'
echo ' └─────────────────────────────────────────────────┘'
echo -e "${NC}\n"

# Show project info
echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║            ${ORANGE}SHROOMIE INSTALLER TOOL${BLUE}             ║${NC}"
echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════════╝${NC}\n"

# Set project directory to current directory
PROJECT_DIR="$(pwd)"
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo -e "${RED}${BOLD}[ERROR]${NC} Not in the correct directory. Please run this script from the shroomie directory!"
    exit 1
fi

# Create and activate Python virtual environment
echo -e "${YELLOW}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ ${BOLD}STEP [1/6]${NC} ${CYAN}Setting up Python environment...${NC}   ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────┘${NC}"

if [ ! -d "env" ]; then
    echo -e "${ORANGE}[!]${NC} Creating virtual environment..."
    python3 -m venv env
    if [ $? -ne 0 ]; then
        echo -e "${RED}[✗]${NC} Failed to create virtual environment!"
        exit 1
    else
        echo -e "${GREEN}[✓]${NC} Virtual environment ${BOLD}created successfully${NC}."
    fi
else
    echo -e "${GREEN}[✓]${NC} Virtual environment ${BOLD}already exists${NC}."
fi

# Activate virtual environment
source env/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}[✗]${NC} Failed to activate virtual environment!"
    exit 1
else
    echo -e "${GREEN}[✓]${NC} Virtual environment ${BOLD}activated successfully${NC}."
fi

# Install required packages
echo -e "\n${CYAN}Installing required packages...${NC}"
pip install PyQt6 pexpect pyinstaller
if [ $? -ne 0 ]; then
    echo -e "${RED}[✗]${NC} Failed to install required packages!"
    exit 1
else
    echo -e "${GREEN}[✓]${NC} Required packages ${BOLD}installed successfully${NC}."
fi

# Check PyInstaller installation
echo -e "${YELLOW}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ ${BOLD}STEP [2/6]${NC} ${CYAN}Checking PyInstaller installation...${NC} ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────┘${NC}"

if ! command -v pyinstaller &> /dev/null; then
    echo -e "${ORANGE}[!]${NC} PyInstaller not found. Installing now..."
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo -e "${RED}[✗]${NC} Failed to install PyInstaller!"
        exit 1
    else
        echo -e "${GREEN}[✓]${NC} PyInstaller ${BOLD}successfully installed${NC}."
    fi
else
    echo -e "${GREEN}[✓]${NC} PyInstaller is ${BOLD}already installed${NC}."
fi

# Navigate to project directory
echo -e "\n${YELLOW}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ ${BOLD}STEP [3/6]${NC} ${CYAN}Navigating to project directory...${NC} ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────┘${NC}"

cd "$PROJECT_DIR"
if [ $? -ne 0 ]; then
    echo -e "${RED}[✗]${NC} Failed to navigate to ${BOLD}$PROJECT_DIR${NC}!"
    exit 1
else
    echo -e "${GREEN}[✓]${NC} Successfully navigated to: ${BOLD}$(pwd)${NC}"
fi

# Check for main.py file
echo -e "\n${YELLOW}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ ${BOLD}STEP [4/6]${NC} ${CYAN}Checking for main.py file...${NC}      ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────┘${NC}"

if [ ! -f "main.py" ]; then
    echo -e "${RED}[✗]${NC} main.py file ${BOLD}not found${NC} in the current directory!"
    exit 1
else
    echo -e "${GREEN}[✓]${NC} main.py file ${BOLD}found${NC}."
fi

# Create spec file
echo -e "\n${YELLOW}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ ${BOLD}STEP [5/6]${NC} ${CYAN}Creating spec file...${NC}             ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────┘${NC}"

echo -e "${CYAN}Executing command:${NC}"
echo -e "${PURPLE}pyi-makespec --onefile --windowed --hidden-import pexpect --hidden-import ptyprocess --hidden-import logging.handlers --hidden-import utils --hidden-import utils.logger --hidden-import utils.themes.colors --hidden-import utils.themes.fonts --hidden-import services.aur_service --hidden-import services.sudo_auth --hidden-import ui.pages --add-data \"resources:resources\" --add-data \"ui:ui\" --add-data \"utils:utils\" --add-data \"components:components\" --add-data \"config:config\" --add-data \"models:models\" --add-data \"services:services\" main.py${NC}\n"

# Show fancy progress bar during spec file creation
function progress_bar {
    local duration=$1
    local interval=0.05
    local steps=$((duration / interval))
    local width=50

    for ((i=0; i<=steps; i++)); do
        local percentage=$((i * 100 / steps))
        local filled=$((i * width / steps))
        local empty=$((width - filled))

        printf "\r${BOLD}[${NC}${BLUE}"
        printf "%${filled}s" '' | tr ' ' '█'
        printf "${NC}${YELLOW}"
        printf "%${empty}s" '' | tr ' ' '▒'
        printf "${NC}${BOLD}]${NC} ${CYAN}%3d%%${NC}" $percentage

        sleep $interval
    done
    echo
}

# Execute the command with output logging
./env/bin/pyi-makespec --onefile --windowed --hidden-import pexpect --hidden-import ptyprocess --hidden-import logging.handlers --hidden-import utils --hidden-import utils.logger --hidden-import utils.themes.colors --hidden-import utils.themes.fonts --hidden-import services.aur_service --hidden-import services.sudo_auth --hidden-import ui.pages --add-data "resources:resources" --add-data "ui:ui" --add-data "utils:utils" --add-data "components:components" --add-data "config:config" --add-data "models:models" --add-data "services:services" main.py > /tmp/makespec_output.log 2>&1 &

PID=$!
progress_bar 5  # Approximate time for spec file creation

# Check operation success
wait $PID
if [ $? -ne 0 ]; then
    echo -e "\n${RED}${BOLD}[✗] FAILED:${NC} Spec file creation failed!"
    echo -e "${YELLOW}Error details:${NC}"
    cat /tmp/makespec_output.log
    exit 1
else
    echo -e "\n${GREEN}${BOLD}[✓] SUCCESS:${NC} Spec file created successfully."
fi

# Display spec file info
if [ -f "main.spec" ]; then
    echo -e "${CYAN}Created file: ${BOLD}${UNDERLINE}main.spec${NC}"
else
    echo -e "${RED}${BOLD}[✗] ERROR:${NC} main.spec file not found despite command success!"
    exit 1
fi

# Build application
echo -e "\n${YELLOW}┌─────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│ ${BOLD}STEP [6/6]${NC} ${CYAN}Build the application now?${NC}        ${YELLOW}│${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────┘${NC}"
echo -en "${ORANGE}Would you like to build the application now? ${BOLD}(y/n)${NC}: "
read -r BUILD_NOW

if [[ "$BUILD_NOW" == "y" || "$BUILD_NOW" == "Y" ]]; then
    echo -e "\n${CYAN}${BOLD}Building application using PyInstaller...${NC}"
    echo -e "${PURPLE}pyinstaller main.spec${NC}\n"

    # Run PyInstaller with output logging
    ./env/bin/pyinstaller main.spec > /tmp/build_output.log 2>&1 &
    PID=$!

    # Fancy spinner animation
    spinners=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
    messages=("Compiling sources..." "Processing resources..." "Packaging files..." "Creating bundle..." "Finalizing build...")
    i=0
    m=0

    while kill -0 $PID 2>/dev/null; do
        i=$(( (i+1) % 10 ))

        # Change message every ~3 seconds
        if [ $((i % 30)) -eq 0 ]; then
            m=$(( (m+1) % 5 ))
        fi

        echo -en "\r${YELLOW}${BOLD}[${spinners[$i]}]${NC} ${CYAN}${messages[$m]}${NC}                             "
        sleep 0.1
    done

    # Check build success
    wait $PID
    if [ $? -ne 0 ]; then
        echo -e "\n\n${RED}${BOLD}[✗] BUILD FAILED!${NC}"
        echo -e "${YELLOW}Error details:${NC}"
        cat /tmp/build_output.log
        exit 1
    else
        echo -e "\n\n${GREEN}${BOLD}[✓] BUILD SUCCESSFUL!${NC} 🎉"
        echo -e "${CYAN}You can find your application at:${NC} ${BOLD}${UNDERLINE}$(pwd)/dist/main${NC}"
    fi
else
    echo -e "\n${BLUE}To build the application later, run:${NC}"
    echo -e "${PURPLE}cd $PROJECT_DIR && pyinstaller main.spec${NC}"
fi

echo -e "\n${GREEN}${BOLD}╔═════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║            OPERATION COMPLETED!            ║${NC}"
echo -e "${GREEN}${BOLD}╚═════════════════════════════════════════════╝${NC}"
