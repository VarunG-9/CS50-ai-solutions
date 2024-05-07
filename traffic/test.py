import os
data_dir = 'gtsrb'
folder_index = 2
new_data_dir = f"{data_dir}{os.sep}{folder_index}"
for files in os.walk(new_data_dir):
    print(files)
