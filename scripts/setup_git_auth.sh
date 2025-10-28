#!/bin/bash

# Interactive GitHub Authentication Setup Script
# Makes git authentication simple and guided

set -e

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  GitHub Authentication Setup${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "This script will help you set up GitHub authentication."
echo "You'll be able to push commits once we're done!"
echo ""

# Function to wait for user
wait_for_user() {
    echo -e "${YELLOW}Press Enter when ready to continue...${NC}"
    read
}

# Function to test git connection
test_git_connection() {
    echo -e "${BLUE}Testing your GitHub connection...${NC}"
    if git ls-remote git@github.com:gregdavill/sage-civilization.git &> /dev/null; then
        echo -e "${GREEN}✓ SUCCESS! GitHub connection is working!${NC}"
        return 0
    else
        echo -e "${RED}✗ Connection test failed. Let's try again.${NC}"
        return 1
    fi
}

# Ask which method
echo "Which authentication method do you prefer?"
echo ""
echo -e "${GREEN}1) SSH Keys${NC} (Recommended - more secure, no passwords)"
echo -e "${BLUE}2) Personal Access Token${NC} (Simpler, but less secure)"
echo ""
echo -n "Enter your choice (1 or 2): "
read choice

case $choice in
    1)
        echo -e "\n${GREEN}Great choice! SSH keys are more secure.${NC}\n"

        # Check if SSH key exists
        if [ -f ~/.ssh/id_ed25519.pub ]; then
            echo -e "${YELLOW}Found an existing SSH key!${NC}"
            echo "Would you like to use it? (y/n): "
            read use_existing

            if [ "$use_existing" = "n" ] || [ "$use_existing" = "N" ]; then
                echo "Generating a new SSH key..."
                ssh-keygen -t ed25519 -C "greg@gregdavill.com" -f ~/.ssh/id_ed25519
            fi
        else
            echo "No SSH key found. Let's create one!"
            echo ""
            echo "The script will now generate an SSH key."
            echo "When prompted for a passphrase, you can press Enter for no passphrase,"
            echo "or enter a passphrase for extra security."
            wait_for_user

            # Create .ssh directory if it doesn't exist
            mkdir -p ~/.ssh
            chmod 700 ~/.ssh

            # Generate SSH key
            ssh-keygen -t ed25519 -C "greg@gregdavill.com" -f ~/.ssh/id_ed25519
        fi

        echo ""
        echo -e "${GREEN}======================================${NC}"
        echo -e "${GREEN}  Your SSH Public Key${NC}"
        echo -e "${GREEN}======================================${NC}"
        echo ""
        cat ~/.ssh/id_ed25519.pub
        echo ""
        echo -e "${GREEN}======================================${NC}"
        echo ""

        echo -e "${YELLOW}Now, follow these steps:${NC}"
        echo ""
        echo "1. Copy the key shown above (everything from 'ssh-ed25519' to the end)"
        echo ""
        echo "2. Open this link in your browser:"
        echo -e "   ${BLUE}https://github.com/settings/ssh/new${NC}"
        echo ""
        echo "3. Give it a title like: 'Sage Laptop'"
        echo ""
        echo "4. Paste your key into the 'Key' field"
        echo ""
        echo "5. Click 'Add SSH key'"
        echo ""

        wait_for_user

        # Configure git to use SSH
        echo -e "${BLUE}Configuring git to use SSH...${NC}"
        git remote set-url origin git@github.com:gregdavill/sage-civilization.git

        # Start ssh-agent and add key
        echo -e "${BLUE}Adding your SSH key to the agent...${NC}"
        eval "$(ssh-agent -s)"
        ssh-add ~/.ssh/id_ed25519

        # Test connection
        echo ""
        if test_git_connection; then
            echo ""
            echo -e "${GREEN}🎉 AWESOME! You're all set up!${NC}"
            echo -e "${GREEN}You can now push commits to GitHub!${NC}"
            exit 0
        else
            echo ""
            echo -e "${RED}Hmm, something didn't work.${NC}"
            echo "Double-check that you added the key to GitHub correctly."
            echo "You can run this script again if needed."
            exit 1
        fi
        ;;

    2)
        echo -e "\n${BLUE}Okay! Let's set up a Personal Access Token.${NC}\n"

        echo -e "${YELLOW}Step 1: Create a token on GitHub${NC}"
        echo ""
        echo "1. Open this link in your browser:"
        echo -e "   ${BLUE}https://github.com/settings/tokens/new${NC}"
        echo ""
        echo "2. Give it a name like: 'Sage Civilization'"
        echo ""
        echo "3. Set expiration to: 90 days (or longer if you prefer)"
        echo ""
        echo "4. Under 'Select scopes', check ONLY: ${GREEN}repo${NC}"
        echo "   (This gives access to your repositories)"
        echo ""
        echo "5. Scroll down and click 'Generate token'"
        echo ""
        echo "6. ${YELLOW}IMPORTANT:${NC} Copy the token immediately!"
        echo "   (GitHub only shows it once)"
        echo ""

        wait_for_user

        echo -e "${YELLOW}Step 2: Enter your token${NC}"
        echo ""
        echo "Paste your token here (it won't be visible as you type):"
        read -s token
        echo ""

        if [ -z "$token" ]; then
            echo -e "${RED}No token entered. Please run the script again.${NC}"
            exit 1
        fi

        # Configure git credential helper
        echo -e "${BLUE}Configuring git to remember your token...${NC}"
        git config --global credential.helper store

        # Store credentials
        echo "https://gregdavill:${token}@github.com" > ~/.git-credentials
        chmod 600 ~/.git-credentials

        # Configure remote URL for HTTPS
        git remote set-url origin https://github.com/gregdavill/sage-civilization.git

        # Test with a fetch
        echo ""
        echo -e "${BLUE}Testing your token...${NC}"
        if git fetch origin &> /dev/null; then
            echo -e "${GREEN}✓ SUCCESS! Your token is working!${NC}"
            echo ""
            echo -e "${GREEN}🎉 AWESOME! You're all set up!${NC}"
            echo -e "${GREEN}You can now push commits to GitHub!${NC}"
            echo ""
            echo -e "${YELLOW}Note:${NC} Your token is saved securely in ~/.git-credentials"
            exit 0
        else
            echo -e "${RED}✗ Token test failed.${NC}"
            echo ""
            echo "Possible issues:"
            echo "- Token might be incorrect"
            echo "- Token might not have 'repo' permissions"
            echo "- Token might have expired"
            echo ""
            echo "You can run this script again to try with a new token."
            exit 1
        fi
        ;;

    *)
        echo -e "${RED}Invalid choice. Please run the script again and choose 1 or 2.${NC}"
        exit 1
        ;;
esac
