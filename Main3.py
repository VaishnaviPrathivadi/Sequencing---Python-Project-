from os import *
from Sequence import *
from FASTA import *
from FASTQ import *


def main():
    # Ask the user for input file and location
    print("Please enter the file location:")
    filename = input()
    sequence_type = None
    file_ext = get_extension_type(filename)

    if file_ext is None:
        print("File format not valid. Supported formats: .fasta and .fastq")
        return

    if file_ext == 'fasta':
        fasta_module = FASTAModule()
        if fasta_module.read(filename):
            sequences = fasta_module.sequences
            sequence_type = determine_sequence_type(sequences)
        else:
            return

    elif file_ext == 'fastq':
        fastq_module = FASTQModule()
        if fastq_module.read(filename):
            sequences = fastq_module.sequences
            sequence_type = 'nucleotide'  # Any FASTQ file will have nucleotide sequences
        else:
            return

    else:
        print("File format not valid. Supported formats: .fasta and .fastq")
        return

    # To check if it is a nucleotide sequence
    if sequence_type == 'nucleotide':
        # Perform nucleotide sequence operations
        print_basic_metrics(sequences, sequence_type)
        provide_nucleotide_interface(fasta_module, fastq_module)
    if file_ext == 'fasta':
        fasta_module = FASTAModule()
        if fasta_module.read(filename):
            sequences = fasta_module.sequences
            sequence_type = determine_sequence_type(sequences)
        else:
            return
    elif file_ext == 'fastq':
        fastq_module = FASTQModule()
        if fastq_module.read(filename):
            sequences = fastq_module.sequences
            sequence_type = 'nucleotide'  # Any FASTQ file will have nucleotide sequences
        else:
            return
    else:
        print("File format not valid. Supported formats: .fasta and .fastq")
        return
    # To check if it is a peptide/amino acid sequence
    elif sequence_type == 'peptide':
        # Perform peptide sequence operations
        print_basic_metrics(sequences, sequence_type)
        provide_peptide_interface(fasta_module, fastq_module)

    else:
        print("Sequence type not recognized.")


def determine_file_type(filename):
    # To check the file extension to determine the file type
    extension = filename.split('.')[-1].lower()
    if extension == 'fasta' or extension == 'fa':
        return 'fasta'
    elif extension == 'fastq' or extension == 'fq':
        return 'fastq'
    else:
        return None


def determine_sequence_type(sequences):
    # To read the first few lines of the sequence and determine the type of sequence
    for sequence in sequences:
        first_line = sequence.sequence.split('\n')[0]
        if set(first_line).issubset({'A', 'C', 'T', 'G', 'N'}):
            return 'nucleotide'
        elif set(first_line).issubset(
                {'A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', '*'}):
            return 'peptide'
        else:
            return None


# To provide basic metrics for the input file
def print_basic_metrics(sequences, sequence_type):
    print("Total Sequences:", len(sequences))
    print("Min Sequence Length:", min(sequence.length for sequence in sequences))
    print("Max Sequence Length:", max(sequence.length for sequence in sequences))
    print("Avg Sequence Length:", sum(sequence.length for sequence in sequences) / len(sequences))

    if sequence_type == 'nucleotide':
        gc_content = calculate_avg_gc_content(sequences)
        print("Avg GC Content:", gc_content)
    elif sequence_type == 'peptide':
        print("Avg GC Content: N/A (Not applicable for peptide sequences)")


# To provide an interface for nucleotide sequences
def provide_nucleotide_interface(fasta_module, fastq_module):
    min_length_threshold = int(input("Enter the minimum sequence length to extract: "))

    if fasta_module:
        fasta_module.print_sequences_with_minimum_length(min_length_threshold)

    if fastq_module:
        min_quality_threshold = int(input("Enter the minimum average quality threshold to extract: "))
        filtered_sequences = fastq_module.filter_sequences_by_min_quality(min_quality_threshold)
        convert_to_fasta = input("Convert FASTQ to FASTA? (y/n): ").lower() == 'y'

        if convert_to_fasta:
            fasta_module = convert_fastq_to_fasta(filtered_sequences)
            fasta_module.print_sequences_with_minimum_length(min_length_threshold)
        else:
            fastq_module.write(filtered_sequences)


# To convert FASTQ to FASTA
def convert_fastq_to_fasta(sequences):
    fasta_module = FASTAModule()
    for sequence in sequences:
        fasta_sequence = SequenceModule(sequence.sequence_id, sequence.description, "", sequence.sequence)
        fasta_module.sequences.append(fasta_sequence)
    return fasta_module


# Additional function to determine the input type
def get_extension_type(filename):
    extension = filename.split('.')[-1].lower()
    print("File extension:", extension)

    if extension == 'fasta':
        print("File type is ", extension)
        f = open(filename, 'r')
        fh = f.read()
        fhd = fh.splitlines()

        # Identify if the sequence is a peptide or nucleotide sequence
        l = ['R', 'N', 'D', 'E', 'Q', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'W', 'Y', 'V']
        count = any(i in fhd[1] for i in l)

        if count == 1:
            print("File has peptide sequences")
        else:
            print("File has nucleotide sequences")

    elif extension == 'fastq':
        print("File type is ", extension)
        print("File has nucleotide sequences")
    else:
        print("Invalid file type")

    return extension


if __name__ == '__main__':
    main()
