# Note: "file_name" refers to uploaded .csv file

import csv
import re

def bulk_upload(file_name):
    
    # First to import .csv as python list
    in_file = re.sub('["]','',file_name)
    in_data = open(in_file,encoding='cp1252')
    csv_data = csv.reader(in_data, delimiter="\t")
    data_lines = list(csv_data)
    
#########################################
    # Next to edit data in lines
    # MAIN PORTION OF SCRIPT!!!
    position = 12
    for y,line in enumerate(data_lines[10::]):
        for i in range(int(line[10])*2)[::2]:
            data_lines[y+10][position] = data_lines[y+10][9]
            position +=2
#########################################
    
    
        # Now to save edited data to new file
    name_end = in_file.index('.')
    file_name = in_file#[:name_end]+'_EDIT.tsv'
          
    output_file = open(file_name,mode='w',newline='',errors='replace')

    # Write edited data lines to new file
    
    csv_writer = csv.writer(output_file, delimiter='\t')
    for line in data_lines:
        print(line)
        csv_writer.writerow(line)
    output_file.close()
    return(file_name)

    