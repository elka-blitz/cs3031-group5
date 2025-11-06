from board import SCL, SDA
from busio import I2C
from time import sleep

class LCD_16x2():
    def __init__(self):
        self.time = 20
        self.i2c = I2C(SCL, SDA)

    def display_message(self, message, line_2=None, clear_display=False):
        address = 0x27  
        while not self.i2c.try_lock():
            pass

        def lcd_command(cmd):
            self.i2c.writeto(address, bytes([(cmd & 0xF0) | 0x08]))  
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) | 0x04]))  
            sleep(0.001)
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) & ~0x04]))  
            self.i2c.writeto(address, bytes([((cmd << 4) & 0xF0) | 0x08]))
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) | 0x04]))
            sleep(0.001)
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) & ~0x04]))
            sleep(0.001)

        def lcd_data(data):            
            self.i2c.writeto(address, bytes([((data & 0xF0) | 0x09)]))
            self.i2c.writeto(address, bytes([(((data & 0xF0) | 0x09) | 0x04)]))
            sleep(0.001)
            self.i2c.writeto(address, bytes([(((data & 0xF0) | 0x09) & ~0x04)]))
            self.i2c.writeto(address, bytes([(((data << 4) & 0xF0) | 0x09)]))
            self.i2c.writeto(address, bytes([((((data << 4) & 0xF0) | 0x09) | 0x04)]))
            sleep(0.001)
            self.i2c.writeto(address, bytes([((((data << 4) & 0xF0) | 0x09) & ~0x04)]))
            sleep(0.001)

        try:
            sleep(0.05)
            lcd_command(0x33)
            lcd_command(0x32)
            lcd_command(0x28)  
            lcd_command(0x0C)  
            lcd_command(0x06)  
            lcd_command(0x01)  
            sleep(0.01)

            for char in message:
                lcd_data(ord(char))

            if line_2 != None:
                lcd_command(0xC0)
                for char in line_2:
                    lcd_data(ord(char))

        finally:
            self.i2c.unlock()  
            return None
        
    def clear_lcd(self):
        address = 0x27  
        while not self.i2c.try_lock():
            pass

        def lcd_command(cmd):
            self.i2c.writeto(address, bytes([(cmd & 0xF0) | 0x08]))  
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) | 0x04]))  
            sleep(0.001)
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) & ~0x04]))  
            self.i2c.writeto(address, bytes([((cmd << 4) & 0xF0) | 0x08]))
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) | 0x04]))
            sleep(0.001)
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) & ~0x04]))
            sleep(0.001)

        try:
            sleep(0.05)
            lcd_command(0x33)
            lcd_command(0x32)
            lcd_command(0x28)  
            lcd_command(0x0C)  
            lcd_command(0x06)  
            lcd_command(0x01)  

        finally:
            self.i2c.unlock()  
            return None

