#include "loc_freq.h"

// Function to create loc_freq dynamic array
loc_freq_array create_loc_freq_array()
{
    loc_freq_array d_array;
    d_array.arr = NULL;
    d_array.size = 0;
    return d_array;
}

// Function to append an element to the dynamic array, updating frequency if existing
void append_element(loc_freq_array *d_array, const char *location, int frequency)
{
    int i;

    // Check if the location already exists
    for (i = 0; i < d_array->size; i++)
    {
        if (strcmp(d_array->arr[i].loc, location) == 0)
        {
            d_array->arr[i].freq += frequency;
            return;
        }
    }

    // If the location doesn't exist, append it
    d_array->size++;
    d_array->arr = (loc_freq *)realloc(d_array->arr, d_array->size * sizeof(loc_freq));
    if (d_array->arr == NULL)
    {
        exit(1); // Memory allocation failed
    }
    d_array->arr[d_array->size - 1].loc = (char *)malloc(strlen(location) + 1);
    if (d_array->arr[d_array->size - 1].loc == NULL)
    {
        exit(1); // Memory allocation failed
    }
    strcpy(d_array->arr[d_array->size - 1].loc, location);
    d_array->arr[d_array->size - 1].freq = frequency;
}

// Function to print elements from dynamic array
void print_loc_freq_array(const loc_freq_array *d_array)
{
    for (int i = 0; i < d_array->size; i++)
    {
        printf("Location: %s, Frequency: %d\n", d_array->arr[i].loc, d_array->arr[i].freq);
    }
}
