import os
import sys
from datetime import datetime
from PIL import Image, ExifTags
import shutil
from termcolor import colored
import random
import string
os.system('color')

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

number_of_camera_images = 0
number_of_whatsapp_images = 0
number_of_movies = 0
number_of_screenshots = 0
number_of_fails = 0

created_names = []

folder_path = os.path.join(os.path.abspath(os.getcwd()), "iphone_data")

valid_file_extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]
valid_movie_extensions = [".mov", ".MOV"]

for subfolder_path in os.listdir(folder_path):
    if(os.path.isdir(os.path.join(folder_path, subfolder_path))):
        for file_name in os.listdir(os.path.join(folder_path, subfolder_path)):
            # Create the old file path
            old_file_path = os.path.join(folder_path,subfolder_path, file_name)
            
            # Get the file extension
            file_extension = os.path.splitext(file_name)[1]


            if file_extension  in valid_file_extensions:
                # Open the image
                image = Image.open(old_file_path)

                # Get the EXIF metadata
                metadata = image._getexif()
                
                # Close the image
                image.close()

                # Check if the metadata exists
                if metadata is None or file_extension  in valid_movie_extensions:
                    time_modified = os.path.getmtime(old_file_path)
                    try:
                        date_time = datetime.fromtimestamp(time_modified).strftime("%Y%m%d-%H%M%S")
                    except:
                        number_of_fails =+ 1
                        print(f"EXIF metadata not found in file: {file_name}")
                        continue
                else:
                    # Get the date taken from the metadata
                    if 36867 in metadata.keys():
                        date_taken = metadata[36867]
                    elif 306 in metadata.keys():
                        date_taken = metadata[306]
                    else:
                        print(f"Date not found in file: {file_name}")
                        continue

                    # Get the date taken as a datetime object
                    date_taken = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S")

                    # Reformat the date taken to "YYYYMMDD-HHmmss"
                    # NOTE: Change this line to change the date/time format of the output filename
                    date_time = date_taken.strftime("%Y%m%d-%H%M%S")


            # Combine the new file name and file extension
            new_file_name = date_time + file_extension

            # Get the file extension
            file_extension = os.path.splitext(file_name)[1]

            if file_extension == ".PNG":
                temp_path = os.path.join(folder_path, "Screenshots")
                number_of_screenshots += 1
                if not os.path.exists(temp_path):
                    os.makedirs(temp_path)

            elif file_extension == ".JPG":
                    if file_name[0].isupper() & file_name[1].isupper() & file_name[2].isupper() & file_name[3].isupper():
                        temp_path = os.path.join(folder_path, "Whatsapp images")
                        if not os.path.exists(temp_path):
                            os.makedirs(temp_path)
                        number_of_whatsapp_images += 1
                    else:
                        temp_path = os.path.join(folder_path, "Camera images")
                        if not os.path.exists(temp_path):
                            os.makedirs(temp_path)
                        number_of_camera_images += 1


            elif file_extension in valid_movie_extensions:
                temp_path = os.path.join(folder_path, "Movies")
                if not os.path.exists(temp_path):
                    os.makedirs(temp_path)
                number_of_movies += 1

            else:
                print("#####################################")
                print("#####################################")
                print(file_name)
                print("#####################################")
                print("#####################################")



            # Rename the file
            try:
                if(new_file_name in created_names):
                    print(new_file_name)
                    new_file_name = new_file_name.split(".")[0] + "_" + get_random_string(4) + "." + new_file_name.split(".")[1]
                    
                created_names.append(new_file_name)
                print(created_names)

                # Create the new folder path
                new_file_path = os.path.join(temp_path, new_file_name)

                shutil.copy(old_file_path, new_file_path)
                #print(str(temp_path.split('\\')[-1]))
                #print(str(file_name) + " copied to folder: " + colored(str(temp_path.split('\\')[-1]), 'green'))
            except:
                pass

print()
print("Copied " + colored(str(number_of_camera_images), 'green') + " camera images")
print("Copied " + colored(str(number_of_whatsapp_images), 'green') + " Whatsapp images")
print("Copied " + colored(str(number_of_movies), 'green') + " movies")
print("Copied " + colored(str(number_of_screenshots), 'green') + " screenshots")
print("Failed to copy " + colored(str(number_of_fails), 'red') + " files")

input("Press Enter to continue...")