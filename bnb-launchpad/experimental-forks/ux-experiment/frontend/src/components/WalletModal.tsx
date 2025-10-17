import React from 'react';
import { LoadingState } from './LoadingState';

interface WalletModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConnect: () => Promise<void>;
  isConnecting: boolean;
  account?: string | null;
}

export const WalletModal: React.FC<WalletModalProps> = ({
  isOpen,
  onClose,
  onConnect,
  isConnecting,
  account,
}) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="bg-dark-card rounded-xl p-6 max-w-md w-full mx-4 border border-gray-700">
        <h2 className="text-2xl font-bold text-white mb-4">Connect Wallet</h2>

        {isConnecting ? (
          <div className="py-8">
            <LoadingState message="Opening MetaMask..." size="large" />
            <p className="text-center text-gray-400 text-sm mt-4">
              Please approve the connection in your wallet
            </p>
          </div>
        ) : account ? (
          <div className="space-y-4">
            <div className="bg-green-500/10 border border-green-500/50 rounded-lg p-4">
              <p className="text-green-500 font-semibold mb-2">✓ Connected</p>
              <p className="text-sm text-gray-300 font-mono break-all">{account}</p>
            </div>
            <button
              onClick={onClose}
              className="w-full py-3 bg-primary hover:bg-primary-dark rounded-lg font-semibold text-white transition-colors"
            >
              Close
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <button
              onClick={onConnect}
              className="w-full py-4 bg-gradient-to-r from-primary to-secondary hover:opacity-90 rounded-lg font-semibold flex items-center justify-center gap-3 text-white transition-opacity"
            >
              <svg className="w-6 h-6" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M36.0112 3L23.1 18.3L25.5 11L36.0112 3Z" fill="#E17726" stroke="#E17726" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M4 3L16.8 18.4L14.5 11L4 3Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M30.6 28.7L27.2 34L35.4 36.2L37.7 28.8L30.6 28.7Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M2.3 28.8L4.6 36.2L12.8 34L9.4 28.7L2.3 28.8Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12.3 17.3L10.3 20.4L18.4 20.8L18.1 12.1L12.3 17.3Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M27.7 17.3L21.8 12L21.6 20.8L29.7 20.4L27.7 17.3Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12.8 34L17.4 31.7L13.4 28.8L12.8 34Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M22.6 31.7L27.2 34L26.6 28.8L22.6 31.7Z" fill="#E27625" stroke="#E27625" strokeWidth="0.25" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Connect MetaMask
            </button>
            <p className="text-sm text-gray-400 text-center">
              Don't have MetaMask?{' '}
              <a
                href="https://metamask.io"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                Install it here
              </a>
            </p>
            <button
              onClick={onClose}
              className="w-full py-2 text-gray-400 hover:text-white transition-colors"
            >
              Cancel
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
