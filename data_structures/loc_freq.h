#ifndef LOC_FREQ_H
#define LOC_FREQ_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define the loc_freq struct to hold location and frequency
typedef struct
{
    char *loc;
    int freq;
} loc_freq;

// Define the loc_freq_array struct to hold a dynamic array of loc_freq
typedef struct
{
    loc_freq *arr;
    int size;
} loc_freq_array;

// Function prototypes
loc_freq_array create_loc_freq_array();
void append_element(loc_freq_array *d_array, const char *location, int frequency);
void print_loc_freq_array(const loc_freq_array *d_array);

#endif // LOC_FREQ_H
