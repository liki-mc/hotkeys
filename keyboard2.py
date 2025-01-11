import ctypes
import ctypes.wintypes
import win32api
import win32con

# Function to get the character for a given virtual key code
def get_key_mapping(vk_code):
    # Create a buffer to hold the character
    buf = ctypes.create_unicode_buffer(10)
    
    # Get the keyboard layout for the current thread
    layout = win32api.GetKeyboardLayout(win32api.GetCurrentThreadId())
    
    # Create a keyboard state array
    keyboard_state = (ctypes.c_ubyte * 256)()
    
    # Call the ToUnicode function
    result = ctypes.windll.user32.ToUnicode(vk_code, 0, keyboard_state, buf, 10, 0)
    
    if result > 0:
        return buf.value
    else:
        return None

# Example: Get mappings for a range of virtual key codes
print("Virtual Key Code Mappings:")
for vk_code in range(0, 256):  # Virtual key codes range from 0 to 255
    char = get_key_mapping(vk_code)
    if char:
        print(f"VK Code: {vk_code}, Character: {repr(char)}")
        try:
            print(f"VK Code pyautogui: {ctypes.windll.user32.VkKeyScanA(ctypes.wintypes.WCHAR(char))}, Character: {repr(char)}")
        except TypeError:
            print(f"No one character unicode string: {repr(char)}")

keyboardMapping = {}
for c in range(32, 128):
    keyboardMapping[chr(c)] = ctypes.windll.user32.VkKeyScanA(ctypes.wintypes.WCHAR(chr(c)))

print(keyboardMapping)
print(keyboardMapping.get("!"))