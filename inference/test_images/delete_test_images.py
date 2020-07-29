import os
import yaml


with open('test_images.yml') as config_file:
  config_data = yaml.load(config_file)
    
image_dir = config_data['image_path']

print ('removing image files:', image_dir)
file_list=os.listdir(image_dir)
for file_name in file_list:
  file_delete=os.path.join(image_dir,file_name)
  os.remove(file_delete)
