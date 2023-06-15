import ctypes
import ctypes.wintypes
import sys

if sys.platform !=  'win32':
    raise Exception('The test_mouse_win module should only be loaded on a Windows system.')

user32 = ctypes.windll.user32

# Get mouse's position

def get_mouse_position():
    cursor = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)

# Set mouse's position

def set_mouse_position(x, y):
    user32.SetCursorPos(x, y)

# Hide or Show the mouse cursor

def set_mouse_visible(is_visible):
    try:
        user32.ShowCursor(is_visible)
    except Exception as e:
        if(is_visible):
            print("Failed to show mouse cursor:", str(e))
        else:
            print("Failed to hide mouse cursor:", str(e))
            
def change_mouse_cursor(cursor_shape):
    try:
        cursor_handle = ctypes.windll.user32.LoadCursorW(None, cursor_shape)
        user32.SetCursor(cursor_handle)
    except Exception as e:
        print("Failed to change cursor shape:", str(e))
    
