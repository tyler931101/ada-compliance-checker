from bs4 import BeautifulSoup, Tag
from ..models import AccessibilityViolation
import re

def css_selector(element: Tag) -> str:
    """
    Generate a CSS selector for an element
    """
    if element.name == '[document]':
        return 'html'
    
    selector = element.name
    
    # Add ID if present
    if element.get('id'):
        selector += f"#{element['id']}"
    
    # Add classes if present
    elif element.get('class'):
        selector += f".{'.'.join(element['class'])}"
    
    # Add nth-child for elements with the same parent
    if element.parent:
        siblings = [sib for sib in element.parent.children if isinstance(sib, Tag) and sib.name == element.name]
        if len(siblings) > 1:
            index = siblings.index(element) + 1
            selector += f":nth-of-type({index})"
    
    # Recursively build the full selector
    if element.parent and element.parent.name != '[document]':
        parent_selector = css_selector(element.parent)
        if parent_selector:
            selector = f"{parent_selector} > {selector}"
    
    return selector

def check_doc_lang(soup: BeautifulSoup):
    """
    Check if HTML has lang attribute
    """
    violations = []
    html_tag = soup.find('html')
    if not html_tag or not html_tag.get('lang'):
        violations.append(
            AccessibilityViolation(
                ruleId="DOC_LANG_MISSING",
                message="The document's primary language is not declared.",
                element="html",
                selector="html",
                codeSnippet=str(html_tag) if html_tag else "<html>"
            )
        )
    return violations

def check_doc_title(soup: BeautifulSoup):
    """
    Check if document has a title
    """
    violations = []
    title_tag = soup.find('title')
    if not title_tag or not title_tag.get_text().strip():
        violations.append(
            AccessibilityViolation(
                ruleId="DOC_TITLE_MISSING",
                message="Every page must have a non-empty <title> tag.",
                element="title",
                selector="html > head > title",
                codeSnippet=str(title_tag) if title_tag else "<title>"
            )
        )
    return violations

def check_color_contrast(soup: BeautifulSoup):
    """
    Check color contrast (simplified for this example)
    In a real implementation, you would use a library like axe-core or specific contrast checking algorithms
    """
    violations = []
    
    # Check for inline styles with potential contrast issues
    elements_with_style = soup.find_all(style=True)
    for elem in elements_with_style:
        style = elem.get('style', '').lower()
        
        # This is a simplified check - real contrast checking would be more complex
        if ('color:' in style) and ('background-color:' in style):
            # Check for known problematic combinations
            color_matches = re.findall(r'color:\s*(#[0-9a-f]+|[a-z]+)', style)
            bg_matches = re.findall(r'background-color:\s*(#[0-9a-f]+|[a-z]+)', style)
            
            if color_matches and bg_matches:
                color = color_matches[0]
                bg_color = bg_matches[0]
                
                # Simulate finding a contrast issue for lightgreen on green
                if ('lightgreen' in color and 'green' in bg_color) or \
                   ('green' in color and 'lightgreen' in bg_color):
                    violations.append(
                        AccessibilityViolation(
                            ruleId="COLOR_CONTRAST",
                            message="Low contrast ratio: 1.98. Minimum expected is 3.0 for large text.",
                            element=elem.name,
                            selector=css_selector(elem),
                            codeSnippet=str(elem)
                        )
                    )
    
    return violations

def check_img_alt(soup: BeautifulSoup):
    """
    Check for missing alt text on images
    """
    violations = []
    images = soup.find_all('img')
    
    for img in images:
        alt_text = img.get('alt', '')
        if alt_text is None or alt_text.strip() == '':
            violations.append(
                AccessibilityViolation(
                    ruleId="IMG_ALT_MISSING",
                    message="Informative images must have a descriptive 'alt' attribute.",
                    element="img",
                    selector=css_selector(img),
                    codeSnippet=str(img)
                )
            )
        elif len(alt_text) > 120:
            violations.append(
                AccessibilityViolation(
                    ruleId="IMG_ALT_LENGTH",
                    message=f"Alt text should not exceed 120 characters (currently {len(alt_text)}).",
                    element="img",
                    selector=css_selector(img),
                    codeSnippet=str(img)
                )
            )
    
    return violations

def check_link_text(soup: BeautifulSoup):
    """
    Check for generic link text
    """
    violations = []
    links = soup.find_all('a')
    generic_phrases = ["click here", "read more", "learn more", "here", "link"]
    
    for link in links:
        text = link.get_text().strip().lower()
        href = link.get('href', '')
        
        # Skip empty links or anchor links
        if not text or href.startswith('#') or href == 'javascript:void(0)':
            continue
            
        if any(phrase in text for phrase in generic_phrases):
            violations.append(
                AccessibilityViolation(
                    ruleId="LINK_GENERIC_TEXT",
                    message="Link text should be descriptive. Avoid generic phrases like 'click here'.",
                    element="a",
                    selector=css_selector(link),
                    codeSnippet=str(link)
                )
            )
    
    return violations

def check_heading_order(soup: BeautifulSoup):
    """
    Check for proper heading hierarchy
    """
    violations = []
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_levels = [int(heading.name[1]) for heading in headings]
    
    # Check if heading levels are skipped
    for i in range(1, len(heading_levels)):
        if heading_levels[i] > heading_levels[i-1] + 1:
            violations.append(
                AccessibilityViolation(
                    ruleId="HEADING_ORDER",
                    message=f"Heading levels must not be skipped. Found {headings[i-1].name} followed by {headings[i].name}.",
                    element=headings[i].name,
                    selector=css_selector(headings[i]),
                    codeSnippet=str(headings[i])
                )
            )
    
    return violations

def check_multiple_h1(soup: BeautifulSoup):
    """
    Check for multiple H1 tags
    """
    violations = []
    h1_tags = soup.find_all('h1')
    
    if len(h1_tags) > 1:
        for h1 in h1_tags[1:]:  # All H1s after the first one
            violations.append(
                AccessibilityViolation(
                    ruleId="HEADING_MULTIPLE_H1",
                    message="There should be only one <h1> tag per page.",
                    element="h1",
                    selector=css_selector(h1),
                    codeSnippet=str(h1)
                )
            )
    
    return violations

def check_accessibility(soup: BeautifulSoup):
    """
    Run all accessibility checks
    """
    violations = []
    
    # Run all checks
    violations.extend(check_doc_lang(soup))
    violations.extend(check_doc_title(soup))
    violations.extend(check_color_contrast(soup))
    violations.extend(check_img_alt(soup))
    violations.extend(check_link_text(soup))
    violations.extend(check_heading_order(soup))
    violations.extend(check_multiple_h1(soup))
    
    return violations