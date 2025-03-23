from pathlib import Path
import os
import re

tdir = Path.home() / 'OneDrive/coursework'

pattern = re.compile(r'(\..*)')

for term_folder in tdir.glob('Term?'):
    print(term_folder)
    for root, dirs, files in os.walk(term_folder):
        proot = Path(root)
        for dir in dirs:
            match = pattern.match(dir)
            if match:
                pdir = proot / dir
                print(pdir.with_name(f'0{pdir.name}'))
                pdir.rename(pdir.with_name(f'0{pdir.name}'))
        for file in files:
            match = pattern.match(file)
            if match:
                fdir = proot / file
                print(fdir.with_name(f'0{fdir.name}'))
                fdir.rename(fdir.with_name(f'0{fdir.name}'))
