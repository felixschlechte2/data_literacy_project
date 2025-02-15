import csv
from cities_over_20k import get_cities
from collections import Counter
#cities = get_cities()
#print(cities)
cities = ['Frankfurt am Main', 'Wiesbaden', 'Kassel', 'Darmstadt', 'Offenbach am Main', 'Hanau', 'Gießen', 'Marburg', 'Fulda', 'Rüsselsheim am Main', 'Bad Homburg vor der Höhe', 'Wetzlar', 'Oberursel (Taunus)',
           'Rodgau', 'Dreieich', 'Bensheim', 'Hofheim am Taunus', 'Langen (Hessen)', 'Maintal', 'Neu-Isenburg', 'Limburg an der Lahn', 'Bad Vilbel', 'Mörfelden-Walldorf', 'Dietzenbach', 'Viernheim', 'Bad Nauheim',
             'Lampertheim', 'Friedberg (Hessen)', 'Taunusstein', 'Bad Hersfeld', 'Mühlheim am Main', 'Kelkheim (Taunus)', 'Rödermark', 'Hattersheim am Main', 'Baunatal', 'Griesheim', 'Heppenheim (Bergstraße)',
               'Butzbach', 'Groß-Gerau', 'Weiterstadt', 'Friedrichsdorf', 'Idstein', 'Obertshausen', 'Pfungstadt', 'Riedstadt', 'Korbach', 'Gelnhausen', 'Dillenburg', 'Karben', 'Bad Soden am Taunus', 'Büdingen',
                 'Eschborn', 'Seligenstadt', 'Flörsheim am Main', 'Stadtallendorf', 'Herborn', 'Groß-Umstadt', 'Bruchköbel', 'Nidderau']

def check_cities(city):
    if city in cities:
        return city
    j = 0
    for i in cities:
        if i in city:
            if i == "Fulda" and j != 1:
                j == 1
                continue
            return i
    
    n = len(city)
    
    for i in range(0,n-1):
        if city[i] == '�':
            if city[0:i]+ "ä"+ city[i+1:n] in cities:
                return city[0:i]+ "ä"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ä"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
            elif city[0:i]+ "ö"+ city[i+1:n] in cities:
                return city[0:i]+ "ö"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ö"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
            elif city[0:i]+ "ü"+ city[i+1:n] in cities:
                return city[0:i]+ "ü"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ü"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
            elif city[0:i]+ "ß"+ city[i+1:n] in cities:
                return city[0:i]+ "ß"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ß"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
    return None



# Input and output file paths
input_files = ["CO.csv", "NO2.csv","O3.csv","PM10.csv","SO2.csv"]


appearing_cities = []
counter = 0
for input_csv_file in input_files:
    # Open the input CSV file for reading
    with open(input_csv_file, 'r',encoding='utf-8', errors='replace') as infile:
        reader = csv.reader(infile, delimiter=',')

        # Process each row from the input file
        for line in reader:
            counter += 1
            for thing in line:
                if any(substring in thing for substring in cities):
                    for j in cities:
                        if j in thing:
                            appearing_cities.append(j)  
                            continue
                if thing in cities:
                    appearing_cities.append(thing)
                    continue
                        
print(len(appearing_cities))
necessary_cities = list(set(appearing_cities))
print(necessary_cities)
print(len(appearing_cities)/counter)
print(Counter(appearing_cities))
        

