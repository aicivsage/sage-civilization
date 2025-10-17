// Global state
let walletManager = null; // WalletConnectionManager instance
let provider = null;
let signer = null;
let userAddress = null;
let factoryContract = null;
let currentTokenContract = null;
let currentTokenAddress = null;
let priceChart = null;
let volumeChart = null;
let activityLog = [];
let tokenVolumeData = {}; // Store volume data per token: { tokenAddress: [buys, sells, creatorFees, platformFees] }
let currentCandle = null; // Current candle being formed: { o, h, l, c, t }
let candleData = []; // Array of up to 5 candles

// Wait for ethers.js to load
function waitForEthers() {
    return new Promise((resolve) => {
        if (typeof ethers !== 'undefined') {
            console.log('✅ Ethers.js already loaded');
            resolve();
        } else {
            console.log('⏳ Waiting for ethers.js...');
            const checkInterval = setInterval(() => {
                if (typeof ethers !== 'undefined') {
                    console.log('✅ Ethers.js loaded');
                    clearInterval(checkInterval);
                    resolve();
                }
            }, 100);
        }
    });
}

// Initialize app
window.addEventListener('load', async () => {
    console.log('App loading...');

    // Wait for ethers to be ready
    await waitForEthers();

    initializeCharts();
    setupEventListeners();

    // Initialize WalletConnectionManager
    initializeWalletManager();
});

// Initialize WalletConnectionManager
function initializeWalletManager() {
    console.log('Initializing WalletConnectionManager...');

    walletManager = new WalletConnectionManager({
        autoConnect: true,
        supportedChainIds: ['0x38', '0x61'], // BSC Mainnet, Testnet
        preferredChainId: CONFIG.NETWORK.chainId,
        storageKey: 'bnb_launchpad_wallet',
        debug: true
    });

    // Subscribe to wallet state changes
    walletManager.onStateChange((state) => {
        console.log('Wallet state changed:', state);

        if (state.status === 'connected') {
            onWalletConnected(state.account, state.chainId);
        } else if (state.status === 'disconnected') {
            onWalletDisconnected();
        } else if (state.status === 'error') {
            console.error('Wallet error:', state.error);
            addActivity('warning', 'Wallet error: ' + state.error.message);
        }
    });

    console.log('✅ WalletConnectionManager initialized');
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('connectWallet').addEventListener('click', connectWallet);
    document.getElementById('disconnectWallet').addEventListener('click', disconnectWallet);
    document.getElementById('createTokenBtn').addEventListener('click', createToken);
    document.getElementById('refreshTokens').addEventListener('click', loadAllTokens);
    document.getElementById('tokenSelector').addEventListener('change', onTokenSelected);
    document.getElementById('buyBtn').addEventListener('click', buyTokens);
    document.getElementById('sellBtn').addEventListener('click', sellTokens);
    document.getElementById('sellMax').addEventListener('click', setSellMax);
    document.getElementById('withdrawCreatorFees').addEventListener('click', () => withdrawFees('creator'));
    document.getElementById('withdrawPlatformFees').addEventListener('click', () => withdrawFees('platform'));

    // Real-time estimates
    document.getElementById('buyAmount').addEventListener('input', updateBuyEstimate);
    document.getElementById('sellAmount').addEventListener('input', updateSellEstimate);
}

// Connect Wallet (using WalletConnectionManager)
async function connectWallet() {
    console.log('=== Connect Wallet Started ===');

    if (!walletManager) {
        console.error('WalletConnectionManager not initialized');
        alert('Wallet manager not ready. Please refresh the page.');
        return;
    }

    try {
        showLoading('Connecting wallet...');
        console.log('Requesting wallet connection via manager...');

        const result = await walletManager.connect();

        if (!result.success) {
            throw new Error(result.error);
        }

        console.log('✅ Wallet connected:', result.account);
        hideLoading();

    } catch (error) {
        hideLoading();
        console.error('Connection error:', error);
        alert('Failed to connect wallet: ' + error.message);
    }
}

