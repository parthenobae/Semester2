
import csv

def sequence_checker(database_file, sequence_file):

    # TODO: Read database file into a variable
    with open(database_file) as database:
        reader = csv.DictReader(database)
        strs = reader.fieldnames[1:]
    # TODO: Read DNA sequence file into a variable
    with open(sequence_file, 'r') as sequence:
        for line in sequence:
            seq = line
            break
    # TODO: Find longest match of each STR in DNA sequence
    matches = []
    for i in range(len(strs)):
        nm = longest_match(seq, strs[i])
        matches.append(nm)
    # TODO: Check database for matching profiles
    with open(database_file) as database:
        reader = csv.DictReader(database)
        for row in reader:
            profile = []
            for str in strs:
                profile.append(int(row[str]))
            if profile == matches:
                return row['name']
                
    return None


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            
            if end > sequence_length:
                break
                
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run