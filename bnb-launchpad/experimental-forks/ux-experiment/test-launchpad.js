const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Configuration
const BASE_URL = 'http://localhost:3000';
const SCREENSHOT_DIR = path.join(__dirname, 'test-verification-screenshots');
const TEST_RESULTS = [];

// Ensure screenshot directory exists
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

// Utility function to save screenshots
async function takeScreenshot(page, name, description) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `${timestamp}-${name}.png`;
  const filepath = path.join(SCREENSHOT_DIR, filename);

  await page.screenshot({ path: filepath, fullPage: true });
  console.log(`✅ Screenshot saved: ${filename}`);
  console.log(`   Description: ${description}`);

  return { filename, filepath, description };
}

// Utility function to collect console logs and errors
function setupConsoleListeners(page, testName) {
  const consoleLogs = [];
  const consoleErrors = [];

  page.on('console', msg => {
    const type = msg.type();
    const text = msg.text();
    const location = msg.location();

    const entry = {
      type,
      text,
      location: `${location.url}:${location.lineNumber}:${location.columnNumber}`,
      timestamp: new Date().toISOString()
    };

    consoleLogs.push(entry);

    if (type === 'error' || type === 'warning') {
      consoleErrors.push(entry);
      console.log(`⚠️  Console ${type}: ${text}`);
    }
  });

  page.on('pageerror', error => {
    const errorEntry = {
      type: 'pageerror',
      message: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    };
    consoleErrors.push(errorEntry);
    console.log(`❌ Page Error: ${error.message}`);
  });

  return { consoleLogs, consoleErrors };
}

