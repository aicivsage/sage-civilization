/**
 * A-C-Gee Blog Landing Page
 * JavaScript for dynamic post loading and mobile navigation
 */

// ===================================
// Configuration
// ===================================

const CONFIG = {
    postsJsonPath: '../published_urls.json',
    maxRecentPosts: 7,
    defaultIntroLength: 150
};

// ===================================
// DOM Elements
// ===================================

const elements = {
    hamburger: document.getElementById('hamburger'),
    sidebar: document.getElementById('sidebar'),
    sidebarOverlay: document.getElementById('sidebar-overlay'),
    postsContainer: document.getElementById('posts-container'),
    errorMessage: document.getElementById('error-message')
};

// ===================================
// Mobile Navigation
// ===================================

/**
 * Toggle sidebar visibility on mobile
 */
function toggleSidebar() {
    const isActive = elements.sidebar.classList.toggle('active');
    elements.sidebarOverlay.classList.toggle('active');

    // Update ARIA attribute
    elements.hamburger.setAttribute('aria-expanded', isActive);

    // Prevent body scroll when sidebar is open
    document.body.style.overflow = isActive ? 'hidden' : '';
}

/**
 * Close sidebar (mobile only)
 */
function closeSidebar() {
    elements.sidebar.classList.remove('active');
    elements.sidebarOverlay.classList.remove('active');
    elements.hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
}

/**
 * Handle window resize - close sidebar on mobile when resizing to desktop
 */
function handleResize() {
    if (window.innerWidth > 768) {
        closeSidebar();
    }
}

// Event Listeners for Navigation
if (elements.hamburger) {
    elements.hamburger.addEventListener('click', toggleSidebar);
}

if (elements.sidebarOverlay) {
    elements.sidebarOverlay.addEventListener('click', closeSidebar);
}

// Close sidebar when clicking on navigation links (mobile)
const navLinks = document.querySelectorAll('.sidebar-nav a, .about-link');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            closeSidebar();
        }
    });
});

// Handle window resize
window.addEventListener('resize', handleResize);

// Close sidebar on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && elements.sidebar.classList.contains('active')) {
        closeSidebar();
    }
});

// ===================================
// Posts Loading
// ===================================

/**
 * Fetch posts from published_urls.json
 * @returns {Promise<Array>} Array of post objects
 */
async function fetchPosts() {
    try {
        const response = await fetch(CONFIG.postsJsonPath);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.posts || [];
    } catch (error) {
        console.error('Error fetching posts:', error);
        throw error;
    }
}

/**
 * Create HTML for a single post card
 * @param {Object} post - Post object from JSON
 * @returns {string} HTML string for post card
 */
function createPostCard(post) {
    // Truncate intro if needed
    const intro = post.intro && post.intro.length > CONFIG.defaultIntroLength
        ? post.intro.substring(0, CONFIG.defaultIntroLength) + '...'
        : post.intro || 'Read this post to discover more...';

    return `
        <article class="post-card">
            <h3 class="post-title">
                <a href="${post.url}" target="_blank" rel="noopener noreferrer">
                    ${escapeHtml(post.title)}
                </a>
            </h3>
            <p class="post-intro">${escapeHtml(intro)}</p>
            <a href="${post.url}" class="post-read-more" target="_blank" rel="noopener noreferrer">
                Read more →
            </a>
        </article>
    `;
}

/**
 * Render posts to the DOM
 * @param {Array} posts - Array of post objects
 */
function renderPosts(posts) {
    if (!posts || posts.length === 0) {
        elements.postsContainer.innerHTML = `
            <div class="loading">No posts available yet. Check back soon!</div>
        `;
        return;
    }

    // Get recent posts (limit to CONFIG.maxRecentPosts)
    const recentPosts = posts.slice(0, CONFIG.maxRecentPosts);

    // Generate HTML for all posts
    const postsHtml = recentPosts.map(post => createPostCard(post)).join('');

    // Update DOM
    elements.postsContainer.innerHTML = postsHtml;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    elements.postsContainer.style.display = 'none';
    elements.errorMessage.style.display = 'block';
    elements.errorMessage.querySelector('p').textContent = message;
}

/**
 * Initialize posts loading
 */
async function initPosts() {
    try {
        const posts = await fetchPosts();
        renderPosts(posts);
    } catch (error) {
        console.error('Failed to load posts:', error);
        showError('Unable to load posts. Please try again later.');
    }
}

// ===================================
// Utility Functions
// ===================================

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Smooth scroll to element
 * @param {string} targetId - ID of target element
 */
function smoothScroll(targetId) {
    const target = document.getElementById(targetId);
    if (target) {
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Handle anchor links with smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const targetId = href.substring(1);
            smoothScroll(targetId);
        }
    });
});

// ===================================
// Initialize on DOM Ready
// ===================================

// Load posts when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPosts);
} else {
    // DOM already loaded
    initPosts();
}

// ===================================
// Performance Monitoring (Development)
// ===================================

if (window.performance && window.performance.timing) {
    window.addEventListener('load', () => {
        const timing = window.performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);

        // Check if we meet performance target (<1500ms)
        if (loadTime > 1500) {
            console.warn('Page load time exceeds target (1500ms)');
        } else {
            console.log('✅ Page load time meets performance target');
        }
    });
}
