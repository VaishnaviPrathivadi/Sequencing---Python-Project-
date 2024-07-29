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
        returns the GC count.
        """
        return self.gc_count

    def calculate_gc_count(self):
        """
        Calculates the GC count.
        """

class FASTQModule:
    def __init__(self):
        self.sequences = []

    def read(self, filename):
        with open(filename, 'r') as file:
            fastq_lines = file.readlines()

        for i in range(0, len(fastq_lines), 4):
            sequence_id = fastq_lines[i].strip()[1:]
            description = fastq_lines[i + 1].strip()
            sequence = fastq_lines[i + 2].strip()
            sequence_quality = fastq_lines[i + 3].strip()

            new_sequence = SequenceModule(sequence_id, description, sequence_quality, sequence)
            self.sequences.append(new_sequence)

    def write(self, seq, filename=None):
        if filename is None:
            # If no filename is provided, print the sequences to the screen in FASTQ format
            for sequence in seq:
                print("@" + sequence.sequence_id)
                print(sequence.description)
                print(sequence.sequence)
                print("+")
                print(sequence.sequence_quality)
        else:
            # Write the sequences to the specified file in FASTQ format
            with open(filename, 'w') as file:
                for sequence in seq:
                    file.write("@" + sequence.sequence_id + "\n")
                    file.write(sequence.description + "\n")
                    file.write(sequence.sequence + "\n")
                    file.write("+" + "\n")
                    file.write(sequence.sequence_quality + "\n")

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


fastq_module = FASTQModule()  # Create an instance of FASTQModule

# Ask the user for the input file
filename = input("Enter the input file name: ")

fastq_module.read(filename)  # Call read method to populate the sequences

sequence_count = fastq_module.count()
average_length = fastq_module.avg_length()
minimum_length = fastq_module.min_length()
maximum_length = fastq_module.max_length()

print("Total Sequences:", sequence_count)
print("Average Length:", average_length)
print("Minimum Length:", minimum_length)
print("Maximum Length:", maximum_length)

# Provide an interface to allow the user to extract sequences with a minimum length
min_length = int(input("Enter the minimum sequence length to extract: "))
fastq_module.print_sequences_with_minimum_length(min_length)

