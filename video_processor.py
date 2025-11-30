import cv2
import pytesseract
from PIL import Image
import numpy as np
import os
import time


# 🚨 CONFIGURATION SECTION 🚨
X_START_PERCENT = 500  
X_END_PERCENT = 1000 
Y_START_PERCENT = 150 
Y_END_PERCENT = 950   

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 


# --- Diagnostic Check and Tesseract Command Setup ---
if not os.path.exists(TESSERACT_PATH):
    print(f"\n🚨 CRITICAL ERROR: Tesseract executable NOT FOUND at: {TESSERACT_PATH}")
    print("Verify TESSERACT_PATH. Falling back to system PATH.")
    TESSERACT_PATH = '' 
elif TESSERACT_PATH:
    try:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    except Exception as e:
        print(f"\n🚨 WARNING: Could not set Tesseract command explicitly: {e}")
# ---------------------------------------------------


def preprocess_frame(frame):
    """Applies basic image processing (grayscale and thresholding) for better OCR."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    return thresh

def clean_and_format_code(raw_snippets, language):
    """
    Cleans up OCR output by removing duplicates and adding basic formatting.
    """

    unique_lines = set(raw_snippets)
    
    clean_output = ""
    for line in unique_lines:
        line = line.strip()
        
    
        line = ' '.join(line.split())
        
        if language == 'html':
            formatted_line = line.replace('><', '>\n<')
        else:
            formatted_line = line
        
        clean_output += formatted_line + "\n"
        
    return clean_output.strip()


def analyze_video_for_code(video_path, frame_interval=30):
    """
    Reads a video, extracts key frames, runs OCR on a specific ROI, and classifies the text.
    """
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return {'html': '', 'css': '', 'js': ''}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return {'html': '', 'css': '', 'js': ''}

    all_extracted_text = []
    frame_count = 0

    print(f"Starting frame extraction and OCR...")

    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    x_start = int(video_width * X_START_PERCENT / 1000)
    x_end = int(video_width * X_END_PERCENT / 1000)
    y_start = int(video_height * Y_START_PERCENT / 1000)
    y_end = int(video_height * Y_END_PERCENT / 1000)
    
    # 🚩 DIAGNOSTIC PRINT 🚩
    print(f"Cropping ROI to: X[{x_start}:{x_end}], Y[{y_start}:{y_end}]")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            
        
            cropped_frame = frame[y_start:y_end, x_start:x_end]
            processed_frame = preprocess_frame(cropped_frame)
            img_pil = Image.fromarray(processed_frame)
            
            try:
                text = pytesseract.image_to_string(img_pil, config='--psm 6')
                
                if text and len(text.strip()) > 10:
                    all_extracted_text.append(text.strip())
                    print(f"Snippet found in frame {frame_count}: {text.strip().splitlines()[0]}...")
                    
            except Exception as e:
                pass 

        frame_count += 1

    cap.release()
    print(f"Analysis complete. Total frames processed: {frame_count}. Snippets found: {len(all_extracted_text)}.")
    
    # --- Code Aggregation and Classification ---
    
    html_snippets, css_snippets, js_snippets = [], [], []
    final_html, final_css, final_js = "", "/* No distinct CSS found. */", "// No distinct JavaScript found."

    if all_extracted_text:
        
        css_snippets = [t for t in all_extracted_text if ('{' in t and '}' in t and ':' in t)]
        js_snippets = [t for t in all_extracted_text if ('function' in t or 'document.' in t or 'const' in t)]
        html_snippets = [t for t in all_extracted_text if ('<div' in t or '<h1' in t or '<p' in t or '<button' in t or '<body' in t)]
        
        if html_snippets:
            final_html = clean_and_format_code(html_snippets, 'html')
            
        if css_snippets:
            final_css = clean_and_format_code(css_snippets, 'css')
        
        if js_snippets:
            final_js = clean_and_format_code(js_snippets, 'js')
            
    
    if not html_snippets and not css_snippets and not js_snippets:
        final_html = """<h1>OCR Fallback Title V2</h1>\n<div class="ocr-fallback-box">OCR found noise or video needs clearer code.</div>"""
        final_css = """.ocr-fallback-box { background-color: darkred; color: white; padding: 10px; text-align: center;}"""
        final_js = "// Fallback: Check video quality or ROI settings."


    return {
        'html': final_html,
        'css': final_css,
        'js': final_js
    }