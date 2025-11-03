import board
import busio
import time

class 16x2lcd:
    def __init__(self):
        # Initialize I2C
        i2c = busio.I2C(board.SCL, board.SDA)
        address = 0x27  # Use 0x3F if needed

        # Wait for I2C lock
        while not i2c.try_lock():
            pass
        
        def initialise_lcd_i2c(cmd): # Throwaway function only required for initialising i2c protocol?
            # Send high nibble
            i2c.writeto(address, bytes([(cmd & 0xF0) | 0x08]))  # Data + backlight
            i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) | 0x04]))  # Enable high
            time.sleep(0.001)
            i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) & ~0x04]))  # Enable low
            # Send low nibble
            i2c.writeto(address, bytes([((cmd << 4) & 0xF0) | 0x08]))
            i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) | 0x04]))
            time.sleep(0.001)
            i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) & ~0x04]))
            time.sleep(0.001)

        # Initialization sequence
        try:
            time.sleep(0.05)
            initialise_lcd_i2c(0x33)
            initialise_lcd_i2c(0x32)
            initialise_lcd_i2c(0x28)  # 4-bit, 2-line, 5x8 font
            initialise_lcd_i2c(0x0C)  # Display on, cursor off
            initialise_lcd_i2c(0x06)  # Increment cursor
            initialise_lcd_i2c(0x01)  # Clear display
            time.sleep(0.01)
        finally:
            i2c.unloc() # Unlocking the bus, best practice

        return True

    def lcd_command(self, cmd): # Throwaway function only required for initialising i2c protocol?
        # Send high nibble
        i2c.writeto(address, bytes([(cmd & 0xF0) | 0x08]))  # Data + backlight
        i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) | 0x04]))  # Enable high
        time.sleep(0.001)
        i2c.writeto(address, bytes([((cmd & 0xF0) | 0x08) & ~0x04]))  # Enable low
        # Send low nibble
        i2c.writeto(address, bytes([((cmd << 4) & 0xF0) | 0x08]))
        i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) | 0x04]))
        time.sleep(0.001)
        i2c.writeto(address, bytes([(((cmd << 4) & 0xF0) | 0x08) & ~0x04]))
        time.sleep(0.001)

    def lcd_data_bus(self, data):
        # RS = 1 (0x01), BL = 1 (0x08) → combined as 0x09
        i2c.writeto(address, bytes([((data & 0xF0) | 0x09)]))
        i2c.writeto(address, bytes([(((data & 0xF0) | 0x09) | 0x04)]))
        time.sleep(0.001)
        i2c.writeto(address, bytes([(((data & 0xF0) | 0x09) & ~0x04)]))
        i2c.writeto(address, bytes([(((data << 4) & 0xF0) | 0x09)]))
        i2c.writeto(address, bytes([((((data << 4) & 0xF0) | 0x09) | 0x04)]))
        time.sleep(0.001)
        i2c.writeto(address, bytes([((((data << 4) & 0xF0) | 0x09) & ~0x04)]))
        time.sleep(0.001)

    def display_test_message(self):
        self.lcd_data_bus('Me when I')
        # Set cursor to second line
        self.lcd_command(0xC0)
        self.lcd_data_bus('Bottom text')

        
