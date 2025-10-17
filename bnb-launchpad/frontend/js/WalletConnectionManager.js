/**
 * WalletConnectionManager - Production-Ready MetaMask Integration
 *
 * Fixes 5 critical bugs in original implementation:
 * 1. Double connection race condition
 * 2. Event listener memory leaks
 * 3. Orphaned provider instances
 * 4. No connection state guard
 * 5. localStorage confusion
 *
 * Based on: /guides/METAMASK-INTEGRATION-GUIDE.md
 * EIP-1193 Compliant: https://eips.ethereum.org/EIPS/eip-1193
 */

class WalletConnectionManager {
    constructor(options = {}) {
        this.options = {
            autoConnect: options.autoConnect !== false, // Default true
            supportedChainIds: options.supportedChainIds || ['0x38', '0x61'], // BSC Mainnet, Testnet
            preferredChainId: options.preferredChainId || '0x38',
            connectionTimeout: options.connectionTimeout || 30000, // 30 seconds
            storageKey: options.storageKey || 'wallet_connection_state',
            debug: options.debug || false
        };

        this.state = {
            status: 'disconnected', // 'disconnected' | 'connecting' | 'connected' | 'error'
            account: null,
            chainId: null,
            error: null
        };

        this.listeners = [];
        this.eventHandlers = {};
        this.connecting = false;

        this._log('WalletConnectionManager initialized', this.options);

        // Auto-connect on initialization if enabled
        if (this.options.autoConnect && this._shouldAutoConnect()) {
            this._silentReconnect();
        }
    }

    /**
     * Connect wallet - Shows MetaMask popup if needed
     */
    async connect() {
        // Guard: Prevent duplicate connection attempts
        if (this.connecting) {
            this._log('Connection already in progress, ignoring duplicate request');
            return { success: false, error: 'Connection already in progress' };
        }

        // Guard: Already connected
        if (this.state.status === 'connected') {
            this._log('Already connected to', this.state.account);
            return {
                success: true,
                account: this.state.account,
                chainId: this.state.chainId
            };
        }

        this.connecting = true;
        this._updateState({ status: 'connecting', error: null });

        try {
            // Check if MetaMask is installed
            if (!window.ethereum) {
                throw new Error('MetaMask not installed. Please install MetaMask extension.');
            }

            // CRITICAL: Check eth_accounts FIRST (silent, no popup)
            const existingAccounts = await this._safeRequest({ method: 'eth_accounts' });

            let accounts;
            if (existingAccounts.length > 0) {
                // Already has permission - NO POPUP
                this._log('Using existing permission, no popup needed');
                accounts = existingAccounts;
            } else {
                // No permission - REQUEST IT (shows popup)
                this._log('Requesting new permission - popup will appear');
                accounts = await this._safeRequest({ method: 'eth_requestAccounts' });
            }

            if (!accounts || accounts.length === 0) {
                throw new Error('No accounts returned from MetaMask');
            }

            const account = accounts[0];
            const chainId = await this._safeRequest({ method: 'eth_chainId' });

            // Setup event listeners (cleanup old ones first)
            this._setupEventListeners();

            // Update state
            this._updateState({
                status: 'connected',
                account: account,
                chainId: chainId,
                error: null
            });

            // Persist connection state
            this._saveConnectionState(true);

            this._log('Connected successfully:', account, 'Chain:', chainId);

            return {
                success: true,
                account: account,
                chainId: chainId
            };

        } catch (error) {
            this._log('Connection failed:', error);

            // Handle specific error codes
            let errorMessage = error.message;
            switch (error.code) {
                case 4001:
                    errorMessage = 'You rejected the connection. Please try again.';
                    break;
                case -32002:
                    errorMessage = 'A connection request is already pending. Please check MetaMask.';
                    break;
                case -32603:
                    errorMessage = 'MetaMask encountered an internal error. Please try again.';
                    break;
            }

            this._updateState({
                status: 'error',
                error: { code: error.code, message: errorMessage }
            });

            return { success: false, error: errorMessage };

        } finally {
            this.connecting = false;
        }
    }