// Wallet Connected Handler
async function onWalletConnected(account, chainId) {
    console.log('=== Wallet Connected ===');
    console.log('Account:', account);
    console.log('Chain ID:', chainId);

    userAddress = account;

    try {
        // Setup provider and signer (use 'any' network to avoid network change errors)
        provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
        signer = provider.getSigner();
        console.log('✅ Provider and signer created');

        // Check network
        const network = await provider.getNetwork();
        const expectedChainId = parseInt(CONFIG.NETWORK.chainId, 16);
        console.log('Network:', network.chainId, 'Expected:', expectedChainId);

        if (network.chainId !== expectedChainId) {
            console.log('Switching network...');
            await walletManager.switchChain(CONFIG.NETWORK.chainId);

            // Recreate provider after network switch
            console.log('Recreating provider after network switch...');
            provider = new ethers.providers.Web3Provider(window.ethereum, 'any');
            signer = provider.getSigner();
        }

        // Setup factory contract
        console.log('Setting up factory contract at:', CONFIG.CONTRACTS.factory);
        factoryContract = new ethers.Contract(CONFIG.CONTRACTS.factory, CONFIG.ABIS.factory, signer);
        console.log('✅ Factory contract created');

        // Update UI
        document.getElementById('connectWallet').classList.add('hidden');
        document.getElementById('walletInfo').classList.remove('hidden');
        document.getElementById('walletAddress').textContent = `${userAddress.slice(0, 6)}...${userAddress.slice(-4)}`;
        document.getElementById('networkName').textContent = CONFIG.NETWORK.name;

        await updateWalletBalance();
        await loadAllTokens();

        addActivity('success', 'Wallet connected successfully');
    } catch (error) {
        console.error('Error in onWalletConnected:', error);
        addActivity('warning', 'Connection setup failed: ' + error.message);
    }
}

// Update wallet balance
async function updateWalletBalance() {
    const balance = await provider.getBalance(userAddress);
    const balanceInBnb = ethers.utils.formatEther(balance);
    document.getElementById('walletBalance').textContent = `${parseFloat(balanceInBnb).toFixed(4)} BNB`;
}

// Disconnect wallet (using WalletConnectionManager)
function disconnectWallet() {
    if (!walletManager) {
        console.error('WalletConnectionManager not initialized');
        return;
    }

    console.log('Disconnecting wallet...');
    walletManager.disconnect();
}

// Wallet Disconnected Handler
function onWalletDisconnected() {
    console.log('=== Wallet Disconnected ===');

    // Clear all state
    provider = null;
    signer = null;
    userAddress = null;
    factoryContract = null;
    currentTokenContract = null;
    currentTokenAddress = null;
    currentCandle = null;
    candleData = [];
    tokenVolumeData = {};

    // Clear interval if running
    if (window.tokenUpdateInterval) {
        clearInterval(window.tokenUpdateInterval);
    }

    // Reset UI
    document.getElementById('connectWallet').classList.remove('hidden');
    document.getElementById('walletInfo').classList.add('hidden');
    document.getElementById('networkName').textContent = 'Not Connected';

    // Clear token selection
    document.getElementById('tokenSelector').value = '';
    document.getElementById('noTokenSelected').classList.remove('hidden');
    document.getElementById('tokenStats').classList.add('hidden');

    // Clear fee earnings
    document.getElementById('creatorFees').textContent = '0.0000 BNB';
    document.getElementById('platformFees').textContent = '0.0000 BNB';

    addActivity('info', 'Wallet disconnected');
    console.log('✅ Wallet disconnected');
}

