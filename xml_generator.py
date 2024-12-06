import xml.etree.ElementTree as ET
import math


def create_script(output_filename):
    # Create the variant element
    variant = ET.Element('variant', {"version": "1.0"})

    # Add the 'no_name' element
    no_name = ET.SubElement(variant, 'no_name', {"runtype": "CLxListVariant"})
    ET.SubElement(no_name, 'bIncludeZ', {"runtype": "bool", "value": "false"})
    ET.SubElement(no_name, 'bPFSEnabled', {"runtype": "bool", "value": "false"})

    coordinates = coordinate_generator([106464.830134385425481, 25188.343777459111152, 57159.144000000000233],
                                       [115271.169865614545415, 25203.656222540881572, 57159.144000000000233], 9)
    for index, coordinate in enumerate(coordinates):
        tag = f"Point{index:05d}"
        name = f"A{index + 1}"
        x, y, z = coordinate

        # <Point#####>
        point = ET.SubElement(no_name, tag, {"runtype": "NDSetupMultipointListItem"})
        ET.SubElement(point, 'bChecked', {"runtype": "bool", "value": "true"})
        ET.SubElement(point, 'strName', {"runtype": "CLxStringW", "value": name})
        ET.SubElement(point, 'dXPosition', {"runtype": "double", "value": f"{x:.15f}"})
        ET.SubElement(point, 'dYPosition', {"runtype": "double", "value": f"{y:.15f}"})
        ET.SubElement(point, 'dZPosition', {"runtype": "double", "value": f"{z:.15f}"})
        ET.SubElement(point, 'dPFSOffset', {"runtype": "double", "value": "-1.000000000000000"})
        ET.SubElement(point, 'baUserData', {"runtype": "CLxByteArray", "value": ""})
        # </Point#####>

    # Manually write the XML declaration and content to a file
    with open(output_filename, "w", encoding="utf-16") as file:
        file.write('<?xml version="1.0" encoding="UTF-16"?>\n')
        tree = ET.ElementTree(variant)
        tree.write(file, encoding="unicode", method="xml")


def coordinate_generator(start, end, images):
    coordinates = []
    x1, y1, z1 = start
    x2, y2, z2 = end

    # Find the distance between start and end coordinates
    x_dist = math.dist([x1], [x2])
    y_dist = math.dist([y1], [y2])
    z_dist = math.dist([z1], [z2])

    # How large are the steps to traverse each distance in n number of steps
    # beware fence post error :)
    x_step = round(round(x_dist, 15) / (images-1), 15)
    y_step = round(round(y_dist, 15) / (images-1), 15)
    z_step = round(round(z_dist, 15) / (images-1), 15)

    for index in range(0, images):
        if index == 0:
            coordinates.append((x1, y1, z1))
        elif index == images - 1:
            coordinates.append((x2, y2, z2))
        else:
            x1 += x_step
            y1 += y_step
            z1 += z_step

            x1 = round(x1, 15)
            y1 = round(y1, 15)
            z1 = round(z1, 15)

            coordinates.append((x1, y1, z1))

    return coordinates


def main():
    # Example usage
    output_path = 'xml_files/'
    output_script = output_path + '\\' + 'script.xml'

    create_script(output_script)  # This makes scripts


if __name__ == '__main__':
    main()