    /**
     * Disconnect wallet - Clean up state and listeners
     */
    disconnect() {
        this._log('Disconnecting wallet');

        // Clean up event listeners
        this._cleanupEventListeners();

        // Update state
        this._updateState({
            status: 'disconnected',
            account: null,
            chainId: null,
            error: null
        });

        // Clear stored state
        this._saveConnectionState(false);
    }

    /**
     * Switch to different network
     */
    async switchChain(chainId) {
        if (!window.ethereum) {
            throw new Error('MetaMask not installed');
        }

        try {
            await this._safeRequest({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId }]
            });

            this._log('Switched to chain:', chainId);
            return { success: true };

        } catch (switchError) {
            // Error 4902: Chain not added to MetaMask yet
            if (switchError.code === 4902) {
                return this._addChain(chainId);
            }
            throw switchError;
        }
    }

    /**
     * Subscribe to state changes
     */
    onStateChange(callback) {
        this.listeners.push(callback);

        // Immediately call with current state
        callback(this.state);

        // Return unsubscribe function
        return () => {
            const index = this.listeners.indexOf(callback);
            if (index > -1) {
                this.listeners.splice(index, 1);
            }
        };
    }

    /**
     * Get current state
     */
    getState() {
        return { ...this.state };
    }

    /**
     * Cleanup - Call on page unload
     */
    cleanup() {
        this._log('Cleaning up WalletConnectionManager');
        this._cleanupEventListeners();
        this.listeners = [];
    }

    // ==================== PRIVATE METHODS ====================

    /**
     * Silent reconnection (no popup) - Used on page load
     */
    async _silentReconnect() {
        if (!window.ethereum) {
            this._log('MetaMask not installed, skipping auto-connect');
            return;
        }

        try {
            // ONLY use eth_accounts (silent check)
            const accounts = await this._safeRequest({ method: 'eth_accounts' });

            if (accounts && accounts.length > 0) {
                this._log('Auto-reconnecting to existing session (no popup)');

                const account = accounts[0];
                const chainId = await this._safeRequest({ method: 'eth_chainId' });

                // Setup event listeners
                this._setupEventListeners();

                // Update state
                this._updateState({
                    status: 'connected',
                    account: account,
                    chainId: chainId,
                    error: null
                });

                this._log('Auto-reconnected:', account);
            } else {
                this._log('No existing session, staying disconnected');
            }

        } catch (error) {
            this._log('Silent reconnect failed:', error.message);
            // Don't throw - just stay disconnected
        }
    }

    /**
     * Setup MetaMask event listeners with proper cleanup
     */
    _setupEventListeners() {
        // Clean up any existing listeners first
        this._cleanupEventListeners();

        if (!window.ethereum) return;

        // accountsChanged - User switched accounts or disconnected
        this.eventHandlers.accountsChanged = (accounts) => {
            this._log('accountsChanged event:', accounts);

            if (accounts.length === 0) {
                // User disconnected in MetaMask
                this.disconnect();
            } else {
                // User switched account
                this._updateState({
                    account: accounts[0]
                });
            }
        };

        // chainChanged - Network changed (ALWAYS reload per MetaMask recommendation)
        this.eventHandlers.chainChanged = (chainId) => {
            this._log('chainChanged event:', chainId);
            // MetaMask recommends reloading on chain change
            window.location.reload();
        };

        // connect - Provider connected
        this.eventHandlers.connect = (connectInfo) => {
            this._log('connect event:', connectInfo);
        };

        // disconnect - Provider disconnected
        this.eventHandlers.disconnect = (error) => {
            this._log('disconnect event:', error);
            this.disconnect();
        };

        // Register all listeners
        window.ethereum.on('accountsChanged', this.eventHandlers.accountsChanged);
        window.ethereum.on('chainChanged', this.eventHandlers.chainChanged);
        window.ethereum.on('connect', this.eventHandlers.connect);
        window.ethereum.on('disconnect', this.eventHandlers.disconnect);

        this._log('Event listeners registered');
    }

    /**
     * Clean up event listeners (prevents memory leaks)
     */
    _cleanupEventListeners() {
        if (!window.ethereum || !this.eventHandlers) return;

        if (this.eventHandlers.accountsChanged) {
            window.ethereum.removeListener('accountsChanged', this.eventHandlers.accountsChanged);
        }
        if (this.eventHandlers.chainChanged) {
            window.ethereum.removeListener('chainChanged', this.eventHandlers.chainChanged);
        }
        if (this.eventHandlers.connect) {
            window.ethereum.removeListener('connect', this.eventHandlers.connect);
        }
        if (this.eventHandlers.disconnect) {
            window.ethereum.removeListener('disconnect', this.eventHandlers.disconnect);
        }

        this.eventHandlers = {};
        this._log('Event listeners cleaned up');
    }

    /**
     * Update state and notify listeners
     */
    _updateState(updates) {
        this.state = { ...this.state, ...updates };

        // Notify all listeners
        this.listeners.forEach(callback => {
            try {
                callback(this.state);
            } catch (error) {
                console.error('Error in state change listener:', error);
            }
        });
    }

    /**
     * Safe RPC request with timeout
     */
    async _safeRequest(params) {
        return Promise.race([
            window.ethereum.request(params),
            new Promise((_, reject) =>
                setTimeout(() => reject(new Error('Request timeout')), this.options.connectionTimeout)
            )
        ]);
    }

    /**
     * Check if should auto-connect on load
     */
    _shouldAutoConnect() {
        try {
            const stored = localStorage.getItem(this.options.storageKey);
            if (!stored) return false;

            const data = JSON.parse(stored);
            return data.wasConnected === true;
        } catch (error) {
            this._log('Error reading stored state:', error);
            return false;
        }
    }

    /**
     * Save connection state to localStorage
     */
    _saveConnectionState(connected) {
        try {
            localStorage.setItem(
                this.options.storageKey,
                JSON.stringify({ wasConnected: connected })
            );
        } catch (error) {
            this._log('Error saving state:', error);
        }
    }

    /**
     * Add new chain to MetaMask
     */
    async _addChain(chainId) {
        const chainConfigs = {
            '0x38': {
                chainId: '0x38',
                chainName: 'BNB Smart Chain Mainnet',
                nativeCurrency: { name: 'BNB', symbol: 'BNB', decimals: 18 },
                rpcUrls: ['https://bsc-dataseed.binance.org/'],
                blockExplorerUrls: ['https://bscscan.com']
            },
            '0x61': {
                chainId: '0x61',
                chainName: 'BNB Smart Chain Testnet',
                nativeCurrency: { name: 'BNB', symbol: 'BNB', decimals: 18 },
                rpcUrls: ['https://data-seed-prebsc-1-s1.bnbchain.org:8545/'],
                blockExplorerUrls: ['https://testnet.bscscan.com']
            }
        };

        const config = chainConfigs[chainId];
        if (!config) {
            throw new Error(`Unknown chain ID: ${chainId}`);
        }

        try {
            await this._safeRequest({
                method: 'wallet_addEthereumChain',
                params: [config]
            });

            this._log('Added chain:', chainId);
            return { success: true };

        } catch (error) {
            this._log('Failed to add chain:', error);
            throw error;
        }
    }

    /**
     * Debug logging
     */
    _log(...args) {
        if (this.options.debug) {
            console.log('[WalletConnectionManager]', ...args);
        }
    }
}

// Export for use in app.js
if (typeof window !== 'undefined') {
    window.WalletConnectionManager = WalletConnectionManager;
}
