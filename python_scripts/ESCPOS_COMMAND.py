import random
import string
#from PIL import Image
class ESCPOSManager:
    def __init__(self):
         self.command_buffer = b""  # Create an instruction buffer.

    def add_command(self, command):
        self.command_buffer += command

    def send_command(self):
        esc_data = self.command_buffer
        return esc_data

    def Prefix_command(self):
        random_id = ''.join(random.choices(string.digits, k=6))
        prefix_command = bytes([0x03, 0x00]) + random_id.encode('utf-8') + b"\x00"
        # Construct print instructions for a specific format
        self.add_command(prefix_command)

    def print_text(self, text):
        text_command = text.encode('utf-8')  # 将文本编码为字节串
        self.add_command(text_command)

    def print_barcode(self, barcode_data, barcode_type):
        barcode_types = {
            'CODE39': b"\x1Dk\x04",
            'CODE128': b"\x1Dk\x49",
            # 添加其他条码类型和相应的 ESC/POS 指令
        }
        if barcode_type in barcode_types:
            barcode_command = barcode_types[barcode_type] + barcode_data.encode('utf-8')
            self.add_command(barcode_command)
        else:
            print("Invalid barcode type")

    def set_font_size(self, size):
        """
        设置字体大小
        :param size: 字体大小，可选值为 1 到 8
        :return: 对应的 ESC/POS 指令
        """
        if size < 1 or size > 128:
            raise ValueError("Font size should be between 1 and 8")
        font_size = bytes([0x1B, 0x21, size - 1])
        # 计算对应的字体放大倍数指令
        # ESC ! n 设置字体大小，n的值为字体高度和宽度放大的倍数，取值范围是 0-7
        # 具体倍数需要根据打印机规格和支持的倍数来调整
        self.add_command(font_size)

    def set_font_big_size(self, big_size):
        """
        设置字体大小
        :param big_size:
        :param size: 字体大小，可选值为 1 到 8
        :return: 对应的 ESC/POS 指令
        """
        if big_size < 1 or big_size > 113:
            raise ValueError("Font size should be between 1 and 8")
        font_big_size = bytes([0x1D, 0x21, big_size - 1])
        self.add_command(font_big_size)

    def print_qr_code(self, data, size=8, error_correction='M'):
        """
        打印 QR Code
        :param data: 要编码的数据
        :param size: QR Code 尺寸，默认为8
        :param error_correction: 纠错级别，可选值为 L（7%），M（15%），Q（25%），H（30%），默认为 M
        :param printer: ESC/POS 打印机对象
        """
        # 纠错级别对应的 ESC/POS 指令
        error_correction_levels = {'L': 48, 'M': 49, 'Q': 50, 'H': 51}
        if error_correction not in error_correction_levels:
            raise ValueError("Error correction should be 'L', 'M', 'Q', or 'H'")

        # 设置 QR Code 的尺寸和纠错级别
        qr_code_size = bytes([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, size])
        qr_code_error_Levels = bytes(
            [0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, error_correction_levels[error_correction]])
        qr_code_data_seting = bytes([0x1D, 0x28, 0x6B, len(data) + 3, 0x00, 0x31, 0x50, 0x30])
        real_data = data.encode('utf-8')
        get_qrcode_data = bytes([0x1D, 0x28, 0x6B, 0x03, 0x00,0x31,0x51, 0x30])
        print_qrcode_seting = bytes([0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31,0x52, 0x30])
        qrcode_data = qr_code_size + qr_code_error_Levels + qr_code_data_seting + real_data +print_qrcode_seting+get_qrcode_data
        self.add_command(qrcode_data)
        # 传输数据到打印机
        # qr_code_data = bytes([0x1D, 0x28, 0x6B, len(data) + 3, 0x00, 0x31, 0x50, error_correction_levels[error_correction]])
        # qr_code_data += data.encode('utf-8')

    def cut_paper(self):
        self.add_command(b"\x1D\x41\x00")  # 切纸指令

    def feed_lines(self, num_lines):
        self.add_command(b"\x1Bd" + bytes([num_lines]))  # 进纸指令
    def Print_barcode(self,barcode_data,set_hri_position=2 ,Set_Barcode_height=64,set_barcode_width=2,set_barcode_type="CODE128"):
        Set_barcode_types = {
            'CODE39': b"\x1Dk\x04",
            'CODE128': b"\x1Dk\x49",
            # 添加其他条码类型和相应的 ESC/POS 指令
        }
        Barcode_hri = bytes([0x1d,0x48,set_hri_position])
        Barcode_height= bytes([0x1d,0x68,Set_Barcode_height])
        Barcode_width = bytes([0x1d,0x77,set_barcode_width])
        pass
    def set_line_space(self,line_space_dots):
        """
        设置行间距为  [ Line_space_dots × 纵向或横向移动单位] 点
        :param line_space_dots: 00 ≤ n ≤ 255
        :return:
        """
        self.add_command(b"\x1b\x33"+bytes([line_space_dots])) #设置行间距
    def set_default_line_space(self):
        self.add_command(b"\x1b\x32")
    def set_print_position(self,nl,nH):
        self.add_command(b"\x1b\x24"+bytes([nl,nH]))
    def set_print_bold(self,bold="bold"):
        """
        bold = normal, it is not bold,
        bold = bold ,it is bold the font
        :param bold:
        :return:
        """
        if bold == "bold":
            bold_number = 1
        elif bold == "normal":
            bold_number = 0
        else: print("you type wrong values,pls choose bold or normal")
        self.add_command(b"\x1b\x45"+bytes([bold_number]))
    def set_alignment(self,align="left"):
        if align == "left":
            self.add_command(b"\x1b\x61\x00")
        elif align == "center":
            self.add_command(b"\x1b\x61\x01")
        elif align == "right":
            self.add_command(b"\x1b\x61\x02")


    # 可以添加其他功能，如设置字体、字号、对齐方式等等
