from pdf2image import convert_from_path
import os 
import cv2
import numpy as np
import pytesseract


poppler_path = r'C:\Program Files\poppler-24.08.0\Library\bin' 
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

class pan_extraction():
    def __init__(self,pdf_path=None,image_path=None):
        os.makedirs("image_store", exist_ok=True)
        self.folder_path=os.path.join(os.getcwd(),"image_store")
        self.image_path= lambda x: os.path.join(self.folder_path, x)
        self.pdf_path=pdf_path 
        self.image_path_1=self.convert_image()
        self.image_path=image_path
        self.final_path=self.image_path if self.image_path is not None else self.image_path_1
        pass

    def convert_image(self):# Change to your Poppler path
        if self.pdf_path is not None:
            images = convert_from_path(self.pdf_path, poppler_path=poppler_path)
            # Save images as needed
            image_path_store=[]
            i=0
            for i, image in enumerate(images):
                i=i+1
                image.save(self.image_path(f'page_{i}.png'), 'png')
                image_path=self.image_path(f'page_{i}.png')
                image_path_store.append(image_path)
            return image_path_store[0]
        else:
            pass
            #os.path.join()

    def read_image_good_quality(self):
        image = cv2.imread(self.final_path)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        page_text = pytesseract.image_to_string(img)
        return page_text

    def  read_image_bad_quality(self):
        image = cv2.imread(self.final_path)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY)
        _,thresh4 = cv2.threshold(thresh,127,255,cv2.THRESH_TOZERO)
        page_text = pytesseract.image_to_string(thresh4)
        return page_text
    
    def final_result(self):
        if self.pdf_path or self.final_path == True:
            if self.read_image_good_quality() ==True:
                return self.read_image_good_quality()
            else:
                return self.read_image_bad_quality()
        else:
            pass
        
    def delete_files_in_directory(self):
        """Delete all files in a directory."""
        try:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    os.remove(os.path.join(root, file))
        except Exception as e:
            print(f"Error deleting files: {e}")


if __name__ == "__main__":
    path = r'C:\Users\USER\Desktop\paid_ocr\image.jpg' 
    pan_ex=pan_extraction(pdf_path=None,image_path=path)
    pan_extraction=pan_ex.final_result()
    pan_ex.delete_files_in_directory()
    print(pan_extraction)

    print("PDF pages converted to images successfully!")

