from PIL import ImageFont
import os

# 한글 문자열을 포함한 테스트 텍스트
test_text = "한글 테스트"

# 시스템 폰트 디렉토리 설정 (예: macOS)
if os.name == "posix":
    system_font_dir = "/System/Library/Fonts"
elif os.name == "nt":
    system_font_dir = "C:\\Windows\\Fonts"
else:
    raise OSError("Unknown operating system")

# 시스템 폰트 디렉터리에 있는 모든 폰트를 가져옴
all_fonts = [os.path.join(system_font_dir, f) for f in os.listdir(system_font_dir) if f.endswith('.ttf')]

# 한글을 지원하는 폰트를 저장할 리스트
ko_fonts = []

for font_path in all_fonts:
    try:
        # 폰트를 설정하여 해당 폰트가 한글 텍스트를 렌더링할 수 있는지 확인
        font = ImageFont.truetype(font_path, 40)
        if font.getsize(test_text)[0] > 0:
            ko_fonts.append(font_path)
    except Exception as e:
        print(f"Failed to load font {font_path}: {e}")
        pass

# 한글을 지원하는 폰트 리스트 출력
print("모든 폰트:")
for ko_font in all_fonts:
    print(ko_font)
    
print("한글을 지원하는 폰트:")    
for ko_font in ko_fonts:
    print(ko_font)


print(len(ko_font))
print(len(all_fonts))

