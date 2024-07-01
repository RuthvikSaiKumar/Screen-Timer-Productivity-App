import os
import win32com.client

#Call this function to add the application to the startup folder
def add_to_startup():
    app_path = os.path.dirname(__file__)
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, 'ReConnect.lnk')

    # Create a shortcut to the application executable
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = os.path.join(app_path, 'ReConnect.bat')
    shortcut.WorkingDirectory = app_path
    shortcut.Description = 'Your App'
    shortcut.IconLocation = os.path.join(app_path, 'your_app.ico')
    shortcut.save()

#Call this function to remove the application from the startup folder
def remove_from_startup():
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, 'ReConnect.lnk')
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)