with open('Data/Gemeindevertretungen_2003.csv', 'r') as infile, open('Data/election_data_2003_formatted.csv', 'w') as outfile:
    for line in infile:
        # Remove trailing commas (any commas after the last value in the line)
        cleaned_line = line[:-3] + '\n'
        print(line, cleaned_line)
        outfile.write(cleaned_line)