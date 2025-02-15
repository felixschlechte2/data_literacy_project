import xml.etree.ElementTree as ET
import csv

cities = ["Hannover","Braunschweig","Oldenburg (Oldb)","Osnabrück","Wolfsburg","Göttingen","Salzgitter","Hildesheim","Delmenhorst","Lüneburg","Wilhelmshaven","Celle","Garbsen","Hameln","Lingen (Ems)","Langenhagen",
    "Nordhorn","Wolfenbüttel","Peine","Emden","Goslar","Cuxhaven","Stade","Melle","Neustadt am Rübenberge","Lehrte","Gifhorn","Aurich","Seevetal","Laatzen","Wunstorf","Buchholz in der Nordheide","Buxtehude",
    "Papenburg","Cloppenburg","Winsen (Luhe)","Meppen","Leer (Ostfriesland)","Barsinghausen","Seelze","Stuhr","Vechta","Uelzen","Achim","Nienburg/ Weser","Ganderkesee","Georgsmarienhütte","Weyhe","Bramsche",
    "Geestland","Burgdorf","Walsrode","Einbeck","Osterholz-Scharmbeck","Wedermark","Bad Zwischenahn","Northeim","Springe","Verden (Aller)","Lohne (Oldenburg)","Nordenham","Helmstedt","Rinteln","Norden","Syke",
    "Haren (Ems)","Ronnenberg","Isernhagen","Varel","Sehnde","Moormerland","Westerstede","Hann. Münden","Rastede","Friesoythe","Edewecht","Stadthagen","Wallenhorst","Rotenburg (Wümme)","Neu Wulmstorf","Ilsede",
    "Soltau","Westoverledingen","Bad Harzburg","Wildeshausen","Osterode am Harz","Schortens","Wittmund","Schwanewede","Burgwedel","Uetze","Duderstadt","Lilienthal","Holzminden"]

# Path to the XML file
xml_file = 'Gemeinde_2001.xml'

# Define the namespaces
namespaces = {
    'o': "urn:schemas-microsoft-com:office:office",
    'x': "urn:schemas-microsoft-com:office:excel",
    'ss': "urn:schemas-microsoft-com:office:spreadsheet",
    'html': "http://www.w3.org/TR/REC-html40"
}

# Parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

i = -1
j = 0
cell_data = []
# Open a CSV file to write data
with open('Niedersachsen2001_Gemeinde.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Find the table elements within the spreadsheet
    tables = root.findall('.//ss:Table', namespaces)
    for table in tables:
        # Iterate through rows in the table
        for row in table.findall('ss:Row', namespaces):
            row_data = []
            
            # Extract specific cells based on their positions in the list
            # List of positions (0-based index) to keep, according to your example
            #positions_to_extract1 = [1]
            positions_to_extract2 = [4,5,6,7,8,9,22]  # Adjust these indices as needed


            # Iterate through cells in the row and extract the data
            if i == 2:
                cell_data = []
            positions_to_extract = positions_to_extract2
            for idx, cell in enumerate(row.findall('ss:Cell', namespaces)):
                data = cell.find('ss:Data', namespaces)
                if data is not None and data.text:  # Check if there's actual data
                    cell_value = data.text.strip()  # Strip leading/trailing spaces
                    
                    
                    if "Gifhorn" not in cell_value and j == 0:
                        i = -1
                        #print(cell_data)
                        continue
                    else:
                        j = 1


                    if len(cell_value) >6:
                        #print(cell_value)
                        #print(cell_data)
                        i = 0
                        #print(cell_value)
                        notinside = True
                        for city in cities:
                            if city in cell_value:
                                cell_data.append(city)
                                notinside = False
                                flag = True
                    if notinside:
                        continue
                        

                    #if cell_value == "Anzahl":
                    #    continue
                        #positions_to_extract = positions_to_extract1
                        #i = 1
                    if cell_value == "%":
                        
                        #positions_to_extract = positions_to_extract2
                        flag = True
                        #print(flag)
                        i = 2
                   #print(flag)
                    # Only add the values from the specific positions
                    
                    if idx in positions_to_extract2 and i ==2:
                        #print(idx)
                        #print(cell_value)
                        #print(cell_data)
                        if cell_value == "-":
                            cell_data.append(0)
                        else:
                            cell_data.append(cell_value)
                    
                    flag = False
            if i <2:
                continue
            
            # Write the selected data to the CSV file (one row)
            if cell_data:
                writer.writerow(cell_data)

print("Data has been written to 'output.csv'.")
