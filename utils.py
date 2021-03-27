#app_util.py
import PySimpleGUI as sg
import ctypes
#import win32api
from datetime import date, datetime
#import psutil # for restart_program
import codecs
import app_theme as th


def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    # b= bytes base 
    # print("size:", pretty_size(1024000,b=1000,u='bytes',pre=['','kilo','mega','giga']))
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)
  
  
# https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def loadfont(fontpath, private=True, enumerable=False):

    if isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA

    elif isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)



def rot13 (string):
    string= codecs.getencoder("rot-13")(string)[0]
    return string


def get_key_of_dct(dct,value):
     return [key for key in dct if (dct[key] == value)]

#Will return true/false if darkmode is enabled and active
# call it, if it returns true, then set your apps's gui to dark mode

#https://stackoverflow.com/questions/65294987/detect-os-dark-mode-in-python/65349866#65349866
def darkmode_state(): 
    try:
        import winreg
    except ImportError:
        #print('not windows')
        return False
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        #print('cant open shit')
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                print('Darkmode Active=')
                return value == 0
        except OSError:
            #print('not windows2')
            break
    return False


def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def fix_text(input_text):
  input_text = input_text[1:] # Remove first dash
  input_text = input_text.split('_', 2)[-1] # Remove All before second underscore
  input_text=input_text.replace("_"," ") # Replace reaming underscores with spaces
  input_text = input_text[:-1] # Remove trailing dash
  input_text=input_text.upper() # For colorful
  if th.WIN_10:
    input_text=input_text.capitalize() # For win10 look
  return input_text

def get_DPI_info():
  root = sg.tk.Tk()
  screen_width = root.winfo_screenwidth()  
  screen_height = root.winfo_screenheight()
  screen_dpi = root.winfo_fpixels('1i')
  scale_amount = 96/screen_dpi    # Format your layout if when 96 DPI
  root.destroy()
  return screen_width, screen_height, screen_dpi,scale_amount

def print_DPI():
    shcore = ctypes.windll.shcore
    monitors = win32api.EnumDisplayMonitors()
    hresult = shcore.SetProcessDpiAwareness(2)
    #assert hresult == 0
    dpiX = ctypes.c_uint()
    dpiY = ctypes.c_uint()
    for i, monitor in enumerate(monitors):
        shcore.GetDpiForMonitor(
            monitor[0].handle,
            0,
            ctypes.byref(dpiX),
            ctypes.byref(dpiY)
        )
        print(f"Monitor {i} (hmonitor: {monitor[0]}) = dpiX: {dpiX.value}, dpiY: {dpiY.value}")
        #return (f"Monitor {i} (hmonitor: {monitor[0]}) = dpiX: {dpiX.value}, dpiY: {dpiY.value}")

def lengthen_string(input_string,desired_length=64): # just use columns
    if str_len < desired_length:
        str_dif=(desired_length-str_len)
        input_string=input_string.replace("_"," ")
    return input_string

def truncate(data,string_limit=21):
    info = data[:string_limit] + (data[string_limit:] and '...')
    return info

def str2bool(input_data):
  return str(input_data).lower() in ("yes", "true", "t", "1")

def encryption(message):
    return f.encrypt(message.encode()).decode()

def decryption(message):
    return f.decrypt(message.encode()).decode()

def getDate():
    today = datetime.now().strftime("%m/%d/%y %H:%M:%S")
    return today

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def get_admin():
    #print('wtf')
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('Not enough privilege, restarting...')
        import sys

        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), "", None)

        #ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, " ".join(sys.argv[1:]), "", None)

        print('did it elevate?')
        exit(0) #disabled for win32?
    else:
        print('Elevated privilege acquired')
        #exit(0)





# The following will enumarate all of the displays
# import wmi
# obj = wmi.WMI().Win32_PnPEntity(ConfigManagerErrorCode=0)

# displays = [x for x in obj if 'DISPLAY' in str(x)]

# for item in displays:
#    print(item)