// Create new token
async function createToken() {
    const name = document.getElementById('tokenName').value.trim();
    const symbol = document.getElementById('tokenSymbol').value.trim().toUpperCase();

    if (!name || !symbol) {
        alert('Please enter token name and symbol');
        return;
    }

    if (!signer) {
        alert('Please connect wallet first');
        return;
    }

    try {
        const statusEl = document.getElementById('createTokenStatus');
        statusEl.textContent = 'Sending transaction...';
        statusEl.className = 'text-sm text-center text-yellow-400';
        statusEl.classList.remove('hidden');

        // Call factory contract (creator is automatically msg.sender)
        const tx = await factoryContract.createToken(name, symbol);

        // Transaction sent! Update UI optimistically
        statusEl.textContent = `⏳ Confirming... (tx: ${tx.hash.slice(0, 10)}...)`;
        addActivity('info', `Token creation sent, waiting for confirmation...`);

        // Wait for confirmation (this is the slow part - 3+ seconds on BSC)
        const receipt = await tx.wait();

        // Get token address from event
        const event = receipt.events.find(e => e.event === 'TokenCreated');
        const tokenAddress = event.args.tokenAddress;

        statusEl.textContent = `✅ Token created: ${tokenAddress.slice(0, 10)}...`;
        statusEl.className = 'text-sm text-center text-green-400';

        // Clear inputs
        document.getElementById('tokenName').value = '';
        document.getElementById('tokenSymbol').value = '';

        // Reload tokens
        await loadAllTokens();

        // Select the new token
        document.getElementById('tokenSelector').value = tokenAddress;
        await onTokenSelected();

        addActivity('success', `Created ${name} (${symbol})`);

        setTimeout(() => statusEl.classList.add('hidden'), 5000);
    } catch (error) {
        console.error('Token creation error:', error);
        const statusEl = document.getElementById('createTokenStatus');
        statusEl.textContent = '❌ Failed: ' + (error.reason || error.message);
        statusEl.className = 'text-sm text-center text-red-400';
        statusEl.classList.remove('hidden');
    }
}

// Load all tokens
async function loadAllTokens() {
    if (!factoryContract) return;

    try {
        const tokens = await factoryContract.getAllTokens();
        const selector = document.getElementById('tokenSelector');

        // Clear existing options except first
        selector.innerHTML = '<option value="">-- Select a token --</option>';

        let loadedCount = 0;
        let failedCount = 0;

        // Add tokens (with error handling for each)
        for (const tokenAddress of tokens) {
            try {
                const tokenContract = new ethers.Contract(tokenAddress, CONFIG.ABIS.token, provider);
                const name = await tokenContract.name();
                const symbol = await tokenContract.symbol();

                const option = document.createElement('option');
                option.value = tokenAddress;
                option.textContent = `${name} (${symbol})`;
                selector.appendChild(option);

                loadedCount++;
            } catch (tokenError) {
                console.warn(`Failed to load token ${tokenAddress}:`, tokenError.message);
                failedCount++;

                // Add as "Unknown Token" so user can still select it
                const option = document.createElement('option');
                option.value = tokenAddress;
                option.textContent = `Token ${tokenAddress.slice(0, 8)}... (name unavailable)`;
                selector.appendChild(option);
            }
        }

        const statusMsg = failedCount > 0
            ? `Loaded ${loadedCount} tokens (${failedCount} with errors)`
            : `Loaded ${loadedCount} tokens`;

        addActivity('info', statusMsg);
    } catch (error) {
        console.error('Error loading tokens:', error);
        addActivity('warning', 'Failed to load token list');
    }
}

