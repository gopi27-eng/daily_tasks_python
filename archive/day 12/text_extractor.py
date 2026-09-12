import cv2
import pandas as pd
import pytesseract
import os 
from logging_utils.log import setup_logger

logger = setup_logger("ocr_pipeline.log")

def image_to_text_extractor(image_dir: str, csv_file: str):
    records = []
    
    for filename in os.listdir(image_dir):
        # 1. Match the generator's file format
        if filename.endswith(".png"):
            image_path = os.path.join(image_dir, filename)
            logger.info(f"Processing {image_path}")
            
            image = cv2.imread(image_path)
            
            # 2. Fix OpenCV syntax
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            # 3. Fix Tesseract syntax
            extracted_text = pytesseract.image_to_string(gray).strip()
            
            # 4. Append as a dictionary for clean Pandas columns
            records.append({
                "filename": filename, 
                "extracted_text": extracted_text
            })
            
    df = pd.DataFrame(records)
    df.to_csv(csv_file, index=False)
    logger.success(f"✅ OCR results saved to {csv_file}")
    
if __name__ == "__main__":
    image_to_text_extractor("images", "cargo_labels_text.csv")