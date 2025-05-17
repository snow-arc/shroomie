import subprocess
from typing import Tuple

def check_yay_installation() -> Tuple[bool, str]:
    """
    Check if yay (AUR helper) is installed on the system.
    
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if yay is installed, False otherwise
            - str: Installation instructions if yay is not installed
    """
    try:
        subprocess.run(['yay', '--version'], 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     check=True)
        return True, ""
    except subprocess.CalledProcessError:
        install_message = """To install yay:
1. Install base-devel and git:
   sudo pacman -S --needed git base-devel
2. Clone the yay repository:
   git clone https://aur.archlinux.org/yay.git
3. Build and install yay:
   cd yay
   makepkg -si"""
        return False, install_message
    except FileNotFoundError:
        # Same instructions as above, just a different error case
        install_message = """To install yay:
1. Install base-devel and git:
   sudo pacman -S --needed git base-devel
2. Clone the yay repository:
   git clone https://aur.archlinux.org/yay.git
3. Build and install yay:
   cd yay
   makepkg -si"""
        return False, install_message
