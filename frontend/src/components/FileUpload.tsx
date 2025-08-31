import React, { useRef } from 'react';

interface FileUploadProps {
  onFileUpload: (content: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        onFileUpload(content);
      };
      reader.readAsText(file);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept=".html,.htm"
        style={{ display: 'none' }}
        aria-hidden="true"
      />
      <button 
        type="button" 
        onClick={handleButtonClick}
        className="upload-button"
      >
        Upload HTML File
      </button>
    </div>
  );
};

export default FileUpload;