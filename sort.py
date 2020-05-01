import os, fnmatch, re
from PIL import Image, ExifTags

imagesBaseDirectory = "/sourcedir"

for dirpath, dirnames, filenames in os.walk(imagesBaseDirectory):
    for filename in [f for f in filenames if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]:
        
        imagePath = os.path.join(dirpath, filename)
        year, month, day = None, None, None

        if re.match("\d{4}-\d{2}-\d{2}.*", filename):
            year = int(filename[:4])
            month = int(filename[5:7])
            day = int(filename[8:10])

        else:
            image = Image.open(imagePath)
            image_exif = image.getexif()
            if image_exif:
                date_taken = image_exif[36867]
                year = int(date_taken[:4])
                month = int(date_taken[5:7])
                day = int(date_taken[8:10])

        if year is not None and month is not None and day is not None:
            dirName = "/targetdir/" + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + "/"
            if not os.path.exists(dirName):
                os.makedirs(dirName)
                print("Directory " + dirName + " created")

            new_image = dirName + filename
            if not os.path.exists(new_image):
                os.rename(imagePath, new_image)
                print("moved in " + new_image)
            else:
                i = 1
                base, extension = os.path.splitext(filename)
                while True:
                    new_name = os.path.join(dirName,base, base + "_" + str(i) + extension)
                    if not os.path.exists(new_name):
                        os.rename(imagePath, new_name)
                        print("moved copy in " + new_image)
                        break 
                    i += 1