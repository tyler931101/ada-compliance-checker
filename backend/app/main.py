from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import HtmlRequest, CheckResponse
from .utils.html_parser import parse_html
from .utils.accessibility_rules import check_accessibility

app = FastAPI(
    title="ADA Compliance Checker API",
    description="API for checking HTML accessibility compliance",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ADA Compliance Checker API"}

@app.post("/check-accessibility", response_model=CheckResponse)
async def check_html_accessibility(request: HtmlRequest):
    try:
        # Parse HTML
        soup = parse_html(request.html)
        
        # Check accessibility
        violations = check_accessibility(soup)
        
        return CheckResponse(violations=violations)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing HTML: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}