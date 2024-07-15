import sys, io
import easyocr

# 기본 인코딩을 UTF-8로 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def ocr_test(image_path):
    reader = easyocr.Reader(['en'])
    print("Reading image...")
    result = reader.readtext(image_path)
    print("Result:", result)

ocr_test("c:\\Users\\82104\\Desktop\\github\\OpenCV-OCR-Translate\\image\\1.jpg")

# data_manager.py

def read_text_image(cls, img_file):
    print ('[DataManager] read_text_image() called!!...')
    texts_info = cls.easyocr_reader.readtext(img_file)

    # easyocr을 통해 읽은 text를 저장
    read_texts = [t[1] for t in texts_info]

    if texts_info == None or len(read_texts) == 0:
        return None
    
    else: 
        print('[DataManager] read_text_image() texts... >>> ', read_texts)
    #     cls.folder_data.work_file.set_texts(read_texts)
    #     cls.folder_data.work_file.is_ocr_detected = True

    # print (111, cls.folder_data.work_file.texts)        # 객체 주소값
    # print (222, cls.folder_data.work_file.is_ocr_detected)

    # # i = len(cls.folder_data.work_file.texts)
    # for i in range(len(cls.folder_data.work_file.texts)):
    #     print(333, cls.folder_data.work_file.get_text(i).text)       # text 값
    