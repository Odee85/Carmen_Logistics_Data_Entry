import PyPDF2
import csv
from datetime import datetime

""" Change location of file when the input and output 
name or location of the file changes """

file_name = "01_TestFiles/TransactionReport-230710110034.pdf"
output_filename = "01_TestFiles/TransactionReport-230710110034.csv"


def get_vendor_name(vendor_name_components):
    """
    Arg: vendor_name_components
    Arg_type: list
    Description: This funciton gets all the components that makes a vendor name
                    in a list format and return the location name in a string format

    """

    # print(vendor_name_components)
    # Testing

    num_index = 0
    for item in vendor_name_components:
        item_ori = item
        try:
            # Check the first character of the number and if it starts with '#', remove it.
            if item[0] == "#":
                item = item[1:]

            num_index = int(item)
            num_index = vendor_name_components.index(item_ori)

            vendor_name_components = vendor_name_components[: num_index + 1]

            continue
        except ValueError:
            pass

    vendor_name = ' '.join(vendor_name_components)

    # print(vendor_name)

    return vendor_name


def get_driver_name(formated_data):
    """
    Arg: formated_data
    Arg_type: list
    Description: Gets driver name based on driver number (e.g driver1, driver2 etc.)

    """

    # print(f"Formated Data {formated_data}")

    driver_id = get_vehicle_id(formated_data)

    if driver_id == 370:
        driver_name = "Jerret"
    elif driver_id == 371:
        driver_name = "Alex"
    elif driver_id == 372:
        driver_name = "Kemario"
    else:
        driver_name = None

    return driver_name


def get_vehicle_id(formated_data):
    """
    Arg: driver_name
    Arg_type: str
    Description: Gets driver id based on driver_name

    """
    #print(f"Formated Data: {type(formated_data[0])}")

    if formated_data[0].strip() == "00000":
        vehicle_id = 372
    elif formated_data[0].strip() == "00042":
        vehicle_id = 371
    elif formated_data[0].strip() == '00059':
        vehicle_id = 370
    else:
        vehicle_id = 000

    return vehicle_id


def get_total_cost(formated_data):
    """
    Arg: formated_data
    Arg_type: list
    Description: gets the total cost by index and format it appropriately
    """

    total_cost = 0

    try:
        total_cost = formated_data[-1]
    except IndexError:
        total_cost = formated_data[-1]
    except:
        total_cost = "None"

    unnecessay_extension = 'YUSD/Gallons'

    if len(total_cost) > len(unnecessay_extension):
        total_cost = total_cost[:-len(unnecessay_extension)]

        if total_cost[:2].upper() == "ND":
            total_cost = total_cost[2:]
        else:
            pass

    return total_cost


def get_odometer_reading(formated_data):
    """
    Arg: formated_data
    Arg_type: list
    Description: Gets the odometer reading if available otherwise sets it to 0

    """

    odometer_reading = formated_data[5]

    try:
        odometer_reading = int(odometer_reading)
    except ValueError:

        formated_data.insert(5, 0)

        odometer_reading = formated_data[5]

    return odometer_reading


def get_fuel_quantity(formated_data):
    """
    Arg: formated_data
    Arg_typ: list
    Description: Gets the fuel quantity using the indicator 'ULSD'

    """

    ulsd_indx = formated_data.index('ULSD')  # Indicator to locate fuel quantity

    index_of_volume = ulsd_indx + 3

    volume = formated_data[index_of_volume]

    point_index = volume.index(".")

    volume = volume[:point_index + 3]  # Getting rid of unwanted data (beyond 2 decimal places)

    return volume


def get_juridiction_info(formated_data):
    """Arg: formated_data
    Arg_type: list
    Description: returns name of jurisdiction of trucks and position within a list"""

    for data in formated_data:
        if len(data) == 2 and data.isupper():
            jurisdiction = data
            jurisdiction_index = formated_data.index(data)
            continue

    return jurisdiction, jurisdiction_index


with open(file_name, 'rb') as carmenlogisticsdffile:
    print("\nReading input file...")
    pdf_file = PyPDF2.PdfReader(carmenlogisticsdffile)

    number_of_pages = len(pdf_file.pages)

    all_content = []

    for page_num in range(0, number_of_pages):
        page = pdf_file.pages[page_num]
        text_content = page.extract_text()

        text_content = text_content.split('\n')

        all_content.append(text_content)

with open(output_filename, 'w', newline='') as carmen_raw_data_output_file_obj:
    print("Creating output file...")
    csv_file_writer = csv.writer(carmen_raw_data_output_file_obj)

    print("Processing output data...\n")
    for text_content in all_content:

        # print(text_content)
        # print()
        formated_data = []
        csv_file_writer.writerow(formated_data)

        for text in text_content:

            main_data = []
            other_data = []

            row_data = text.split(" ")

            card_id = ""

            try:
                card_id = int(row_data[0])
            except ValueError:
                pass

            if len(row_data[0]) == 5 and card_id != "":
                formated_data = row_data

            try:
                if row_data[0] == 'ULSD' and len(formated_data) > 0:
                    # print(f"Row: {row_data[0]}")
                    formated_data += row_data

                    #print(formated_data)

                    if 'Driver' in formated_data:
                        formated_data[3:5] = []
                        #print(formated_data)

                    if len(formated_data) != 0:
                        required_data = []

                        date_raw = datetime.strptime(formated_data[1], '%Y-%m-%d')

                        date = date_raw.strftime("%m/%d/%Y")
                        time = "1:30pm"  # Default time stamp

                        jurisdiction, jurisdiction_index = get_juridiction_info(formated_data)

                        driver_name = get_driver_name(formated_data)

                        # print(f"Odometer Reading {odometer_reading}")

                        vehicle_id = get_vehicle_id(formated_data)

                        fuel_type = "Diesel"  # Default fuely type

                        fuel_measurement_unit = 'Gallons'  # Default

                        volume = get_fuel_quantity(formated_data)

                        currency = "USD"  # Default

                        total_cost = get_total_cost(formated_data)

                        # print(formated_data)

                        vendor_name_components = formated_data[4: jurisdiction_index + 1]

                        vendor_name = get_vendor_name(vendor_name_components)

                        odometer_reading = get_odometer_reading(formated_data)

                        location = vendor_name

                        required_data.append(date)
                        required_data.append(time)
                        required_data.append(jurisdiction)
                        required_data.append(driver_name)
                        required_data.append(vehicle_id)
                        required_data.append(fuel_type)
                        required_data.append(fuel_measurement_unit)
                        required_data.append(volume)
                        required_data.append(currency)
                        required_data.append(total_cost)
                        required_data.append(vendor_name)
                        required_data.append(location)

                        # print(f"Required Data {required_data}")

                        # print(len(required_data))
                        print("Writing processed data into output file...")
                        csv_file_writer.writerow(required_data)

                        formated_data = []
            except IndexError:
                pass

print(f"\nFiled saved into '{output_filename}'")
print("\nDone")
