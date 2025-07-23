import platform
import PyInstaller.__main__
import os
import shutil

def build_app():
    system = platform.system()
    app_name = "Swedish Learn" if system == "Windows" else "swedish-learn"
    icon_path = "assets/icon.ico" if system == "Windows" else None
    
    PyInstaller.__main__.run([
        '--name=%s' % app_name,
        '--onefile',
        '--windowed' if system == "Windows" else '',
        '--icon=%s' % icon_path if icon_path else '',
        '--add-data=assets;assets' if os.path.exists('assets') else '',
        'main.py'
    ])
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists(f'{app_name}.spec'):
        os.remove(f'{app_name}.spec')

if __name__ == "__main__":
    build_app()