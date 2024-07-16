from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class MosaicFrame:
    root = None
    def __init__(self, mosaic):
        # top button frame
        self.mosaic_frm = ttk.Frame(mosaic)
        self.mosaic_frm.pack(padx = 2, pady = 2, fill = 'both', side = 'top')

        btn_mosaic_area = ttk.Button(self.mosaic_frm, text = '모자이크 영역 검출', command = self.text_mosaic_area)
        btn_mosaic = ttk.Button(self.mosaic_frm, text = '모자이크 하기', command = self.text_mosaic)
        btn_mosaic_area.pack(side = 'left')
        btn_mosaic.pack(side = 'left')
        
        self.mosaic_tab_down_frm = ttk.Frame(mosaic)
        self.mosaic_tab_down_frm.pack(fill = 'both', expand = True)
        
        self.text = ScrolledText(self.mosaic_tab_down_frm)
        self.text.pack(fill = 'both', expand = True)

        MosaicFrame.root = self.mosaic_frm
    
    def text_mosaic_area(self):
        self.text['state'] = 'normal'
        # ref: https://tkdocs.com/tutorial/text.html
        # 기존 글씨 삭제
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', '모자이크 영역을 검출합니다.')
        # ref: https://www.pythontutorial.net/tkinter/tkinter-text/
        # 사용자가 위젯의 내용을 변경하지 못하도록 'disabled'
        self.text['state'] = 'disabled'
    
    def text_mosaic(self):
        self.text['state'] = 'normal'
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', '이미지 보호를 위해 모자이크를 진행합니다.')
        self.text['state'] = 'disabled'