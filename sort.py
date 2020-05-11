import os, fnmatch, re, shutil, logging
from datetime import datetime
from PIL import Image, ExifTags

from pathlib import Path

currentDirectory = Path(os.path.dirname(os.path.realpath(__file__)))
logFileName = filename=datetime.now().strftime("%Y%m%d_%H%M%S") + '.log'
logFilePath = str(currentDirectory / logFileName)

imagesBaseDirectory = "/volume1/photo/sort/"
logging.basicConfig(filename=logFilePath, level=logging.DEBUG)
logging.info("Starting sort")

for dirpath, dirnames, filenames in os.walk(imagesBaseDirectory):
    if not '@eaDir' in dirpath:
        for filename in [f for f in filenames if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.JPG')]:
            
            imagePath = os.path.join(dirpath, filename)
            year, month, day = None, None, None

            if re.match("\d{4}-\d{2}-\d{2}.*", filename):
                year = int(filename[:4])
                month = int(filename[5:7])
                day = int(filename[8:10])

            else:
                try:
                    image = Image.open(imagePath)
                    image_exif = image.getexif()
                    if image_exif and 36867 in image_exif:
                        date_taken = image_exif[36867]
                        year = int(date_taken[:4])
                        month = int(date_taken[5:7])
                        day = int(date_taken[8:10])
                except IOError:
                    logging.warning("Can't open the file : " + imagePath)

            if year is not None and month is not None and day is not None:
                dirName = "/volume1/photo/" + str(year) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + "/"
                if not os.path.exists(dirName):
                    os.makedirs(dirName)
                    print("Directory " + dirName + " created")

                new_image = dirName + filename
                if not os.path.exists(new_image):
                    print("moving " + imagePath + " in " + new_image)
                    shutil.move(imagePath, new_image)
                else:
                    logging.info("Duplicate found : " + filename)
            else:
                logging.info("No date found for " + imagePath)