// Test 1: Initial Load
async function testInitialLoad(page) {
  console.log('\n🔍 TEST 1: Initial Load');
  console.log('='.repeat(50));

  const { consoleLogs, consoleErrors } = setupConsoleListeners(page, 'initial-load');

  try {
    console.log(`Navigating to ${BASE_URL}...`);
    await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait a bit for any async loading
    await page.waitForTimeout(2000);

    // Take screenshot
    const screenshot = await takeScreenshot(page, '01-initial-load', 'Homepage before connecting wallet');

    // Check if page loaded
    const title = await page.title();
    console.log(`Page title: ${title}`);

    // Check for main elements
    const headerExists = await page.locator('header').count() > 0;
    const connectButtonExists = await page.locator('button:has-text("Connect")').count() > 0;

    console.log(`Header exists: ${headerExists}`);
    console.log(`Connect button exists: ${connectButtonExists}`);

    // Check for runtime errors
    const hasRuntimeErrors = consoleErrors.filter(e => e.type === 'error' || e.type === 'pageerror').length > 0;

    return {
      test: 'Initial Load',
      passed: !hasRuntimeErrors && headerExists,
      screenshot,
      consoleLogs,
      consoleErrors,
      details: {
        title,
        headerExists,
        connectButtonExists,
        hasRuntimeErrors
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    return {
      test: 'Initial Load',
      passed: false,
      error: error.message,
      consoleLogs,
      consoleErrors
    };
  }
}

// Test 2: Wallet Connection Modal
async function testWalletConnectionModal(page) {
  console.log('\n🔍 TEST 2: Wallet Connection Modal');
  console.log('='.repeat(50));

  const { consoleLogs, consoleErrors } = setupConsoleListeners(page, 'wallet-modal');

  try {
    // Find and click connect wallet button
    const connectButton = page.locator('button:has-text("Connect")').first();
    const buttonExists = await connectButton.count() > 0;

    console.log(`Connect button found: ${buttonExists}`);

    if (!buttonExists) {
      throw new Error('Connect Wallet button not found');
    }

    // Take screenshot before clicking
    await takeScreenshot(page, '02-before-connect-click', 'Before clicking Connect Wallet');

    console.log('Clicking Connect Wallet button...');
    await connectButton.click();

    // Wait for modal to appear
    await page.waitForTimeout(1000);

    // Take screenshot after clicking
    const screenshot = await takeScreenshot(page, '03-wallet-modal-open', 'Wallet connection modal opened');

    // Check if modal exists
    const modalVisible = await page.locator('[role="dialog"], .modal, [class*="modal"]').count() > 0;
    const metamaskButtonExists = await page.locator('button:has-text("MetaMask")').count() > 0;

    console.log(`Modal visible: ${modalVisible}`);
    console.log(`MetaMask button exists: ${metamaskButtonExists}`);

    // Check modal styling
    const modalHasStyling = await page.evaluate(() => {
      const modal = document.querySelector('[role="dialog"], .modal, [class*="modal"]');
      if (!modal) return false;
      const styles = window.getComputedStyle(modal);
      return styles.display !== 'none' && styles.visibility !== 'hidden';
    });

    console.log(`Modal has proper styling: ${modalHasStyling}`);

    return {
      test: 'Wallet Connection Modal',
      passed: modalVisible && modalHasStyling,
      screenshot,
      consoleLogs,
      consoleErrors,
      details: {
        modalVisible,
        metamaskButtonExists,
        modalHasStyling
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    await takeScreenshot(page, '03-wallet-modal-error', `Error: ${error.message}`);
    return {
      test: 'Wallet Connection Modal',
      passed: false,
      error: error.message,
      consoleLogs,
      consoleErrors
    };
  }
}

// Test 3: Token Loading
async function testTokenLoading(page) {
  console.log('\n🔍 TEST 3: Token Loading');
  console.log('='.repeat(50));

  const { consoleLogs, consoleErrors } = setupConsoleListeners(page, 'token-loading');

  try {
    // Close modal if open
    const closeButton = page.locator('button:has-text("Close"), button[aria-label="Close"], .close, [class*="close"]').first();
    if (await closeButton.count() > 0) {
      await closeButton.click();
      await page.waitForTimeout(500);
    }

    // Look for token selector/dropdown
    console.log('Looking for token selector...');

    // Try multiple selectors
    const tokenSelector = page.locator('select, [role="combobox"], [class*="token-select"], [class*="tokenSelect"]').first();
    const tokenSelectorExists = await tokenSelector.count() > 0;

    console.log(`Token selector found: ${tokenSelectorExists}`);

    if (!tokenSelectorExists) {
      console.log('Trying to find token list or dropdown button...');
      const dropdownButton = page.locator('button:has-text("Select"), button:has-text("Token"), [class*="dropdown"]').first();
      const dropdownExists = await dropdownButton.count() > 0;

      if (dropdownExists) {
        await takeScreenshot(page, '04-before-token-dropdown', 'Before clicking token dropdown');
        console.log('Clicking dropdown button...');
        await dropdownButton.click();
        await page.waitForTimeout(1000);
      }
    }

    // Take screenshot of token area
    const screenshot = await takeScreenshot(page, '05-token-selector', 'Token selector/list area');

    // Check for token list items
    const tokenItems = await page.locator('[class*="token"], li, option').count();
    console.log(`Token items found: ${tokenItems}`);

    // Check for loading indicators
    const loadingIndicator = await page.locator('[class*="loading"], [class*="skeleton"], .spinner').count() > 0;
    console.log(`Loading indicator present: ${loadingIndicator}`);

    // Try to get token names from the page
    const tokenNames = await page.evaluate(() => {
      const elements = Array.from(document.querySelectorAll('[class*="token"] span, li span, option'));
      return elements.map(el => el.textContent.trim()).filter(text => text.length > 0).slice(0, 10);
    });

    console.log(`Token names found: ${tokenNames.length > 0 ? tokenNames.join(', ') : 'None'}`);

    return {
      test: 'Token Loading',
      passed: tokenItems > 0 || loadingIndicator,
      screenshot,
      consoleLogs,
      consoleErrors,
      details: {
        tokenSelectorExists,
        tokenItems,
        loadingIndicator,
        tokenNames
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    await takeScreenshot(page, '05-token-loading-error', `Error: ${error.message}`);
    return {
      test: 'Token Loading',
      passed: false,
      error: error.message,
      consoleLogs,
      consoleErrors
    };
  }
}

// Test 4: Chart Display
async function testChartDisplay(page) {
  console.log('\n🔍 TEST 4: Chart Display');
  console.log('='.repeat(50));

  const { consoleLogs, consoleErrors } = setupConsoleListeners(page, 'chart-display');

  try {
    // Look for chart container
    console.log('Looking for chart elements...');

    const chartCanvas = await page.locator('canvas').count();
    const chartSvg = await page.locator('svg[class*="chart"], svg[class*="recharts"]').count();
    const chartDiv = await page.locator('[class*="chart"], [id*="chart"]').count();

    console.log(`Chart canvas elements: ${chartCanvas}`);
    console.log(`Chart SVG elements: ${chartSvg}`);
    console.log(`Chart div elements: ${chartDiv}`);

    const screenshot = await takeScreenshot(page, '06-chart-area', 'Chart display area');

    // Check if chart library loaded
    const chartLibraryLoaded = await page.evaluate(() => {
      return typeof window.Recharts !== 'undefined' ||
             typeof window.Chart !== 'undefined' ||
             document.querySelector('canvas, svg[class*="chart"]') !== null;
    });

    console.log(`Chart library loaded: ${chartLibraryLoaded}`);

    return {
      test: 'Chart Display',
      passed: chartCanvas > 0 || chartSvg > 0 || chartDiv > 0,
      screenshot,
      consoleLogs,
      consoleErrors,
      details: {
        chartCanvas,
        chartSvg,
        chartDiv,
        chartLibraryLoaded
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    await takeScreenshot(page, '06-chart-error', `Error: ${error.message}`);
    return {
      test: 'Chart Display',
      passed: false,
      error: error.message,
      consoleLogs,
      consoleErrors
    };
  }
}

// Test 5: Trading Panel
async function testTradingPanel(page) {
  console.log('\n🔍 TEST 5: Trading Panel');
  console.log('='.repeat(50));

  const { consoleLogs, consoleErrors } = setupConsoleListeners(page, 'trading-panel');

  try {
    // Look for buy/sell buttons
    const buyButton = page.locator('button:has-text("Buy")').first();
    const sellButton = page.locator('button:has-text("Sell")').first();

    const buyButtonExists = await buyButton.count() > 0;
    const sellButtonExists = await sellButton.count() > 0;

    console.log(`Buy button exists: ${buyButtonExists}`);
    console.log(`Sell button exists: ${sellButtonExists}`);

    // Check button colors
    let sellButtonColor = null;
    if (sellButtonExists) {
      sellButtonColor = await sellButton.evaluate(el => {
        const styles = window.getComputedStyle(el);
        return {
          backgroundColor: styles.backgroundColor,
          color: styles.color,
          isRed: styles.backgroundColor.includes('rgb(220, 38, 38)') ||
                 styles.backgroundColor.includes('rgb(239, 68, 68)') ||
                 styles.backgroundColor.includes('red')
        };
      });
      console.log(`Sell button color: ${JSON.stringify(sellButtonColor)}`);
    }

    const screenshot = await takeScreenshot(page, '07-trading-panel', 'Trading panel with buy/sell buttons');

    // Look for input fields
    const inputFields = await page.locator('input[type="text"], input[type="number"]').count();
    console.log(`Input fields found: ${inputFields}`);

    return {
      test: 'Trading Panel',
      passed: buyButtonExists && sellButtonExists,
      screenshot,
      consoleLogs,
      consoleErrors,
      details: {
        buyButtonExists,
        sellButtonExists,
        sellButtonColor,
        inputFields
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    await takeScreenshot(page, '07-trading-panel-error', `Error: ${error.message}`);
    return {
      test: 'Trading Panel',
      passed: false,
      error: error.message,
      consoleLogs,
      consoleErrors
    };
  }
}

// Test 6: Full Page Overview
async function testFullPageOverview(page) {
  console.log('\n🔍 TEST 6: Full Page Overview');
  console.log('='.repeat(50));

  try {
    const screenshot = await takeScreenshot(page, '08-full-page-overview', 'Complete page overview');

    // Get all visible text content
    const pageText = await page.evaluate(() => {
      return document.body.innerText;
    });

    console.log(`Page text length: ${pageText.length} characters`);
    console.log('Page contains:', {
      hasConnect: pageText.includes('Connect'),
      hasToken: pageText.includes('Token') || pageText.includes('token'),
      hasBuy: pageText.includes('Buy'),
      hasSell: pageText.includes('Sell'),
      hasPrice: pageText.includes('Price') || pageText.includes('price'),
    });

    return {
      test: 'Full Page Overview',
      passed: true,
      screenshot,
      details: {
        pageTextLength: pageText.length,
        pageTextSnippet: pageText.substring(0, 500)
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    return {
      test: 'Full Page Overview',
      passed: false,
      error: error.message
    };
  }
}

// Test 7: Console Errors Final Check
async function testConsoleErrors(page) {
  console.log('\n🔍 TEST 7: Console Errors Final Check');
  console.log('='.repeat(50));

  const { consoleLogs, consoleErrors } = setupConsoleListeners(page, 'console-errors');

  try {
    // Wait a bit to collect any delayed errors
    await page.waitForTimeout(2000);

    // Get browser console
    const screenshot = await takeScreenshot(page, '09-final-state', 'Final page state');

    console.log(`Total console logs: ${consoleLogs.length}`);
    console.log(`Total console errors: ${consoleErrors.length}`);

    if (consoleErrors.length > 0) {
      console.log('\n❌ Console Errors Found:');
      consoleErrors.forEach((err, i) => {
        console.log(`  ${i + 1}. [${err.type}] ${err.text || err.message}`);
        if (err.location) console.log(`     Location: ${err.location}`);
      });
    } else {
      console.log('✅ No console errors found!');
    }

    return {
      test: 'Console Errors',
      passed: consoleErrors.length === 0,
      screenshot,
      consoleLogs,
      consoleErrors,
      details: {
        totalLogs: consoleLogs.length,
        totalErrors: consoleErrors.length
      }
    };
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    return {
      test: 'Console Errors',
      passed: false,
      error: error.message
    };
  }
}

// Main test runner
async function runTests() {
  console.log('\n');
  console.log('='.repeat(70));
  console.log('🚀 BNB LAUNCHPAD COMPREHENSIVE TEST SUITE');
  console.log('='.repeat(70));
  console.log(`Testing URL: ${BASE_URL}`);
  console.log(`Screenshot directory: ${SCREENSHOT_DIR}`);
  console.log('='.repeat(70));

  let browser;
  let page;

  try {
    // Launch browser
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    });

    page = await context.newPage();

    // Run all tests
    TEST_RESULTS.push(await testInitialLoad(page));
    TEST_RESULTS.push(await testWalletConnectionModal(page));
    TEST_RESULTS.push(await testTokenLoading(page));
    TEST_RESULTS.push(await testChartDisplay(page));
    TEST_RESULTS.push(await testTradingPanel(page));
    TEST_RESULTS.push(await testFullPageOverview(page));
    TEST_RESULTS.push(await testConsoleErrors(page));

    // Generate summary report
    console.log('\n');
    console.log('='.repeat(70));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(70));

    const passedTests = TEST_RESULTS.filter(r => r.passed).length;
    const failedTests = TEST_RESULTS.length - passedTests;

    console.log(`\nTotal Tests: ${TEST_RESULTS.length}`);
    console.log(`✅ Passed: ${passedTests}`);
    console.log(`❌ Failed: ${failedTests}`);
    console.log('\nDetailed Results:');

    TEST_RESULTS.forEach((result, i) => {
      const status = result.passed ? '✅ PASS' : '❌ FAIL';
      console.log(`  ${i + 1}. ${status} - ${result.test}`);
      if (result.error) {
        console.log(`     Error: ${result.error}`);
      }
    });

    // Collect all console errors
    const allConsoleErrors = [];
    TEST_RESULTS.forEach(result => {
      if (result.consoleErrors) {
        allConsoleErrors.push(...result.consoleErrors);
      }
    });

    // Deduplicate errors
    const uniqueErrors = [...new Map(allConsoleErrors.map(err =>
      [err.text || err.message, err]
    )).values()];

    if (uniqueErrors.length > 0) {
      console.log('\n❌ ALL CONSOLE ERRORS FOUND:');
      console.log('='.repeat(70));
      uniqueErrors.forEach((err, i) => {
        console.log(`\n${i + 1}. [${err.type}]`);
        console.log(`   Message: ${err.text || err.message}`);
        if (err.location) console.log(`   Location: ${err.location}`);
        if (err.stack) console.log(`   Stack: ${err.stack.split('\n')[0]}`);
      });
    }

    // Save detailed report
    const reportPath = path.join(SCREENSHOT_DIR, 'test-report.json');
    fs.writeFileSync(reportPath, JSON.stringify({
      timestamp: new Date().toISOString(),
      url: BASE_URL,
      summary: {
        total: TEST_RESULTS.length,
        passed: passedTests,
        failed: failedTests
      },
      tests: TEST_RESULTS,
      allConsoleErrors: uniqueErrors
    }, null, 2));

    console.log('\n='.repeat(70));
    console.log(`📄 Detailed report saved to: ${reportPath}`);
    console.log('='.repeat(70));

  } catch (error) {
    console.error(`\n❌ Fatal error: ${error.message}`);
    console.error(error.stack);
  } finally {
    if (browser) {
      await browser.close();
    }
  }

  // Exit with appropriate code
  const hasFailures = TEST_RESULTS.some(r => !r.passed);
  process.exit(hasFailures ? 1 : 0);
}

// Run the tests
runTests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
