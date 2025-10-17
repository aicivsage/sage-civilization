import { useState, useEffect, useCallback } from 'react';
import { ethers } from 'ethers';
import { CHAIN_CONFIG, WalletType } from '../utils/constants';

declare global {
  interface Window {
    ethereum?: any;
  }
}

export const useWallet = () => {
  const [account, setAccount] = useState<string | null>(null);
  const [provider, setProvider] = useState<ethers.providers.Web3Provider | null>(null);
  const [signer, setSigner] = useState<ethers.Signer | null>(null);
  const [chainId, setChainId] = useState<number | null>(null);
  const [balance, setBalance] = useState<string>('0');
  const [isConnecting, setIsConnecting] = useState(false);
  const [walletType, setWalletType] = useState<WalletType | null>(null);

  // Initialize provider from window.ethereum
  const initializeProvider = useCallback(async () => {
    if (window.ethereum) {
      const web3Provider = new ethers.providers.Web3Provider(window.ethereum);
      setProvider(web3Provider);

      try {
        // Check if user explicitly disconnected - if so, don't auto-reconnect
        const wasDisconnected = localStorage.getItem('walletDisconnected');
        if (wasDisconnected === 'true') {
          return; // Don't auto-reconnect if user disconnected
        }

        const accounts = await web3Provider.listAccounts();
        if (accounts.length > 0) {
          setAccount(accounts[0]);
          const signer = web3Provider.getSigner();
          setSigner(signer);

          const network = await web3Provider.getNetwork();
          setChainId(network.chainId);

          const balance = await web3Provider.getBalance(accounts[0]);
          setBalance(ethers.utils.formatEther(balance));

          setWalletType(WalletType.METAMASK);
        }
      } catch (error) {
        console.error('Error initializing provider:', error);
      }
    }
  }, []);

  // Switch network (DEFINED FIRST so connectMetaMask can use it)
  const switchNetwork = useCallback(async (targetChainId: number) => {
    if (!window.ethereum) return;

    const chainConfig = targetChainId === 97
      ? CHAIN_CONFIG.BSC_TESTNET
      : CHAIN_CONFIG.BSC_MAINNET;

    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: chainConfig.chainId }],
      });
    } catch (switchError: any) {
      // This error code indicates that the chain has not been added to MetaMask
      if (switchError.code === 4902) {
        try {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [chainConfig],
          });
        } catch (addError) {
          console.error('Error adding network:', addError);
        }
      } else {
        console.error('Error switching network:', switchError);
      }
    }
  }, []);

  // Connect to MetaMask
  const connectMetaMask = useCallback(async () => {
    if (!window.ethereum) {
      alert('Please install MetaMask!');
      return;
    }

    setIsConnecting(true);

    try {
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      const web3Provider = new ethers.providers.Web3Provider(window.ethereum);
      setProvider(web3Provider);

      const accounts = await web3Provider.listAccounts();
      setAccount(accounts[0]);

      const signer = web3Provider.getSigner();
      setSigner(signer);

      const network = await web3Provider.getNetwork();
      setChainId(network.chainId);

      // Try to get balance, but don't fail if RPC is flaky
      try {
        const balance = await web3Provider.getBalance(accounts[0]);
        setBalance(ethers.utils.formatEther(balance));
      } catch (balanceError: any) {
        console.error('Could not fetch balance (RPC may be syncing):', balanceError?.message);
        setBalance('0'); // Set to 0, will retry via auto-update interval
      }

      setWalletType(WalletType.METAMASK);
      localStorage.removeItem('walletDisconnected');

      // Switch to BSC Testnet if not already
      if (network.chainId !== 97) {
        await switchNetwork(97);
      }
    } catch (error) {
      console.error('========== METAMASK CONNECTION ERROR ==========');
      console.error('Error:', error);
      console.error('Message:', error instanceof Error ? error.message : String(error));
      console.error('Stack:', error instanceof Error ? error.stack : 'N/A');
      console.error('==============================================');
    } finally {
      setIsConnecting(false);
    }
  }, [switchNetwork]);

  // Disconnect wallet
  const disconnect = useCallback(() => {
    setAccount(null);
    setProvider(null);
    setSigner(null);
    setChainId(null);
    setBalance('0');
    setWalletType(null);
    localStorage.setItem('walletDisconnected', 'true');
  }, []);

  // Update balance (with retry for flaky RPC)
  const updateBalance = useCallback(async () => {
    if (provider && account) {
      try {
        const balance = await provider.getBalance(account);
        setBalance(ethers.utils.formatEther(balance));
      } catch (error: any) {
        console.error('========== ERROR FETCHING BALANCE ==========');
        console.error('Error:', error);
        console.error('Error message:', error?.message || String(error));

        // Check if it's the "missing trie node" RPC error
        if (error?.data?.message?.includes('missing trie node')) {
          console.error('RPC Error: BSC Testnet node sync issue');
          console.error('Will retry balance fetch...');
          // Set balance to 0 for now, will retry automatically
          setBalance('0');
        } else {
          console.error('Unexpected balance fetch error');
          console.error('Stack:', error?.stack || 'N/A');
          setBalance('0');
        }
        console.error('==========================================');
      }
    }
  }, [provider, account]);

  // Listen for account changes
  useEffect(() => {
    if (!window.ethereum) return;

    const handleAccountsChanged = (accounts: string[]) => {
      if (accounts.length === 0) {
        disconnect();
      } else if (accounts[0] !== account) {
        setAccount(accounts[0]);
        updateBalance();
      }
    };

    const handleChainChanged = (chainId: string) => {
      setChainId(parseInt(chainId, 16));
      window.location.reload();
    };

    window.ethereum.on('accountsChanged', handleAccountsChanged);
    window.ethereum.on('chainChanged', handleChainChanged);

    return () => {
      window.ethereum.removeListener('accountsChanged', handleAccountsChanged);
      window.ethereum.removeListener('chainChanged', handleChainChanged);
    };
  }, [account, disconnect, updateBalance]);

  // Initialize on mount
  useEffect(() => {
    initializeProvider();
  }, [initializeProvider]);

  // Auto-update balance every 10 seconds
  useEffect(() => {
    if (!account) return;

    const interval = setInterval(updateBalance, 10000);
    return () => clearInterval(interval);
  }, [account, updateBalance]);

  return {
    account,
    provider,
    signer,
    chainId,
    balance,
    isConnecting,
    walletType,
    isConnected: !!account,
    connectMetaMask,
    disconnect,
    switchNetwork,
    updateBalance,
  };
};
