import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


# width>1205</width>
# <height>1600</height>
# <bndbox>
#     <xmin>139</xmin>
#     <ymin>309</ymin>
#     <xmax>982</xmax>
#     <ymax>1411</ymax>
# </bndbox>
# x_relative_min,y_relative_min,
# x_relative_max,y_relative_min,
# x_relative_max,y_relative_max,
# x_relative_min,y_relative_max
def xml_to_csv(path, data_type):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            width = float(root.find('size')[0].text)
            height = float(root.find('size')[1].text)
            x_min = float(member[4][0].text)/width
            y_min = float(member[4][1].text)/height
            x_max = float(member[4][2].text)/width
            y_max = float(member[4][3].text)/height

            value = (data_type,
                     root.find('filename').text,
                     member[0].text,
                     x_min,
                     y_min,
                     x_max,
                     y_min,
                     x_max,
                     y_max,
                     x_min,
                     y_min
                     )
            xml_list.append(value)
    
    xml_df = pd.DataFrame(xml_list)
    return xml_df


def main():
    data_types = ['TRAIN','TEST','VALIDATION']
    for data_type in data_types:
        image_path = os.path.join(os.getcwd(), data_type.lower())
        xml_df = xml_to_csv(image_path, data_type)
        xml_df.to_csv('{}_labels.csv'.format(data_type.lower()), index=None)
        print('Dataset has been created')

main()