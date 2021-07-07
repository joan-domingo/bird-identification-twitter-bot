import os
from PIL import Image
import glob

dataset_dirname = "dataset"

def read_images():
    image_list = []

    for filename in glob.glob('./dataset/*/*.jpg'):
        if "_full.jpg" in filename:
            print(filename)
            os.remove(filename)
        else:
            image_list.append(filename)

    print(len(image_list))

def read_classes():
    dirfiles = os.listdir(dataset_dirname)
    fullpaths = map(lambda name: os.path.join(dataset_dirname, name), dirfiles)
    dirs = []

    for file in fullpaths:
        if os.path.isdir(file):
            class_name = file.split("/")[1]
            #print(class_name)
            dirs.append(class_name)

    return dirs

def main():
    return read_classes();

main()