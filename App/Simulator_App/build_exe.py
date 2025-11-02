import PyInstaller.__main__
import os

def build_executable():
    args = [
        'main.py',
        '--onefile',
        '--windowed',
        '--name=TSASM',
        '--add-data=simulation_components;simulation_components',
        '--add-data=ui;ui', 
        '--add-data=utils;utils',
        '--add-data=views;views',
        '--hidden-import=tkinter',
        '--hidden-import=matplotlib',
        '--hidden-import=numpy',
        '--hidden-import=scipy',
        '--hidden-import=PIL',
        '--clean',
        '--noconfirm'
    ]
    
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_executable()