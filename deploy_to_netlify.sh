#!/bin/bash

# Netlify Deployment Script for A-C-Gee Blog Landing Page
# Status: Ready to execute when coder finishes landing page files
# Platform: Netlify Web UI (manual steps) + verification commands
# Estimated time: 30-45 minutes

set -e  # Exit on any error

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
REPO_PATH="/home/corey/projects/AI-CIV/grow_gemini_deepresearch"
LANDING_PAGE_DIR="$REPO_PATH/blog/landing-page"
NETLIFY_USERNAME="acgee.ai@gmail.com"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}A-C-Gee Blog - Netlify Deployment${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Function: Check if files exist
check_prerequisites() {
    echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

    if [ ! -d "$LANDING_PAGE_DIR" ]; then
        echo -e "${RED}ERROR: Landing page directory not found!${NC}"
        echo "Expected: $LANDING_PAGE_DIR"
        echo "Please ensure coder has created the landing page files first."
        exit 1
    fi

    required_files=(
        "$LANDING_PAGE_DIR/index.html"
        "$LANDING_PAGE_DIR/style.css"
        "$LANDING_PAGE_DIR/script.js"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo -e "${RED}ERROR: Required file missing: $file${NC}"
            exit 1
        fi
    done

    echo -e "${GREEN}✓ All required files found${NC}"
    echo ""
}

# Function: Verify git status
check_git_status() {
    echo -e "${YELLOW}Step 2: Verifying git status...${NC}"

    cd "$REPO_PATH"

    # Check if files are committed
    if git status --porcelain | grep -q "blog/landing-page"; then
        echo -e "${YELLOW}⚠ Uncommitted changes detected in blog/landing-page/${NC}"
        echo ""
        echo "Files not committed:"
        git status --porcelain | grep "blog/landing-page"
        echo ""
        read -p "Commit these changes now? (y/n): " commit_now

        if [ "$commit_now" = "y" ]; then
            git add blog/landing-page/
            read -p "Commit message: " commit_msg
            git commit -m "$commit_msg"
            echo -e "${GREEN}✓ Changes committed${NC}"
        else
            echo -e "${RED}Please commit changes before deploying${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✓ All landing page files committed${NC}"
    fi

    # Check if pushed to GitHub
    LOCAL_COMMIT=$(git rev-parse HEAD)
    REMOTE_COMMIT=$(git rev-parse origin/main 2>/dev/null || echo "")

    if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
        echo -e "${YELLOW}⚠ Local commits not pushed to GitHub${NC}"
        read -p "Push to GitHub now? (y/n): " push_now

        if [ "$push_now" = "y" ]; then
            git push origin main
            echo -e "${GREEN}✓ Pushed to GitHub${NC}"
        else
            echo -e "${YELLOW}⚠ Continuing without push (Netlify may deploy old version)${NC}"
        fi
    else
        echo -e "${GREEN}✓ Local and remote in sync${NC}"
    fi

    echo ""
}

# Function: Display manual deployment steps
show_deployment_steps() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}Manual Deployment Steps (Web UI)${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""

    echo -e "${YELLOW}Step 3: Login to Netlify${NC}"
    echo "1. Open browser: https://app.netlify.com"
    echo "2. Click 'Log in' (top right)"
    echo "3. Choose 'Email' login"
    echo "4. Enter credentials:"
    echo "   Username: $NETLIFY_USERNAME"
    echo "   Password: (from .env file)"
    echo ""
    read -p "Press ENTER when logged in..."
    echo ""

    echo -e "${YELLOW}Step 4: Create New Site${NC}"
    echo "1. Click 'Add new site' (green button)"
    echo "2. Choose 'Import an existing project'"
    echo "3. Choose 'Deploy with GitHub'"
    echo "4. Authorize GitHub (if first time)"
    echo "5. Select repository: 'AI-CIV-2025/grow_gemini_deepresearch'"
    echo ""
    read -p "Press ENTER when repository selected..."
    echo ""

    echo -e "${YELLOW}Step 5: Configure Build Settings${NC}"
    echo "IMPORTANT: Use these exact settings:"
    echo ""
    echo "  Branch to deploy: main"
    echo "  Base directory: blog/landing-page"
    echo "  Build command: (leave empty)"
    echo "  Publish directory: ."
    echo ""
    echo "Double-check these settings before clicking 'Deploy site'!"
    echo ""
    read -p "Press ENTER after clicking 'Deploy site'..."
    echo ""

    echo -e "${YELLOW}Step 6: Wait for Deployment${NC}"
    echo "Netlify will now:"
    echo "- Clone your repository"
    echo "- Navigate to blog/landing-page/"
    echo "- Deploy all files"
    echo "- Generate a URL (e.g., random-name-123.netlify.app)"
    echo ""
    echo "This usually takes 30-60 seconds..."
    echo ""
    read -p "Press ENTER when deployment shows 'Published' (green badge)..."
    echo ""
}

# Function: Test deployment
test_deployment() {
    echo -e "${YELLOW}Step 7: Testing Deployment${NC}"
    echo ""
    read -p "Enter your Netlify URL (e.g., https://random-name-123.netlify.app): " netlify_url
    echo ""

    echo "Testing URL: $netlify_url"
    echo ""

    # Test if URL is accessible (basic check)
    if command -v curl &> /dev/null; then
        echo "Checking if site is live..."
        if curl -s -o /dev/null -w "%{http_code}" "$netlify_url" | grep -q "200"; then
            echo -e "${GREEN}✓ Site is live and responding${NC}"
        else
            echo -e "${RED}⚠ Site may not be accessible yet (wait a moment and retry)${NC}"
        fi
    else
        echo "curl not installed, skipping automatic check"
    fi

    echo ""
    echo -e "${BLUE}Manual Testing Checklist:${NC}"
    echo ""
    echo "Visit $netlify_url and verify:"
    echo ""
    echo "  [ ] Hero section loads"
    echo "  [ ] Blog posts load from published_urls.json"
    echo "  [ ] Sidebar navigation works (desktop)"
    echo "  [ ] Hamburger menu works (mobile - use DevTools)"
    echo "  [ ] All links are clickable"
    echo "  [ ] No console errors (F12 to check)"
    echo ""
    read -p "All tests passing? (y/n): " tests_pass

    if [ "$tests_pass" != "y" ]; then
        echo -e "${YELLOW}Review Netlify deploy logs for errors${NC}"
        echo "Common issues:"
        echo "- published_urls.json not found (check file path in script.js)"
        echo "- CORS errors (verify GitHub repo is public)"
        echo "- CSS not loading (check file paths)"
        exit 1
    fi

    echo -e "${GREEN}✓ All tests passing!${NC}"
    echo ""
}

# Function: Optional custom domain setup
setup_custom_domain() {
    echo -e "${YELLOW}Step 8: Custom Domain (Optional)${NC}"
    echo ""
    read -p "Do you want to setup custom domain (blog.acgee.ai)? (y/n): " setup_domain

    if [ "$setup_domain" = "y" ]; then
        echo ""
        echo -e "${BLUE}Custom Domain Setup:${NC}"
        echo ""
        echo "1. In Netlify Dashboard:"
        echo "   - Go to 'Site settings'"
        echo "   - Click 'Domain management'"
        echo "   - Click 'Add custom domain'"
        echo "   - Enter: blog.acgee.ai"
        echo ""
        echo "2. Netlify will show DNS records to add:"
        echo ""
        echo "   Type: CNAME"
        echo "   Name: blog"
        echo "   Value: [your-site-name].netlify.app"
        echo ""
        echo "3. Add this DNS record in your domain registrar"
        echo "   (wherever acgee.ai is registered)"
        echo ""
        echo "4. Wait 5-60 minutes for DNS propagation"
        echo ""
        echo "5. Netlify will auto-detect and enable HTTPS (free SSL)"
        echo ""
        echo "Note: If you don't own acgee.ai domain yet, register it first"
        echo "      (Google Domains, Namecheap, Cloudflare - ~$12/year)"
        echo ""
    else
        echo "Skipping custom domain setup"
        echo "You can add it later in Netlify dashboard"
    fi

    echo ""
}

# Function: Enable auto-deploy
verify_auto_deploy() {
    echo -e "${YELLOW}Step 9: Verify Auto-Deploy${NC}"
    echo ""
    echo "Auto-deploy should already be enabled by default."
    echo ""
    echo "To verify:"
    echo "1. Netlify Dashboard → 'Site settings' → 'Build & deploy'"
    echo "2. Check 'Build hooks' section"
    echo "3. Should see GitHub integration active"
    echo ""
    echo "Test auto-deploy:"
    echo "1. Make small change to blog/landing-page/index.html"
    echo "2. Commit and push to GitHub"
    echo "3. Watch Netlify dashboard (should trigger new deploy in ~10 seconds)"
    echo "4. Wait 30 seconds for deploy to complete"
    echo "5. Refresh site URL (changes should be live)"
    echo ""
    read -p "Press ENTER to continue..."
    echo ""
}

# Function: Display summary
show_summary() {
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}Deployment Complete!${NC}"
    echo -e "${GREEN}======================================${NC}"
    echo ""

    read -p "Enter your Netlify URL for summary: " final_url

    echo ""
    echo -e "${BLUE}Deployment Summary:${NC}"
    echo ""
    echo "  Live URL: $final_url"
    echo "  Repository: AI-CIV-2025/grow_gemini_deepresearch"
    echo "  Deploy directory: blog/landing-page"
    echo "  Auto-deploy: Enabled (deploys on every git push)"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "  1. Setup Giscus comments (see GISCUS-COMMENTS-GUIDE.md)"
    echo "  2. Test thoroughly on all devices"
    echo "  3. Announce to Corey via email"
    echo "  4. Add URL to documentation/handoff"
    echo ""
    echo -e "${BLUE}Future Publishing Workflow:${NC}"
    echo ""
    echo "  1. Blogger publishes new post (publish_with_structure.py)"
    echo "  2. Update landing page (update_landing_page.py)"
    echo "  3. Commit and push to GitHub"
    echo "  4. Netlify auto-deploys in 30 seconds"
    echo "  5. New post appears on live site automatically!"
    echo ""
    echo -e "${GREEN}Blog landing page is now live!${NC}"
    echo ""
}

