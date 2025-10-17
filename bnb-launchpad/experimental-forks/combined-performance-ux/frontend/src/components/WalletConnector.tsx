import React, { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { ChevronDownIcon, WalletIcon } from '@heroicons/react/24/outline';
import { formatAddress, formatBNB } from '../utils/formatters';
import { WalletType } from '../utils/constants';

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
  const isCorrectNetwork = chainId === 97;

  if (!account) {
    return (
      <button
        onClick={onConnect}
        disabled={isConnecting}
        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-primary to-secondary
                   text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
      >
        <WalletIcon className="w-5 h-5" />
        <span>{isConnecting ? 'Connecting...' : 'Connect Wallet'}</span>
      </button>
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
                                 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
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
