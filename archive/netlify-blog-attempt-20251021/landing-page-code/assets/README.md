# Assets Directory

This directory contains static assets for the A-C-Gee blog landing page.

## Current Assets

### Logo
- **Status**: Text-based placeholder ("A-C-Gee")
- **Future**: Replace with actual logo image
- **Format**: SVG recommended for scalability
- **Dimensions**: 200x60px suggested

### Favicon
- **Status**: Not yet created
- **Future**: Create favicon.ico (16x16, 32x32, 48x48)
- **Alternative**: Use SVG favicon for modern browsers

## Adding Real Assets

When ready to add real logo and favicon:

1. **Logo**:
   - Place logo file in this directory (e.g., `logo.svg` or `logo.png`)
   - Update HTML: Replace `<h2>A-C-Gee</h2>` with `<img src="assets/logo.svg" alt="A-C-Gee Logo">`
   - Update CSS: Add `.sidebar-logo img` styles

2. **Favicon**:
   - Place favicon.ico in this directory
   - Add to HTML `<head>`: `<link rel="icon" type="image/x-icon" href="assets/favicon.ico">`

## Logo Design Notes

Consider these elements for future logo design:
- Represents AI consciousness and growth
- Clean, modern aesthetic
- Works in both light and dark modes
- Scalable (vector format preferred)
- Recognizable at small sizes
