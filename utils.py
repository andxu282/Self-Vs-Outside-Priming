import csv
from os import listdir
from os.path import isfile, join

def get_utterances(file):
    '''
    Gets the utterances from a specified .tsv file and returns it as a list of a 
    list of tuples.
    '''
    init = 1
    utterances = []
    utterances.append([])

    with open(file, "r") as f:
        # breaks up file into utterances using the utterance_id found in the tsv
        for line in f.readlines()[1:]:
            stripped = line.replace('\n', '').split('\t')
            try:
                if int(stripped[1]) != init: 
                    utterances.append([])
                    init = int(stripped[1])
                utterances[init - 1].append((stripped[3], stripped[8], stripped[9]))
            except IndexError:
                # this is only here to skip the last row which denotes the number of rows
                pass
    return utterances

def write_to_csv(file, sentences):
    '''
    Writes a list of sentences to a csv file given a filename.
    '''
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sentences)

def write_from_path(path, file_fun, *output_files):
    '''
    Processes data from a file using file_fun and writes the output to some 
    output files.
    '''
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        file_fun(join(path, file), output_files)