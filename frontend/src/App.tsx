import React, { useState } from 'react';
import HtmlInput from './components/HtmlInput';
import ResultsDisplay from './components/ResultDisplay';
import { Violation } from './types';
import './App.css';

const App: React.FC = () => {
  const [violations, setViolations] = useState<Violation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastHtml, setLastHtml] = useState<string>('');

  const checkAccessibility = async (html: string) => {
    setLoading(true);
    setError(null);
    setLastHtml(html);
    
    try {
      const response = await fetch('http://localhost:8000/check-accessibility', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ html }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setViolations(data.violations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleHighlight = (selector: string, codeSnippet: string) => {
    // In a real implementation, this would highlight the element in a preview
    // For this example, we'll show an alert with the selector and code
    alert(`Would highlight element with selector: ${selector}\n\nCode:\n${codeSnippet}`);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>ADA Compliance Checker</h1>
        <p>Check your HTML for accessibility issues</p>
      </header>
      
      <main className="app-main">
        <HtmlInput onSubmit={checkAccessibility} loading={loading} />
        
        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}
        
        {!loading && violations.length > 0 && (
          <ResultsDisplay violations={violations} onHighlight={handleHighlight} />
        )}
      </main>
      
      <footer className="app-footer">
        <p>Built with React and FastAPI</p>
      </footer>
    </div>
  );
};

export default App;