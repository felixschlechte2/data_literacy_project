import csv

cities = ['Frankfurt am Main', 'Wiesbaden', 'Kassel', 'Darmstadt', 'Offenbach am Main', 'Hanau', 'Gießen', 'Marburg', 'Fulda', 'Rüsselsheim am Main', 'Bad Homburg vor der Höhe', 'Wetzlar', 'Oberursel (Taunus)',
           'Rodgau', 'Dreieich', 'Bensheim', 'Hofheim am Taunus', 'Langen (Hessen)', 'Maintal', 'Neu-Isenburg', 'Limburg an der Lahn', 'Bad Vilbel', 'Mörfelden-Walldorf', 'Dietzenbach', 'Viernheim', 'Bad Nauheim',
             'Lampertheim', 'Friedberg (Hessen)', 'Taunusstein', 'Bad Hersfeld', 'Mühlheim am Main', 'Kelkheim (Taunus)', 'Rödermark', 'Hattersheim am Main', 'Baunatal', 'Griesheim', 'Heppenheim (Bergstraße)',
               'Butzbach', 'Groß-Gerau', 'Weiterstadt', 'Friedrichsdorf', 'Idstein', 'Obertshausen', 'Pfungstadt', 'Riedstadt', 'Korbach', 'Gelnhausen', 'Dillenburg', 'Karben', 'Bad Soden am Taunus', 'Büdingen',
                 'Eschborn', 'Seligenstadt', 'Flörsheim am Main', 'Stadtallendorf', 'Herborn', 'Groß-Umstadt', 'Bruchköbel', 'Nidderau']




# Input and output file paths
input_files = ["HE2021.csv","Hessen2001-2016rawtry.csv"]
output_file = "Hessen.csv"


appearing_cities = []

header = [
        "City",
        "State",
        "Date",
        "Linke",
        "Gruene",
        "SPD",
        "FDP",
        "CDU",
        "AfD",
        "Others",
    ]
    # Open the output file for writing
with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header row

        with open(input_files[0], mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile)

            for row in reader:
                writer.writerow(row)

        with open(input_files[1], mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile, delimiter=';')
            for row in reader:
                 new_row = [row[0],row[1],int(row[2]),int(row[8])/int(row[10])*100,int(row[5])/int(row[10])*100,
                            int(row[4])/int(row[10])*100,int(row[6])/int(row[10])*100,int(row[3])/int(row[10])*100,int(row[9])/int(row[10])*100]
                 new_row.append(100- sum(new_row[3:8]))
                 print(new_row)
                 writer.writerow(new_row)
        

