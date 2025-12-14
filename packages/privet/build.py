
import os
import shutil
from PyInstaller.__main__ import run

if __name__ == '__main__':
    # Clean up previous builds
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # Path to the main script
    main_script = 'privet/main.py'
    
    # PyInstaller options
    # --name: Name of the executable
    # --onefile: Create a single file executable
    # --add-data: Include the 'nodes' directory
    # --hidden-import: Ensure all necessary modules are included
    opts = [
        '--name=privet-executor',
        '--onefile',
        '--add-data=privet/nodes:privet/nodes',
        main_script,
    ]
    
    # Run PyInstaller
    run(opts)
