# AdA Compliance Checker

## Features

- Upload or paste HTML code for analysis
- Check for common accessibility issues:
  - Missing lang attribute
  - Missing or empty title tag
  - Color contrast issues
  - Missing or too long alt text on images
  - Generic link text
  - Heading hierarchy issues
  - Multiple H1 tags
- Interactive results with code snippets
- Sample HTML loading for testing

## Technologies Used

### Backend

- FastAPI (Python web framework)
- BeautifulSoup4 (HTML parsing)
- Uvicorn (ASGI server)

### Frontend

- React with TypeScript
- CSS for styling

## Setup Instructions

### Prerequisites

- Python 3.3+
- Node.js 18+
- npm or yarn

### Backend Setup

cd backend
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

### Frontend Setup

cd frontend
npm install
npm start

## Innovative Features

File Upload: Users can upload HTML files instead of just pasting code.
Sample HTML Loading: Quick access to a sample HTML with known accessibility issues.
Interactive Results: Clicking on a violation shows detailed information and would highlight the element in a real implementation.
Comprehensive Checks: Implements all required accessibility rules plus additional checks.
Accessible UI: The interface itself follows accessibility guidelines with proper focus management and ARIA attributes.
Responsive Design: Works well on both desktop and mobile devices.

## Future Enhancements

Add HTML preview pane to visualize the code.
Implement actual element highlighting in the preview.
Add more accessibility rules (ARIA attributes, form labels, etc.).
Provide suggestions for fixing identified issues.
Add authentication and history of scans.
Export results as PDF or CSV.
