import shutil
import csv
from collections import defaultdict


def change(temp='20',denomination='D',start_month='1',start_date='1',end_month='1',end_date='31'):
    '''Makes changes in temperature, frequency at which output is generated, and the run period for simulation.
If data not given, assume default value'''
    list_of_den=('Daily','Hourly','Monthly')
    if denomination=='D':
        den=list_of_den[0]
    elif denomination=='H':
        den=list_of_den[1]
    else:
        den=list_of_den[2]
    
    #idf=open("energyplus/test/formatted.idf",'w')
    #shutil.copy2('energyplus/test/format.idf','energyplus/test/formatted.idf')
    with open('energyplus/test/format.idf') as f:
        linestring = f.read()
    a=linestring.format(start_month,start_date,end_month,end_date,temp,temp,temp,temp,temp,temp,temp,temp,temp,temp,temp,temp,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den,den)
    with open("energyplus/test/formatted.idf", "w") as f:
        f.write(a)

def output(denomination='D'):
    '''Generates 4 arrays of strigns in the following order: Date/Time, Cooling Energy, Heating Energy, Electrical Energy.
Ensure that the denomination given here as an input parameter is the same as the denomination given in the above
'change' function.
'''
    columns = defaultdict(list) # each value in each column is appended to a list

    with open('energyplus/test/formattedMeter.csv') as f:
        reader = csv.DictReader(f) # read rows into a dictionary format
        for row in reader: # read a row as {column1: value1, column2: value2,...}
            for (k,v) in row.items(): # go over each column name and value
                columns[k].append(v) # append the value into the appropriate list
    f.close() # based on column name k
    den0=('Daily','Hourly','Monthly')
    #print(columns['Date/Time'])
    if denomination=='D':
        r1=den0[0]
    elif denomination=='H':
        r1=den0[1]
    else:
        r1=den0[2]
    den1='Cooling:Electricity [J]('+r1+')'
    den2='Heating:Electricity [J]('+r1+')'
    den3='Electricity:Facility [J]('+r1+')'
    #print(columns[den1])
    #print(columns[den2])
    c1=columns[den1]
    c2=columns[den2]
    c3=columns[den3]
    #result=[0]*len(c1)
    #for i in range(0,len(c1)):
     # result[i]=str(float(c1[i])+float(c2[i]))
    return columns['Date/Time'],c1,c2,c3