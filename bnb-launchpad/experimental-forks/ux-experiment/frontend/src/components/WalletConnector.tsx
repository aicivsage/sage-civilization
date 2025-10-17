import React, { Fragment, useState } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { ChevronDownIcon, WalletIcon } from '@heroicons/react/24/outline';
import { formatAddress, formatBNB } from '../utils/formatters';
import { WalletType } from '../utils/constants';
import { WalletModal } from './WalletModal';
import toast from 'react-hot-toast';

interface WalletConnectorProps {
  account: string | null;
  balance: string;
  chainId: number | null;
  isConnecting: boolean;
  walletType: WalletType | null;
  onConnect: () => void;
  onDisconnect: () => void;
  onSwitchNetwork: (chainId: number) => void;
}

export const WalletConnector: React.FC<WalletConnectorProps> = ({
  account,
  balance,
  chainId,
  isConnecting,
  walletType,
  onConnect,
  onDisconnect,
  onSwitchNetwork,
}) => {
  const [showModal, setShowModal] = useState(false);
  const isCorrectNetwork = chainId === 97;

  const handleConnect = async () => {
    try {
      toast.loading('Opening MetaMask...', { id: 'wallet' });
      await onConnect();
      toast.success('Wallet connected! (Balance may take a moment to load)', { id: 'wallet', duration: 4000 });
      setShowModal(false);
    } catch (error: any) {
      console.error('Wallet connection error:', error);
      let message = 'Failed to connect wallet';
      if (error.message?.includes('User rejected')) {
        message = 'Connection rejected in wallet';
      } else if (error.message?.includes('missing trie node')) {
        message = 'Connected! (BSC Testnet RPC is slow, balance will load shortly)';
        toast.success(message, { id: 'wallet', duration: 5000 });
        setShowModal(false);
        return; // Don't show error
      } else if (error.message) {
        message = error.message;
      }
      toast.error(message, { id: 'wallet' });
    }
  };

  if (!account) {
    return (
      <>
        <button
          onClick={() => setShowModal(true)}
          disabled={isConnecting}
          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-secondary
                     text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          <WalletIcon className="w-5 h-5" />
          <span>{isConnecting ? 'Connecting...' : 'Connect Wallet'}</span>
        </button>

        <WalletModal
          isOpen={showModal}
          onClose={() => setShowModal(false)}
          onConnect={handleConnect}
          isConnecting={isConnecting}
          account={account}
        />
      </>
    );
  }

  return (
    <div className="flex items-center gap-3">
      {/* Network Indicator */}
      {!isCorrectNetwork && (
        <button
          onClick={() => onSwitchNetwork(97)}
          className="px-3 py-1 bg-red-500 text-white text-sm rounded-md hover:bg-red-600 transition-colors"
        >
          Switch to BSC Testnet
        </button>
      )}

      {/* Wallet Info Dropdown */}
      <Menu as="div" className="relative">
        <Menu.Button className="flex items-center gap-2 px-4 py-2 bg-dark-card text-white rounded-lg
                                hover:bg-dark-hover transition-colors">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="hidden md:block text-sm text-gray-300">
              {formatBNB(balance)} BNB
            </span>
            <span className="font-mono text-sm">{formatAddress(account)}</span>
          </div>
          <ChevronDownIcon className="w-4 h-4" />
        </Menu.Button>

        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <Menu.Items className="absolute right-0 mt-2 w-56 origin-top-right rounded-lg bg-dark-card
                                 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
            <div className="p-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-gray-400">Balance</span>
                <span className="text-sm font-semibold text-white">
                  {formatBNB(balance, 6)} BNB
                </span>
              </div>

              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-gray-400">Network</span>
                <span className="text-sm text-white">
                  {isCorrectNetwork ? 'BSC Testnet' : `Chain ${chainId}`}
                </span>
              </div>

              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-gray-400">Wallet</span>
                <span className="text-sm text-white">{walletType}</span>
              </div>

              <div className="border-t border-gray-700 pt-3 mt-3">
                <a
                  href={`https://testnet.bscscan.com/address/${account}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full px-3 py-2 text-sm text-center text-primary hover:bg-dark-hover
                           rounded-md transition-colors mb-2"
                >
                  View on BSCScan
                </a>

                <button
                  onClick={onDisconnect}
                  className="block w-full px-3 py-2 text-sm text-center text-red-400 hover:bg-dark-hover
                           rounded-md transition-colors"
                >
                  Disconnect
                </button>
              </div>
            </div>
          </Menu.Items>
        </Transition>
      </Menu>
    </div>
  );
};
