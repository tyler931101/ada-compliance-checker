import React from 'react';
import { Violation } from '../types';

interface ResultsDisplayProps {
  violations: Violation[];
  onHighlight: (selector: string, codeSnippet: string) => void;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ violations, onHighlight }) => {
  if (violations.length === 0) {
    return (
      <div className="results-display">
        <div className="success-message">
          <h2>No accessibility issues found!</h2>
          <p>The HTML code passed all the accessibility checks.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="results-display">
      <h2>Identified Issues</h2>
      <p className="violations-count">{violations.length} accessibility issue{violations.length !== 1 ? 's' : ''} found:</p>
      
      <div className="violations-list">
        {violations.map((violation, index) => (
          <div 
            key={index} 
            className="violation-item"
            onClick={() => onHighlight(violation.selector, violation.codeSnippet)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onHighlight(violation.selector, violation.codeSnippet);
              }
            }}
            tabIndex={0}
            role="button"
            aria-label={`Highlight ${violation.element} with ${violation.ruleId} issue`}
          >
            <h3 className="violation-title">
              <span className="rule-id">{violation.ruleId}</span>
              <span className="element-name">{violation.element}</span>
            </h3>
            
            <div className="violation-details">
              <p><strong>Details:</strong> {violation.message}</p>
              <p><strong>Element:</strong> <code>{violation.element}</code></p>
              <p><strong>Selector:</strong> <code>{violation.selector}</code></p>
            </div>
            
            <div className="code-snippet">
              <h4>Code Snippet:</h4>
              <pre><code>{violation.codeSnippet}</code></pre>
            </div>
            
            <div className="click-hint">Click to highlight this element</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResultsDisplay;