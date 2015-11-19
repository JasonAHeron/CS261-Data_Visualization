from __future__ import division
import pandas as pd
import os



def all_csvs_in_directory(directory):
    '''
    :param directory containing csv files
    :return: list of csvs in the directory
    :assumption: you have a fairly small number of csvs in this directory,
    this should be rewritten as a generator if you have many csvs
    '''
    return [file for file in os.listdir(directory) if file.endswith('.csv')]


def clean_all_csvs(directory):
    '''
    :param directory containing csv files
    :result drop all rows with invalid data
    '''
    for csv in all_csvs_in_directory(directory):
        clean_csv(directory, csv)


def clean_csv(directory, csv_file):
    df = pd.read_csv('{}/{}'.format(directory, csv_file), header=0)
    try:
        df = df.drop('2012', 1)
        df = df.drop('2013', 1)
        df = df.drop('2014', 1)
        df = df.drop('2015', 1)
        df = df.dropna()
        df.to_csv(csv_file)
    except ValueError as e:
        print e, csv_file


def intersect_all_sets(directory):
    intersection = set()
    for csv_file in all_csvs_in_directory(directory):
        df = pd.read_csv('{}/{}'.format(directory, csv_file), header=0)
        indicator_codes = {indicator_code for indicator_code in df['Indicator Code']}
        if not intersection:
            intersection.update(indicator_codes)
        else:
            intersection.intersection_update(indicator_codes)
    return intersection


def drop_non_intersecting(directory):
    intersection = intersect_all_sets(directory)
    for csv_file in all_csvs_in_directory(directory):
        df = pd.read_csv('{}/{}'.format(directory, csv_file), header=0)
        df = df[df['Indicator Code'].isin(intersection)]
        df.to_csv(csv_file)

drop_non_intersecting('correlations_unique')

# for csv_file in all_csvs_in_directory('clean_data'):
#     df = pd.read_csv('{}/{}'.format('clean_data', csv_file), header=0)
#     for column in df.ix[:,6:len(df.ix[1,]) -1]:  # for every year except the last one
#         current_internet_value = df.ix[df['Indicator Code'] == 'IT.NET.USER.P2', column]  # take the current years internet value
#         next_internet_value = df.ix[df['Indicator Code'] == 'IT.NET.USER.P2', str(int(column)+1)]  # take the next years value of internet
#         multiplier = (next_internet_value - current_internet_value)/current_internet_value.values[0]
#         print csv_file, multiplier, column


# for csv_file in all_csvs_in_directory('valid_data'):
#     df = pd.read_csv('{}/{}'.format('valid_data', csv_file), header=0)
#     df = df.set_index(df['AAAIndicator Name'])
#     for column in df.ix[:,6:len(df.ix[1,]) -1]:  # for every year except the last one
#         current_internet_value = df.ix[df['Indicator Code'] == 'IT.NET.USER.P2', column]  # take the current years internet value
#         next_internet_value = df.ix[df['Indicator Code'] == 'IT.NET.USER.P2', str(int(column)+1)]  # take the next years value of internet
#         try:
#             multiplier = ((next_internet_value - current_internet_value)/current_internet_value).values[0]
#         except IndexError as e:
#             print e, csv_file, column
#         i = 0
#         for value, next_value in  zip(df[column], df[str(int(column)+1)]):  # look at one factor for this and next year
#             high = value + (value * multiplier)
#             low = value - (value * multiplier)
#             if low <= next_value <= high:
#                 pass
#             else:
#                 #print 'For {} to {} internet changed by {}, c{}, n{}'.format(column, int(column)+1,multiplier,value,next_value)
#                 df = df[df[column] != value]
#                 #print "DROPPED"
#             i+=1
#     df.to_csv(csv_file)



#internet_values = df.ix[df['Indicator Code'] == 'IT.NET.USER.P2', 6:].values

