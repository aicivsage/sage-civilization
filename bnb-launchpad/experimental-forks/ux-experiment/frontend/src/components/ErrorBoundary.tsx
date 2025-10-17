import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('========== ERROR BOUNDARY CAUGHT ERROR ==========');
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    console.error('Error stack:', error.stack);

    // Stringify full error
    try {
      console.error('Full error JSON:', JSON.stringify(error, Object.getOwnPropertyNames(error), 2));
    } catch (e) {
      console.error('Could not stringify error:', e);
    }

    console.error('Component stack:', errorInfo.componentStack);

    // Stringify errorInfo
    try {
      console.error('Full errorInfo JSON:', JSON.stringify(errorInfo, null, 2));
    } catch (e) {
      console.error('Could not stringify errorInfo:', e);
    }
    console.error('=================================================');

    this.setState({
      error,
      errorInfo,
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-dark-bg flex items-center justify-center p-4">
          <div className="bg-dark-card rounded-xl p-6 max-w-2xl w-full border border-red-500">
            <h1 className="text-2xl font-bold text-red-500 mb-4">Something went wrong</h1>

            {this.state.error && (
              <div className="mb-4">
                <h2 className="text-lg font-semibold text-white mb-2">Error Message:</h2>
                <pre className="bg-dark-bg p-3 rounded text-red-400 text-sm overflow-auto">
                  {this.state.error.toString()}
                </pre>
              </div>
            )}

            {this.state.errorInfo && (
              <div className="mb-4">
                <h2 className="text-lg font-semibold text-white mb-2">Stack Trace:</h2>
                <pre className="bg-dark-bg p-3 rounded text-gray-400 text-xs overflow-auto max-h-64">
                  {this.state.errorInfo.componentStack}
                </pre>
              </div>
            )}

            <button
              onClick={() => window.location.reload()}
              className="w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