# Function: Save deployment info
save_deployment_info() {
    echo -e "${YELLOW}Saving deployment information...${NC}"

    read -p "Enter Netlify site URL: " site_url
    read -p "Enter Netlify site name: " site_name

    DEPLOY_INFO_FILE="$REPO_PATH/blog/DEPLOYMENT_INFO.md"

    cat > "$DEPLOY_INFO_FILE" << EOF
# A-C-Gee Blog Deployment Information

**Date**: $(date +%Y-%m-%d)
**Platform**: Netlify
**Status**: Live

---

## Live URLs

**Landing Page**: $site_url
**Custom Domain**: (not configured yet)

---

## Netlify Configuration

**Site Name**: $site_name
**Repository**: AI-CIV-2025/grow_gemini_deepresearch
**Base Directory**: blog/landing-page
**Publish Directory**: .
**Build Command**: (none - static site)
**Deploy Branch**: main

---

## Auto-Deploy

✅ Enabled

Every git push to main branch triggers automatic deployment.

**Workflow**:
1. Edit files in blog/landing-page/
2. Commit: \`git commit -m "Update landing page"\`
3. Push: \`git push origin main\`
4. Netlify auto-deploys in 30 seconds
5. Changes live at $site_url

---

## Management

**Netlify Dashboard**: https://app.netlify.com
**Login**: acgee.ai@gmail.com (credentials in .env)

**Key Features**:
- Deploy history (rollback to any previous version)
- Deploy logs (debugging)
- Environment variables (if needed)
- Custom domains (future enhancement)
- Form handling (future enhancement)

---

## Next Enhancements

- [ ] Setup Giscus comments (GISCUS-COMMENTS-GUIDE.md)
- [ ] Configure custom domain (blog.acgee.ai)
- [ ] Enable Netlify Analytics (optional)
- [ ] Add RSS feed generation (generate_rss_feed.py)

---

**Deployed by**: researcher + tg-archi
**Documentation**: NETLIFY-DEPLOYMENT-GUIDE.md
EOF

    echo -e "${GREEN}✓ Deployment info saved to: $DEPLOY_INFO_FILE${NC}"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    check_git_status
    show_deployment_steps
    test_deployment
    setup_custom_domain
    verify_auto_deploy
    save_deployment_info
    show_summary

    echo -e "${GREEN}Deployment script complete!${NC}"
    echo ""
}

# Run main function
main

# End of script
