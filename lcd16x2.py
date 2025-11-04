"""
Class for use with Circuit Playground Express for the purpose of displaying text on a 16x2 LCD

The actual 'screens' should be defined in the main process
"""

import board
import busio
import time

class LCD_16x2():
    def __init__(self):
        self.time = 20
        # Initialize I2C
        self.i2c = busio.I2C(board.SCL, board.SDA)

    def display_message(self, message, line_2=None, clear_display=False):
        address = 0x27  # Use 0x3F if needed

        # Wait for I2C lock
        while not self.i2c.try_lock():
            pass

        def lcd_command(cmd):
            # Send high nibble
            self.i2c.writeto(address, bytes([(cmd & 0xF0) | 0x08]))  # Data + backlight
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) | 0x04]))  # Enable high
            time.sleep(0.001)
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) & ~0x04]))  # Enable low
            # Send low nibble
            self.i2c.writeto(address, bytes([((cmd << 4) & 0xF0) | 0x08]))
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) | 0x04]))
            time.sleep(0.001)
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) & ~0x04]))
            time.sleep(0.001)

        def lcd_data(data):
            # RS = 1 (0x01), BL = 1 (0x08) → combined as 0x09
            self.i2c.writeto(address, bytes([((data & 0xF0) | 0x09)]))
            self.i2c.writeto(address, bytes([(((data & 0xF0) | 0x09) | 0x04)]))
            time.sleep(0.001)
            self.i2c.writeto(address, bytes([(((data & 0xF0) | 0x09) & ~0x04)]))
            self.i2c.writeto(address, bytes([(((data << 4) & 0xF0) | 0x09)]))
            self.i2c.writeto(address, bytes([((((data << 4) & 0xF0) | 0x09) | 0x04)]))
            time.sleep(0.001)
            self.i2c.writeto(address, bytes([((((data << 4) & 0xF0) | 0x09) & ~0x04)]))
            time.sleep(0.001)

        try:
            # Initialization sequence
            time.sleep(0.05)
            lcd_command(0x33)
            lcd_command(0x32)
            lcd_command(0x28)  # 4-bit, 2-line, 5x8 font
            lcd_command(0x0C)  # Display on, cursor off
            lcd_command(0x06)  # Increment cursor
            lcd_command(0x01)  # Clear display

            time.sleep(0.01)

            for char in message:
                lcd_data(ord(char))
            
            if line_2 != None:
                lcd_command(0xC0)
                for char in line_2:
                    lcd_data(ord(char))

        finally:
            self.i2c.unlock()  # Always unlock the bus   
            return None
        
    def clear_lcd(self):
        address = 0x27  # Use 0x3F if needed

        # Wait for I2C lock
        while not self.i2c.try_lock():
            pass

        def lcd_command(cmd):
            # Send high nibble
            self.i2c.writeto(address, bytes([(cmd & 0xF0) | 0x08]))  # Data + backlight
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) | 0x04]))  # Enable high
            time.sleep(0.001)
            self.i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) & ~0x04]))  # Enable low
            # Send low nibble
            self.i2c.writeto(address, bytes([((cmd << 4) & 0xF0) | 0x08]))
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) | 0x04]))
            time.sleep(0.001)
            self.i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) & ~0x04]))
            time.sleep(0.001)

        try:
            # Initialization sequence
            time.sleep(0.05)
            lcd_command(0x33)
            lcd_command(0x32)
            lcd_command(0x28)  # 4-bit, 2-line, 5x8 font
            lcd_command(0x0C)  # Display on, cursor off
            lcd_command(0x06)  # Increment cursor
            lcd_command(0x01)  # Clear display

        finally:
            self.i2c.unlock()  # Always unlock the bus   
            return None