"""
1b 40 1d 48 02 1d 68 64 1d 77 02
30 0D 0A
1d 6b 00 30 31 32 33 34 35 36 37 38 39 31 00
31 0D 0A
1d 6b 01 30 32 30 30 30 30 30 30 30 30 30 00
32 0D0A
1d 6b 02 30 31 32 33 34 35 36 37 38 39 31 32 00
33 0D 0A
1d 6b 03 30 31 32 33 34 35 36 37 00
34 0D 0A
1D 6B 04 30 31 32 41 42 20 24 25 2B 2D 2E 2F 00
35 0D 0A
1d 6b 05 30 31 32 33 34 35 36 37 38 39 31 32 00
36 0D 0A
1d 6b 06 2D 31 32 42 24 2B 2D 2E 00
1d 6b 06 43 31 32 33 34 35 36 34 38 39 00

36 35 0D 0A
1d 6b 41 0c 31 32 33 34 35 36 37 38 39 30 31 32 
36 36 0D 0A
1d 6b 42 0c 30 32 33 34 35 36 30 30 30 30 38 39 
36 37 0D 0A
1d 6b 43 0c 30 32 33 34 35 36 30 30 30 30 38 39 
36 38 0D 0A
1d 6b 44 08 30 32 33 34 35 36 30 30  
36 39 20 20 4e 4f 20 24 25 2b 2d 2e 2f 31 32 33 34 35 36 30 30 0D 0A
1d 6b 45 11 4e 4f 20 24 25 2b 2d 2e 2f 31 32 33 34 35 36 30 30
37 30 20 20 20 30 32 33 34 35 36 30 30 C5 BC CA FD 0D 0A
1d 6b 46 09 30 31 32 33 34 35 36 30 30
37 31 0d 0a
1d 6b 47 05 32 33 34 35 36
37 32 0d 0a
1d 6b 48 0b 32 33 34 35 36 41 42 2e 2f 2b 2c
37 33 0d0a
1d 6b 49 0A 7B 42 4E 6F 2E 7B 43 0C 22 38
"""