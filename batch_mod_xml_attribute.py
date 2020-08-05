from os import listdir
from os.path import isfile, isdir, join
import xml.etree.ElementTree as ET
import pprint


'''
Bulk edit for XML resources (vector assets)
    - Convenience tool for bulk editing 100's of SVG/XML in Android project resources
    - Finds the attribute at param 'ATTR' and replaces it with param 'RES_ID'
'''


### I/O directory prompt
print('\nDirectory of .xml drawables to copy and modify (usually ..\\main\\res\\drawable:')
DIR_INPUT = input('Enter input path\n>> ')
print('\nDirectory to write modified .xml drawables:')
DIR_OUTPUT = input('Enter output path\n>> ')

### Parameters
NAMESPACE = '{http://schemas.android.com/apk/res/android}'
ATTR = 'fillColor'                               # SVG/XML 
TARGET_ATTR = NAMESPACE + ATTR
RES_ID = '?android:attr/textColorPrimary'        # Or any other resource ID
ET.register_namespace('android','http://schemas.android.com/apk/res/android')

if not (isdir(DIR_INPUT) or isdir(DIR_OUTPUT)):
    print('Input or output paths are missing or invalid, exiting')
    exit(1)

files = [fname for fname in listdir(DIR_INPUT) if fname[-3:] == 'xml']     # All files in dir, only xml

counterFiles, counterAttrs = 0, 0
for xmlFname in files:
    absPath = DIR_INPUT + '\\' + xmlFname
    tree = ET.parse(absPath)
    root = tree.getroot()
    
    if root[0].tag != 'path':               # Skip non-vector drawables
        continue
    
    path = root.findall(".//path")          # Check under <path> tag for attribute 'android:fillColor'
    for attr in path:
        attr.set(TARGET_ATTR, RES_ID)       # Set attribute's value 'android:fillColor' to new value
        outputFname = DIR_OUTPUT + '\\' + xmlFname
        tree.write(outputFname, xml_declaration=True, encoding='utf-8', method='xml')
        counterAttrs += 1
    counterFiles += 1

print('\n> Created {} new XML files out of {} found.\nReplaced {} instances of {}.'.format(counterFiles, len(files), counterAttrs, TARGET_ATTR))