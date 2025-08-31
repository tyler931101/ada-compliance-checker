import React, { useState } from 'react';
import FileUpload from './FileUpload';

interface HtmlInputProps {
  onSubmit: (html: string) => void;
  loading: boolean;
}

const HtmlInput: React.FC<HtmlInputProps> = ({ onSubmit, loading }) => {
  const [html, setHtml] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(html);
  };

  const handleFileUpload = (content: string) => {
    setHtml(content);
  };

  const sampleHtml = `<html lang="">
<head>
<title>Pages</title>
</head>
<body>
<h1 style="color: lightgreen; background-color: green;">Welcome</h1>
<h3>Our Services</h3>
<img src="/logo.png" alt="">
<p>To learn more about our offerings, <a href="/more">click here</a></p>
</body>
</html>`;

  const loadSample = () => {
    setHtml(sampleHtml);
  };

  return (
    <div className="html-input">
      <h2>Input HTML Code</h2>
      
      <div className="input-options">
        <FileUpload onFileUpload={handleFileUpload} />
        <button 
          type="button" 
          onClick={loadSample}
          className="sample-button"
        >
          Load Sample
        </button>
      </div>
      
      <div className="or-divider">OR</div>
      
      <form onSubmit={handleSubmit}>
        <textarea
          value={html}
          onChange={(e) => setHtml(e.target.value)}
          placeholder="Paste your HTML code here..."
          rows={15}
          aria-label="HTML code input"
          className="html-textarea"
        />
        
        <button 
          type="submit" 
          disabled={loading || !html.trim()}
          className="submit-button"
        >
          {loading ? 'Checking Accessibility...' : 'Check Accessibility'}
        </button>
      </form>
    </div>
  );
};

export default HtmlInput;