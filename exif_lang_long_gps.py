import PIL.Image
import PIL
from exif import Image
import pandas as pd
from sqlalchemy import create_engine
import os

img_path = ('C:\\zdj_kompra\\DJI_0036.JPG')

image_list = os.listdir('C:\\Users\\tekic\\Desktop\\zdj_kompra\\')
image_list = [a for a in image_list if a.endswith('JPG')]

# functions from: 
# https://medium.com/spatial-data-science/how-to-extract-gps-coordinates-from-images-in-python-e66e542af354
# author: Abdishakur

def decimal_coords(coords, ref):
 decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
 if ref == 'S' or ref == 'W':
     decimal_degrees = -decimal_degrees
 return decimal_degrees

def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print('The Image has no EXIF information')
    print(f"Image {src.name[-12:-4]}, OS Version:{img.get('software', 'Not Known')} ------")
    print(f"Was taken: {img.datetime_original}, and has coordinates:{coords}")
    return [coords,src.name[-12:-4]]

coordsy = []
for img in image_list:
    path = f'C:\\zdj_kompra\\{img}'
    x = image_coordinates(path)
    coordsy.append(x)

columns = ['coords','name']
df = pd.DataFrame(coordsy, columns=columns)

# to PostgreSQL
engine = create_engine('postgresql://logs:pass@localhost/db')
df.to_sql(name='table', schema='schema', con=engine, if_exists='replace')