// Token selected
async function onTokenSelected() {
    const tokenAddress = document.getElementById('tokenSelector').value;

    if (!tokenAddress) {
        document.getElementById('noTokenSelected').classList.remove('hidden');
        document.getElementById('tokenStats').classList.add('hidden');
        currentTokenContract = null;
        currentTokenAddress = null;
        return;
    }

    currentTokenAddress = tokenAddress;
    currentTokenContract = new ethers.Contract(tokenAddress, CONFIG.ABIS.token, signer);

    // Reset candle data for new token
    currentCandle = null;
    candleData = [];
    if (priceChart) {
        priceChart.data.datasets[0].data = [];
        priceChart.update();
    }

    // Initialize or restore volume data for this token
    if (!tokenVolumeData[tokenAddress]) {
        tokenVolumeData[tokenAddress] = [0, 0, 0, 0]; // [buys, sells, creatorFees, platformFees]
    }

    // Restore volume chart data
    if (volumeChart) {
        volumeChart.data.datasets[0].data = [...tokenVolumeData[tokenAddress]];
        volumeChart.update();
    }

    document.getElementById('noTokenSelected').classList.add('hidden');
    document.getElementById('tokenStats').classList.remove('hidden');

    await updateTokenStats();
    await updateFeeEarnings();

    // Update every 10 seconds
    if (window.tokenUpdateInterval) clearInterval(window.tokenUpdateInterval);
    window.tokenUpdateInterval = setInterval(async () => {
        await updateTokenStats();
        await updateFeeEarnings();
    }, 10000);
}

