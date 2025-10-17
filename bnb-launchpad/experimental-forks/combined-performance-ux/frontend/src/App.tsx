import React, { useState, useCallback, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { WalletConnector } from './components/WalletConnector';
import { PriceChart } from './components/PriceChart';
import { TradingPanel } from './components/TradingPanel';
import { TokenSelector } from './components/TokenSelector';
import { TokenCreator } from './components/TokenCreator';
import { useWallet } from './hooks/useWallet';
import { useWebSocket } from './hooks/useWebSocket';
import { useContract } from './hooks/useContract';
import './index.css';

function App() {
  const [selectedToken, setSelectedToken] = useState<string | null>(null);
  const [tokenList, setTokenList] = useState<any[]>([]);
  const [tokenBalance, setTokenBalance] = useState('0');

  // Hooks
  const wallet = useWallet();
  const { priceData, trades, newTokens, connected: wsConnected } = useWebSocket(selectedToken);
  const contract = useContract(wallet.provider, wallet.signer);

  // Auto-update token balance when wallet account or selected token changes
  useEffect(() => {
    const updateBalance = async () => {
      if (wallet.account && selectedToken && contract.getTokenBalance) {
        try {
          const balance = await contract.getTokenBalance(selectedToken, wallet.account);
          setTokenBalance(balance);
        } catch (error) {
          console.error('Error updating balance:', error);
          setTokenBalance('0');
        }
      } else {
        setTokenBalance('0');
      }
    };

    updateBalance();
  }, [wallet.account, selectedToken, contract.getTokenBalance]);

  // Load all tokens
  const loadTokens = useCallback(async () => {
    if (!contract.factoryContract) return;

    try {
      const addresses = await contract.getAllTokens();
      const tokenData = await Promise.all(
        addresses.map(async (address: string) => {
          const info = await contract.getTokenInfo(address);
          return {
            address,
            name: info?.name || 'Unknown',
            symbol: info?.symbol || 'UNK',
          };
        })
      );
      setTokenList(tokenData);
    } catch (error) {
      console.error('Error loading tokens:', error);
    }
  }, [contract]);

  // Handle token selection
  const handleSelectToken = useCallback(
    async (address: string) => {
      setSelectedToken(address);

      if (wallet.account) {
        const balance = await contract.getTokenBalance(address, wallet.account);
        setTokenBalance(balance);
      }
    },
    [wallet.account, contract]
  );

  // Handle buy
  const handleBuy = useCallback(
    async (amount: string) => {
      if (!selectedToken) throw new Error('No token selected');

      try {
        await contract.buyTokens(selectedToken, amount);

        // Update balance
        if (wallet.account) {
          const balance = await contract.getTokenBalance(selectedToken, wallet.account);
          setTokenBalance(balance);
          wallet.updateBalance();
        }
      } catch (error: any) {
        console.error('Error in handleBuy:', error);
        // Re-throw so UI component can show toast
        throw error;
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [selectedToken, contract, wallet.account]
  );

  // Handle sell
  const handleSell = useCallback(
    async (amount: string) => {
      if (!selectedToken) throw new Error('No token selected');

      try {
        await contract.sellTokens(selectedToken, amount);

        // Update balance
        if (wallet.account) {
          const balance = await contract.getTokenBalance(selectedToken, wallet.account);
          setTokenBalance(balance);
          wallet.updateBalance();
        }
      } catch (error: any) {
        console.error('Error in handleSell:', error);
        // Re-throw so UI component can show toast
        throw error;
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [selectedToken, contract, wallet.account]
  );

  // Handle create token
  const handleCreateToken = useCallback(
    async (name: string, symbol: string) => {
      try {
        const result = await contract.createToken(name, symbol);

        // Reload tokens after creation
        await loadTokens();

        // Auto-select the new token
        if (result.tokenAddress) {
          setSelectedToken(result.tokenAddress);

          // Update balance
          if (wallet.account) {
            const balance = await contract.getTokenBalance(result.tokenAddress, wallet.account);
            setTokenBalance(balance);
          }
        }
      } catch (error: any) {
        console.error('Error in handleCreateToken:', error);
        // Re-throw so UI component can show toast
        throw error;
      }
    },
    [contract, loadTokens, wallet.account]
  );

  return (
    <div className="min-h-screen bg-dark-bg">
      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 5000,
          style: {
            background: '#2B2B43',
            color: '#fff',
          },
        }}
      />

      {/* Header */}
      <header className="bg-dark-card border-b border-gray-800">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-primary to-secondary rounded-lg
                           flex items-center justify-center">
                <span className="text-white font-bold text-xl">B</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">BNB Launchpad</h1>
                <p className="text-xs text-gray-400">Enhanced UX Fork</p>
              </div>
            </div>

            {/* Connection Status */}
            <div className="flex items-center gap-4">
              <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-dark-bg rounded-lg">
                <div className={`w-2 h-2 rounded-full ${wsConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                <span className="text-xs text-gray-400">
                  {wsConnected ? 'Live' : 'Disconnected'}
                </span>
              </div>

              <WalletConnector
                account={wallet.account}
                balance={wallet.balance}
                chainId={wallet.chainId}
                isConnecting={wallet.isConnecting}
                walletType={wallet.walletType}
                onConnect={wallet.connectMetaMask}
                onDisconnect={wallet.disconnect}
                onSwitchNetwork={wallet.switchNetwork}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Token Selector */}
          <div className="lg:col-span-1">
            <TokenSelector
              tokens={tokenList}
              newTokens={newTokens}
              selectedToken={selectedToken}
              onSelectToken={handleSelectToken}
              onLoadTokens={loadTokens}
            />

            {/* Token Creator */}
            <div className="mt-6">
              <TokenCreator
                isConnected={wallet.isConnected}
                onConnect={wallet.connectMetaMask}
                onCreate={handleCreateToken}
              />
            </div>
          </div>

          {/* Middle Column - Chart */}
          <div className="lg:col-span-1">
            <PriceChart tokenAddress={selectedToken || ''} priceData={priceData} />

            {/* Trade History */}
            <div className="bg-dark-card rounded-xl p-4 mt-6">
              <h3 className="text-lg font-semibold text-white mb-4">Recent Trades</h3>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {trades.length === 0 ? (
                  <div className="text-center py-8 text-gray-400">
                    No recent trades
                  </div>
                ) : (
                  trades.map((trade, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-2 bg-dark-bg rounded"
                    >
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2 py-1 text-xs font-semibold rounded ${
                            trade.type === 'buy'
                              ? 'bg-green-500/20 text-green-500'
                              : 'bg-red-500/20 text-red-500'
                          }`}
                        >
                          {trade.type.toUpperCase()}
                        </span>
                        <span className="text-sm text-white">
                          {trade.type === 'buy'
                            ? `${parseFloat(trade.bnbAmount || '0').toFixed(4)} BNB`
                            : `${parseFloat(trade.tokensSold || '0').toFixed(2)} tokens`}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500">
                        {new Date(trade.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Trading Panel */}
          <div className="lg:col-span-1">
            <TradingPanel
              tokenAddress={selectedToken}
              tokenSymbol={priceData?.symbol || 'TOKEN'}
              tokenBalance={tokenBalance}
              bnbBalance={wallet.balance}
              currentPrice={priceData?.price || '0'}
              isConnected={wallet.isConnected}
              onBuy={handleBuy}
              onSell={handleSell}
              onConnect={wallet.connectMetaMask}
            />

            {/* Token Info */}
            {priceData && (
              <div className="bg-dark-card rounded-xl p-4 mt-6">
                <h3 className="text-lg font-semibold text-white mb-4">Token Info</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Name</span>
                    <span className="text-sm font-semibold text-white">{priceData.name}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Symbol</span>
                    <span className="text-sm font-semibold text-white">{priceData.symbol}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Address</span>
                    <a
                      href={`https://testnet.bscscan.com/address/${priceData.address}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-mono text-primary hover:underline"
                    >
                      {priceData.address.slice(0, 6)}...{priceData.address.slice(-4)}
                    </a>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Status</span>
                    <span
                      className={`text-sm font-semibold ${
                        priceData.status === 0 ? 'text-green-500' : 'text-blue-500'
                      }`}
                    >
                      {priceData.status === 0 ? 'Active' : 'Graduated'}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-6 mt-12 border-t border-gray-800">
        <div className="text-center text-sm text-gray-400">
          <p>BNB Token Launchpad - Enhanced UX Fork</p>
          <p className="mt-1">BSC Testnet - For testing purposes only</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
