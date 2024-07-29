class SequenceModule:
    def __init__(self, sequence_id, description, sequence_quality, sequence):
        self.sequence_id = sequence_id
        self.description = description
        self.sequence_quality = sequence_quality
        self.sequence = sequence
        self.gc_count = self.calculate_gc_count()
        self.length = len(sequence)

    # Setter method for GC count
    def set_gc_count(self, gc_count):
        """
        Sets the GC count.
        """
        self.gc_count = gc_count

    # Getter method for GC count
    def get_gc_count(self):
        """
        Returns the GC count.
        """
        return self.gc_count
    
    def calculate_gc_count(self):
        """
        Calculates the GC count.
        """
        pass

class FASTAModule:
    def __init__(self):
        self.sequences = []

    def read(self, filename):
        with open(filename, 'r') as file:
            fasta_lines = file.readlines()

        sequence_id = ""
        description = ""
        sequence_quality = []
        sequence = ""

        for line in fasta_lines:
            line = line.strip()
            if line.startswith('>'):
                # If a new sequence entry begins, create a new SequenceModule instance and add it to the list
                if sequence_id != "":
                    new_sequence = SequenceModule(sequence_id, description, sequence_quality, sequence)
                    self.sequences.append(new_sequence)

                sequence_id = line[1:]
                description = ""
                sequence_quality = []
                sequence = ""
            else:
                sequence += line
        # Add the last sequence to the list
        if sequence_id != "":
            new_sequence = SequenceModule(sequence_id, description, sequence_quality, sequence)
            self.sequences.append(new_sequence)

    def write(self, seq, filename=None):
        if filename is None:
            # If no filename is provided, print the sequences to the screen in FASTA format
            for sequence in seq:
                print(">" + sequence.sequence_id)
                print(sequence.sequence)
        else:
            # Write the sequences to the specified file in FASTA format
            with open(filename, 'w') as file:
                for sequence in seq:
                    file.write(">" + sequence.sequence_id + "\n")
                    file.write(sequence.sequence + "\n")

    def count(self):
        # Return the total number of sequences in the input file
        return len(self.sequences)

    def avg_length(self):
        total_length = sum(sequence.length for sequence in self.sequences)
        avg_length = total_length / len(self.sequences) if len(self.sequences) > 0 else 0
        return avg_length

    def min_length(self):
        # Return the minimum sequence length
        return min(sequence.length for sequence in self.sequences)

    def max_length(self):
        # Return the maximum sequence length
        return max(sequence.length for sequence in self.sequences)

    def print_sequences_with_minimum_length(self, min_length):
        # Print sequences with a length greater than or equal to the minimum length
        for sequence in self.sequences:
            if sequence.length >= min_length:
                print(">" + sequence.sequence_id)
                print(sequence.sequence)

fasta_module = FASTAModule()  # Create an instance of FASTAModule

# Ask the user for the input file
filename = input("Enter the input file name: ")

fasta_module.read(filename)  # Call the read method to populate the sequences

sequence_count = fasta_module.count()
average_length = fasta_module.avg_length()
minimum_length = fasta_module.min_length()
maximum_length = fasta_module.max_length()

print("Total Sequences:", sequence_count)
print("Average Length:", average_length)
print("Minimum Length:", minimum_length)
print("Maximum Length:", maximum_length)

# Provide an interface to allow the user to extract sequences with a minimum length
min_length = int(input("Enter the minimum sequence length to extract: "))
fasta_module.print_sequences_with_minimum_length(min_length)