// Update token stats
async function updateTokenStats() {
    if (!currentTokenContract) return;

    try {
        const [name, symbol, bnbReserves, yourBalance, status] = await Promise.all([
            currentTokenContract.name(),
            currentTokenContract.symbol(),
            currentTokenContract.bnbReserves(),
            currentTokenContract.balanceOf(userAddress),
            currentTokenContract.status()
        ]);

        // Update token info
        document.getElementById('selectedTokenName').textContent = name;
        document.getElementById('selectedTokenSymbol').textContent = symbol;

        // Update reserves
        const bnbReservesFormatted = parseFloat(ethers.utils.formatEther(bnbReserves)).toFixed(4);
        document.getElementById('bnbReserves').textContent = bnbReservesFormatted;
        document.getElementById('currentReserves').textContent = bnbReservesFormatted;

        // Update your balance
        const balanceFormatted = parseFloat(ethers.utils.formatEther(yourBalance)).toFixed(2);
        document.getElementById('yourTokenBalance').textContent = balanceFormatted;

        // Calculate current price (BNB per token)
        const totalSupply = ethers.utils.parseEther(CONFIG.CONSTANTS.TOTAL_SUPPLY);
        const virtualBnb = ethers.utils.parseEther('30');
        const currentBnbReserves = bnbReserves.add(virtualBnb);
        const K = ethers.utils.parseEther('32190005730');
        const currentTokenReserves = K.div(currentBnbReserves); // Results in "ether units" (not wei)

        // Price = BNB_reserves (wei) / token_reserves (ether units) = wei per token
        const price = currentBnbReserves.div(currentTokenReserves);
        const priceFormatted = parseFloat(ethers.utils.formatEther(price)).toFixed(8);
        document.getElementById('currentPrice').textContent = priceFormatted + ' BNB';

        // Market cap = Circulating Supply * Price
        // Circulating Supply = Total Supply - Tokens Still in Reserve
        // Note: totalSupply is in wei, currentTokenReserves is in ether units
        const totalSupplyEther = totalSupply.div(ethers.utils.parseEther('1'));
        const circulatingSupply = totalSupplyEther.sub(currentTokenReserves); // Both in ether now
        const marketCapWei = circulatingSupply.mul(price); // ether * (wei/ether) = wei
        const marketCap = parseFloat(ethers.utils.formatEther(marketCapWei));
        document.getElementById('marketCap').textContent = marketCap.toFixed(4) + ' BNB';

        // Status
        const statusText = status === 0 ? 'Trading' : (status === 1 ? 'Graduated' : 'Unknown');
        document.getElementById('tokenStatus').textContent = statusText;
        document.getElementById('tokenStatus').className = `text-lg font-bold ${status === 0 ? 'text-green-400' : 'text-blue-400'}`;

        // Graduation progress
        const progress = (parseFloat(bnbReservesFormatted) / 50) * 100;
        const progressCapped = Math.min(progress, 100);
        document.getElementById('graduationProgress').textContent = progressCapped.toFixed(1) + '%';
        document.getElementById('graduationBar').style.width = progressCapped + '%';

        // Update chart with current price
        updatePriceChart(parseFloat(priceFormatted));
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Update fee earnings
async function updateFeeEarnings() {
    if (!currentTokenContract) return;

    try {
        // First get creator and platform addresses
        const [creator, platformRecipient] = await Promise.all([
            currentTokenContract.creator(),
            currentTokenContract.platformFeeRecipient()
        ]);

        // Then query fees for the actual fee recipients
        const [creatorFees, platformFees] = await Promise.all([
            currentTokenContract.pendingFees(creator),
            currentTokenContract.pendingFees(platformRecipient)
        ]);

        // Always display both fees (not just if user is creator/platform)
        const creatorFeesFormatted = parseFloat(ethers.utils.formatEther(creatorFees)).toFixed(4);
        const platformFeesFormatted = parseFloat(ethers.utils.formatEther(platformFees)).toFixed(4);

        document.getElementById('creatorFees').textContent = creatorFeesFormatted + ' BNB';
        document.getElementById('platformFees').textContent = platformFeesFormatted + ' BNB';

        // Check if user can withdraw (is creator or platform)
        const isCreator = creator.toLowerCase() === userAddress.toLowerCase();
        const isPlatform = platformRecipient.toLowerCase() === userAddress.toLowerCase();

        // Could add UI indication here if user can withdraw
    } catch (error) {
        console.error('Error updating fees:', error);
    }
}

// Update buy estimate
async function updateBuyEstimate() {
    const buyAmount = document.getElementById('buyAmount').value;
    if (!buyAmount || !currentTokenContract) {
        document.getElementById('buyEstimate').textContent = '0 tokens';
        document.getElementById('buyFees').textContent = '0.0000 BNB';
        return;
    }

    try {
        const bnbAmount = ethers.utils.parseEther(buyAmount);

        // Calculate fees
        const totalFees = bnbAmount.mul(2).div(100); // 2% total
        const bnbAfterFees = bnbAmount.sub(totalFees);

        // Get token estimate
        const tokensOut = await currentTokenContract.calculateTokensReceived(bnbAfterFees);
        const tokensFormatted = parseFloat(ethers.utils.formatEther(tokensOut)).toFixed(0);

        document.getElementById('buyEstimate').textContent = tokensFormatted.toLocaleString() + ' tokens';
        document.getElementById('buyFees').textContent = parseFloat(ethers.utils.formatEther(totalFees)).toFixed(4) + ' BNB';
    } catch (error) {
        // Handle RPC data pruning errors gracefully
        if (error.message && error.message.includes('missing trie node')) {
            document.getElementById('buyEstimate').textContent = 'Estimate unavailable (old token)';
            document.getElementById('buyFees').textContent = '0.0000 BNB';
        } else {
            console.error('Error calculating buy estimate:', error);
            document.getElementById('buyEstimate').textContent = 'Error calculating estimate';
            document.getElementById('buyFees').textContent = '0.0000 BNB';
        }
    }
}

// Update sell estimate
async function updateSellEstimate() {
    const sellAmount = document.getElementById('sellAmount').value;
    if (!sellAmount || !currentTokenContract) {
        document.getElementById('sellEstimate').textContent = '0.0000 BNB';
        document.getElementById('sellFees').textContent = '0.0000 BNB';
        return;
    }

    try {
        const tokenAmount = ethers.utils.parseEther(sellAmount);

        // Get BNB estimate
        const bnbOut = await currentTokenContract.calculateBNBReceived(tokenAmount);

        // Calculate fees (2% of BNB out)
        const totalFees = bnbOut.mul(2).div(100);
        const bnbAfterFees = bnbOut.sub(totalFees);

        document.getElementById('sellEstimate').textContent = parseFloat(ethers.utils.formatEther(bnbAfterFees)).toFixed(4) + ' BNB';
        document.getElementById('sellFees').textContent = parseFloat(ethers.utils.formatEther(totalFees)).toFixed(4) + ' BNB';
    } catch (error) {
        // Handle RPC data pruning errors gracefully
        if (error.message && error.message.includes('missing trie node')) {
            document.getElementById('sellEstimate').textContent = 'Estimate unavailable (old token)';
            document.getElementById('sellFees').textContent = '0.0000 BNB';
        } else {
            console.error('Error calculating sell estimate:', error);
            document.getElementById('sellEstimate').textContent = 'Error calculating estimate';
            document.getElementById('sellFees').textContent = '0.0000 BNB';
        }
    }
}

// Set sell max
async function setSellMax() {
    if (!currentTokenContract) return;
    try {
        const balance = await currentTokenContract.balanceOf(userAddress);
        document.getElementById('sellAmount').value = ethers.utils.formatEther(balance);
        await updateSellEstimate();
    } catch (error) {
        console.error('Error setting max:', error);
    }
}

// Buy tokens
async function buyTokens() {
    const buyAmount = document.getElementById('buyAmount').value;

    if (!buyAmount || parseFloat(buyAmount) < 0.001) {
        alert('Minimum buy amount is 0.001 BNB');
        return;
    }

    if (!currentTokenContract) {
        alert('Please select a token first');
        return;
    }

    try {
        const statusEl = document.getElementById('buyStatus');
        statusEl.textContent = 'Sending transaction...';
        statusEl.className = 'text-sm text-center text-yellow-400';
        statusEl.classList.remove('hidden');

        const bnbAmount = ethers.utils.parseEther(buyAmount);
        const tx = await currentTokenContract.buy(0, { value: bnbAmount });

        // Transaction sent! Update UI optimistically
        statusEl.textContent = `⏳ Confirming... (tx: ${tx.hash.slice(0, 10)}...)`;
        addActivity('info', `Buy transaction sent, waiting for confirmation...`);

        // Wait for confirmation (this is the slow part - 3+ seconds on BSC)
        const receipt = await tx.wait();

        // Parse event
        const event = receipt.events.find(e => e.event === 'TokensPurchased');
        const tokensReceived = ethers.utils.formatEther(event.args.tokensReceived);

        statusEl.textContent = `✅ Bought ${parseFloat(tokensReceived).toFixed(0)} tokens!`;
        statusEl.className = 'text-sm text-center text-green-400';

        // Clear input
        document.getElementById('buyAmount').value = '';
        document.getElementById('buyEstimate').textContent = '0 tokens';

        await updateTokenStats();
        await updateWalletBalance();
        await updateFeeEarnings();

        addActivity('buy', `Bought ${parseFloat(tokensReceived).toFixed(0)} tokens for ${buyAmount} BNB`);
        updateVolumeChart('buy', parseFloat(buyAmount));

        setTimeout(() => statusEl.classList.add('hidden'), 5000);
    } catch (error) {
        console.error('Buy error:', error);
        const statusEl = document.getElementById('buyStatus');
        statusEl.textContent = '❌ Failed: ' + (error.reason || error.message);
        statusEl.className = 'text-sm text-center text-red-400';
        statusEl.classList.remove('hidden');
    }
}

// Sell tokens
async function sellTokens() {
    const sellAmount = document.getElementById('sellAmount').value;

    if (!sellAmount || parseFloat(sellAmount) < 1000) {
        alert('Minimum sell amount is 1000 tokens');
        return;
    }

    if (!currentTokenContract) {
        alert('Please select a token first');
        return;
    }

    try {
        const statusEl = document.getElementById('sellStatus');
        statusEl.textContent = 'Sending transaction...';
        statusEl.className = 'text-sm text-center text-yellow-400';
        statusEl.classList.remove('hidden');

        const tokenAmount = ethers.utils.parseEther(sellAmount);
        const tx = await currentTokenContract.sell(tokenAmount, 0);

        // Transaction sent! Update UI optimistically
        statusEl.textContent = `⏳ Confirming... (tx: ${tx.hash.slice(0, 10)}...)`;
        addActivity('info', `Sell transaction sent, waiting for confirmation...`);

        // Wait for confirmation (this is the slow part - 3+ seconds on BSC)
        const receipt = await tx.wait();

        // Parse event
        const event = receipt.events.find(e => e.event === 'TokensSold');
        const bnbReceived = ethers.utils.formatEther(event.args.bnbReturned);

        statusEl.textContent = `✅ Sold for ${parseFloat(bnbReceived).toFixed(4)} BNB!`;
        statusEl.className = 'text-sm text-center text-green-400';

        // Clear input
        document.getElementById('sellAmount').value = '';
        document.getElementById('sellEstimate').textContent = '0.0000 BNB';

        await updateTokenStats();
        await updateWalletBalance();
        await updateFeeEarnings();

        addActivity('sell', `Sold ${sellAmount} tokens for ${parseFloat(bnbReceived).toFixed(4)} BNB`);
        updateVolumeChart('sell', parseFloat(bnbReceived));

        setTimeout(() => statusEl.classList.add('hidden'), 5000);
    } catch (error) {
        console.error('Sell error:', error);
        const statusEl = document.getElementById('sellStatus');
        statusEl.textContent = '❌ Failed: ' + (error.reason || error.message);
        statusEl.className = 'text-sm text-center text-red-400';
        statusEl.classList.remove('hidden');
    }
}

// Withdraw fees
async function withdrawFees(type) {
    if (!currentTokenContract) {
        alert('Please select a token first');
        return;
    }

    try {
        showLoading(`Withdrawing ${type} fees...`);

        const tx = await currentTokenContract.withdrawFees();
        await tx.wait();

        await updateFeeEarnings();
        await updateWalletBalance();

        hideLoading();
        addActivity('success', `Withdrew ${type} fees`);
        alert(`${type} fees withdrawn successfully!`);
    } catch (error) {
        hideLoading();
        console.error('Withdraw error:', error);
        alert('Failed to withdraw fees: ' + (error.reason || error.message));
    }
}

// Initialize charts
function initializeCharts() {
    // Price chart (candlestick)
    const priceCtx = document.getElementById('priceChart').getContext('2d');
    priceChart = new Chart(priceCtx, {
        type: 'candlestick',
        data: {
            datasets: [{
                label: 'Price (BNB)',
                data: []
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                        displayFormats: {
                            minute: 'HH:mm'
                        }
                    },
                    ticks: { color: '#9ca3af' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    ticks: {
                        color: '#9ca3af',
                        callback: function(value) {
                            return value.toFixed(8);
                        }
                    },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });

    // Volume chart
    const volumeCtx = document.getElementById('volumeChart').getContext('2d');
    volumeChart = new Chart(volumeCtx, {
        type: 'bar',
        data: {
            labels: ['Buys', 'Sells', 'Creator Fees', 'Platform Fees'],
            datasets: [{
                label: 'Volume (BNB)',
                data: [0, 0, 0, 0],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(168, 85, 247, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    ticks: { color: '#9ca3af' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    ticks: {
                        color: '#9ca3af',
                        callback: function(value) {
                            // Format as BNB with proper decimals
                            if (value >= 0.01) return value.toFixed(3);
                            if (value >= 0.001) return value.toFixed(4);
                            return value.toFixed(6);
                        }
                    },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    beginAtZero: true
                }
            }
        }
    });
}

// Update price chart (candlestick with 5 candles)
function updatePriceChart(price) {
    const now = Date.now();

    // If no current candle, create one
    if (!currentCandle) {
        currentCandle = {
            x: now,
            o: price,
            h: price,
            l: price,
            c: price,
            updates: 1
        };
    } else {
        // Update current candle
        currentCandle.h = Math.max(currentCandle.h, price);
        currentCandle.l = Math.min(currentCandle.l, price);
        currentCandle.c = price;
        currentCandle.updates++;

        // Close candle after 3 updates (each buy/sell creates new candle)
        if (currentCandle.updates >= 3) {
            // Add completed candle to array
            candleData.push({
                x: currentCandle.x,
                o: currentCandle.o,
                h: currentCandle.h,
                l: currentCandle.l,
                c: currentCandle.c
            });

            // Keep only 5 candles
            if (candleData.length > 5) {
                candleData.shift();
            }

            // Start new candle
            currentCandle = {
                x: now,
                o: price,
                h: price,
                l: price,
                c: price,
                updates: 1
            };
        }
    }

    // Update chart with all candles (completed + current)
    const allCandles = [...candleData];
    if (currentCandle) {
        allCandles.push({
            x: currentCandle.x,
            o: currentCandle.o,
            h: currentCandle.h,
            l: currentCandle.l,
            c: currentCandle.c
        });
    }

    priceChart.data.datasets[0].data = allCandles;
    priceChart.update('none'); // 'none' for performance
}

// Update volume chart
function updateVolumeChart(type, amount) {
    if (!currentTokenAddress || !volumeChart) return;

    if (type === 'buy') {
        volumeChart.data.datasets[0].data[0] += amount;
        // Calculate fees (1% creator + 1% platform on the BNB amount BEFORE the buy)
        const creatorFee = amount * 0.01;
        const platformFee = amount * 0.01;
        volumeChart.data.datasets[0].data[2] += creatorFee;
        volumeChart.data.datasets[0].data[3] += platformFee;
    } else if (type === 'sell') {
        volumeChart.data.datasets[0].data[1] += amount;
        // Calculate fees (1% creator + 1% platform on the BNB amount RETURNED)
        const creatorFee = amount * 0.01;
        const platformFee = amount * 0.01;
        volumeChart.data.datasets[0].data[2] += creatorFee;
        volumeChart.data.datasets[0].data[3] += platformFee;
    }

    // Save updated data to storage
    tokenVolumeData[currentTokenAddress] = [...volumeChart.data.datasets[0].data];

    volumeChart.update();
}

// Add activity
function addActivity(type, message) {
    const activity = {
        type,
        message,
        time: new Date().toLocaleTimeString()
    };
    activityLog.unshift(activity);

    const feed = document.getElementById('activityFeed');

    // Clear "no activity" message
    if (activityLog.length === 1) {
        feed.innerHTML = '';
    }

    // Add new activity
    const colors = {
        success: 'text-green-400',
        buy: 'text-green-400',
        sell: 'text-red-400',
        info: 'text-blue-400',
        warning: 'text-yellow-400'
    };

    const icons = {
        success: '✅',
        buy: '📈',
        sell: '📉',
        info: 'ℹ️',
        warning: '⚠️'
    };

    const item = document.createElement('div');
    item.className = `bg-gray-700 rounded-lg p-3 text-sm ${colors[type] || 'text-gray-400'}`;
    item.innerHTML = `
        <div class="flex items-start">
            <span class="text-xl mr-2">${icons[type] || '•'}</span>
            <div class="flex-1">
                <div>${message}</div>
                <div class="text-xs text-gray-400 mt-1">${activity.time}</div>
            </div>
        </div>
    `;

    feed.insertBefore(item, feed.firstChild);

    // Keep max 50 items
    while (feed.children.length > 50) {
        feed.removeChild(feed.lastChild);
    }
}

// Show loading
function showLoading(message) {
    document.getElementById('loadingText').textContent = message;
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

// Hide loading
function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}
