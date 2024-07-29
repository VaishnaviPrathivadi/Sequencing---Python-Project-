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
        gc_count = 0
        for base in self.sequence:
            if base == 'G' or base == 'C':
                gc_count += 1
        return gc_count
    

# Create an instance of SequenceModule
sequence = SequenceModule("sequence_id", "description", "sequence_quality", "sequence")

# Access the instance attributes
print(sequence.sequence_id)
print(sequence.description)
print(sequence.sequence_quality)
print(sequence.sequence)
print(sequence.get_gc_count())
print(sequence.length)

