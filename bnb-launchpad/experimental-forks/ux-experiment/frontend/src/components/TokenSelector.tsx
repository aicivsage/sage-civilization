import React, { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { formatAddress, formatTimeAgo } from '../utils/formatters';
import { TokenCreatedEvent } from '../hooks/useWebSocket';

interface Token {
  address: string;
  name: string;
  symbol: string;
  creator?: string;
  timestamp?: number;
}

interface TokenSelectorProps {
  tokens: Token[];
  newTokens: TokenCreatedEvent[];
  selectedToken: string | null;
  onSelectToken: (address: string) => void;
  onLoadTokens: () => void;
}

export const TokenSelector: React.FC<TokenSelectorProps> = ({
  tokens,
  newTokens,
  selectedToken,
  onSelectToken,
  onLoadTokens,
}) => {
  const [search, setSearch] = useState('');
  const [showNewTokens, setShowNewTokens] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Load tokens on mount
  useEffect(() => {
    const loadTokensWithLoading = async () => {
      setIsLoading(true);
      try {
        await onLoadTokens();
      } finally {
        setIsLoading(false);
      }
    };
    loadTokensWithLoading();
  }, [onLoadTokens]);

  // Filter tokens
  const filteredTokens = tokens.filter((token) => {
    const searchLower = search.toLowerCase();
    return (
      token.name.toLowerCase().includes(searchLower) ||
      token.symbol.toLowerCase().includes(searchLower) ||
      token.address.toLowerCase().includes(searchLower)
    );
  });

  return (
    <div className="bg-dark-card rounded-xl p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Select Token</h3>
        <button
          onClick={() => setShowNewTokens(!showNewTokens)}
          className="relative flex items-center gap-2 px-3 py-1 bg-primary/20 text-primary
                   rounded-lg hover:bg-primary/30 transition-colors"
        >
          <SparklesIcon className="w-4 h-4" />
          <span className="text-sm">New</span>
          {newTokens.length > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs
                           rounded-full flex items-center justify-center">
              {newTokens.length}
            </span>
          )}
        </button>
      </div>

      {/* Search */}
      <div className="relative mb-4">
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search tokens..."
          className="w-full pl-10 pr-4 py-2 bg-dark-bg text-white rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* New Tokens Section */}
      {showNewTokens && newTokens.length > 0 && (
        <div className="mb-4 p-3 bg-primary/10 border border-primary/30 rounded-lg">
          <div className="text-sm font-semibold text-primary mb-2">
            Recently Created
          </div>
          <div className="space-y-2">
            {newTokens.slice(0, 5).map((token) => (
              <button
                key={token.address}
                onClick={() => {
                  onSelectToken(token.address);
                  setShowNewTokens(false);
                }}
                className="w-full p-2 bg-dark-card rounded hover:bg-dark-hover transition-colors
                         text-left"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-semibold text-white">
                      {token.name}
                    </div>
                    <div className="text-xs text-gray-400">
                      {token.symbol} · {formatAddress(token.address)}
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">
                    {formatTimeAgo(token.timestamp)}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Token List */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {isLoading ? (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="animate-pulse bg-dark-bg rounded-lg p-3">
                <div className="h-4 bg-gray-700 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-700 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        ) : filteredTokens.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            {tokens.length === 0 ? (
              <div>
                <div className="mb-2">No tokens found</div>
                <button
                  onClick={onLoadTokens}
                  className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark
                           transition-colors"
                >
                  Load Tokens
                </button>
              </div>
            ) : (
              'No matching tokens'
            )}
          </div>
        ) : (
          filteredTokens.map((token) => (
            <button
              key={token.address}
              onClick={() => onSelectToken(token.address)}
              className={`w-full p-3 rounded-lg transition-all ${
                selectedToken === token.address
                  ? 'bg-primary text-white'
                  : 'bg-dark-bg text-gray-300 hover:bg-dark-hover'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="text-left">
                  <div className="font-semibold">{token.name}</div>
                  <div className="text-sm opacity-75">
                    {token.symbol} · {formatAddress(token.address)}
                  </div>
                </div>

                {selectedToken === token.address && (
                  <div className="w-6 h-6 bg-white rounded-full flex items-center justify-center">
                    <div className="w-3 h-3 bg-primary rounded-full" />
                  </div>
                )}
              </div>
            </button>
          ))
        )}
      </div>
    </div>
  );
};
