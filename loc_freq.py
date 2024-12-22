import ctypes
from ctypes import Structure, POINTER, c_char_p, c_int

# Load the DLL
loc_freq_lib = ctypes.CDLL('dlls/loc_freq.dll')

# Define ctypes structures based on C structures

class LocFreq(Structure):
    _fields_ = [
        ("loc", c_char_p),  # Pointer to a string
        ("freq", c_int),    # Frequency as integer
    ]

class LocFreqArray(Structure):
    _fields_ = [
        ("arr", POINTER(LocFreq)),  # Pointer to an array of LocFreq
        ("size", c_int),            # Size of the array
    ]

# Set return and argument types for C functions
loc_freq_lib.create_loc_freq_array.restype = LocFreqArray

loc_freq_lib.append_element.argtypes = [POINTER(LocFreqArray), c_char_p, c_int]
loc_freq_lib.append_element.restype = None

loc_freq_lib.print_loc_freq_array.argtypes = [POINTER(LocFreqArray)]
loc_freq_lib.print_loc_freq_array.restype = None

# Python OOP Wrapper Classes

class LocationFrequency:
    def __init__(self, loc_freq):
        self.location = loc_freq.loc.decode('utf-8')
        self.frequency = loc_freq.freq

    def __repr__(self):
        return f"LocationFrequency(location='{self.location}', frequency={self.frequency})"

class LocationFrequencyArray:
    def __init__(self):
        # Create a new loc_freq_array using the C function
        self.array = loc_freq_lib.create_loc_freq_array()

    def add(self, location, frequency):
        """
        Append a new location-frequency pair to the array.
        If the location exists, it updates the frequency.
        """
        loc_freq_lib.append_element(ctypes.byref(self.array), location.encode('utf-8'), frequency)

    def display(self):
        """
        Print the contents of the array using the C library's print function.
        """
        loc_freq_lib.print_loc_freq_array(ctypes.byref(self.array))

    def get_all(self):
        """
        Retrieve all elements in the dynamic array as Python objects.
        """
        return [
            LocationFrequency(self.array.arr[i])
            for i in range(self.array.size)
        ]

    def __repr__(self):
        return f"LocationFrequencyArray(size={self.array.size})"

if __name__ == "__main__":
    # Initialize a new LocationFrequencyArray
    loc_freq_array = LocationFrequencyArray()

    # Add location-frequency pairs
    loc_freq_array.add("New York", 5)
    loc_freq_array.add("San Francisco", 3)
    loc_freq_array.add("New York", 2)  # Updates the frequency for "New York"

    # Display the array using the C library's print function
    loc_freq_array.display()

    # Retrieve and print all elements as Python objects
    # all_locations = loc_freq_array.get_all()
    # print("All Locations and Frequencies:")
    # for loc in all_locations:
    #     print(loc)
