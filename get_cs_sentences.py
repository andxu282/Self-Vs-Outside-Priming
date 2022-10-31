import sys
from utils import write_to_csv, get_utterances, write_from_path


def get_cs_sentences(file):
    '''
    Returns a list of sentences (the list of words of each utterance) that have 
    a code-switch within them in addition to the indices of the code-switches 
    appended to each sentence. The index of the code-switch is the last word of
    the original language (i.e. if the sentece begins in English, the index is 
    the index of the last English word). Accounts for multiple code-switches 
    within a sentence.
    '''
    utterances = get_utterances(file)
    cs_sentences = []
    sentences_cs_points = []
    for utterance in utterances:
        lang = "" 
        cs_points = []
        for i, tup in enumerate(utterance):
            if i == 0:
                lang = tup[2]
            else:
                if lang == "eng&spa" and tup[2] != "eng&spa" and tup[2] != "999":
                    lang = tup[2]
                if lang != tup[2] and tup[2] != "eng&spa" and lang != "eng&spa" and tup[2] != "999":
                    cs_points.append(i - 1)
                    lang = tup[2]
        if len(cs_points) > 0:
            sentence = [word_tup[0] for word_tup in utterance]
            sentence_cs_points = [str(cs_point) for cs_point in cs_points]
            cs_sentences.append(sentence)
            sentences_cs_points.append(sentence_cs_points)
    return cs_sentences, sentences_cs_points


def write_cs_sentences_from_file(utterances_file, output_files):
    '''
    Writes all code switched sentences and code switch positions for each
    sentence to two separate csv files given a specific file with code-switch 
    data. 
    '''
    (sents_file, cs_points_file) = output_files
    cs_sents, sentences_cs_points = get_cs_sentences(utterances_file)
    write_to_csv(sents_file, cs_sents)
    write_to_csv(cs_points_file, sentences_cs_points)


def main():
    '''
    Reads in a path to a directory containing code-switch data files and 
    generates two csv file names to put all code-switched sentences into and 
    code-switch positions.
    '''
    path = sys.argv[1]
    sents_file = path + "_cs_sents.csv"
    cs_points_file = path + "_cs_points.csv"
    write_from_path(path, write_cs_sentences_from_file, 
        sents_file, cs_points_file)

if __name__ == "__main__":
   main()
    