#include "transaction.h"

#include <math.h>
#include <string.h>
#include <time.h>

int calculate_total_frequency(const loc_freq_array *locations)
{
    int total_freq = 0;
    for (int i = 0; i < locations->size; i++)
    {
        total_freq += locations->arr[i].freq;
    }
    return total_freq;
}

// Function to calculate the risk score for a given location
float calculate_high_risk_location(const char *location, const loc_freq_array *locations)
{
    int location_freq = 0;
    int total_frequency = calculate_total_frequency(locations);

    // Find the frequency of the current location
    for (int i = 0; i < locations->size; i++)
    {
        if (strcmp(locations->arr[i].loc, location) == 0)
        {
            location_freq = locations->arr[i].freq;
            break;
        }
    }

    // If the location is not found
    if (location_freq == 0)
    {
        return 1.0f; 
    }

    // Calculate the location risk: loc_risk = (1 - (location_freq / total_frequency))
    float loc_risk = 1.0f - ((float)location_freq / total_frequency);
    return loc_risk;
}

// function to check if transaction time is during odd hours (outside 9 AM - 6 PM)
int is_odd_time(const char *time_str)
{
    struct tm tm_time;
    memset(&tm_time, 0, sizeof(tm_time));

    // Assuming time_str is in "dd-mm-yyyy_hh:mm:ss" format, we parse just the time part
    sscanf(time_str, "%*d-%*d-%*d_%d:%d:%d", &tm_time.tm_hour, &tm_time.tm_min, &tm_time.tm_sec);

    // If the transaction is not between 9 AM and 6 PM, it's an odd time
    return (tm_time.tm_hour < 9 || tm_time.tm_hour > 18);
}

// Function to calculate risk based on the transaction amount
float calculate_amount_risk(float amount)
{
    if (amount > 10000)
    {
        return 0.9; // Very high risk for large amounts
    }
    else if (amount > 5000)
    {
        return 0.7; // High risk
    }
    else if (amount > 1000)
    {
        return 0.30; // Moderate risk
    }
    else
    {
        return 0.1; // Low risk
    }
}

// Function to calculate the overall transaction risk score
float calculate_trans_risk(float amount, const char *location, const char *time, loc_freq_array *locations)
{
    float risk_score = 0.0;

    // Amount Risk (weight: 0.65)
    float amount_risk = calculate_amount_risk(amount);
    risk_score += 0.65 * amount_risk;

    // Location Risk (weight: 0.25)
    float loc_risk = calculate_high_risk_location(location, locations);
    risk_score += 0.25 * loc_risk;

    // Time Risk (weight: 0.10)
    if (is_odd_time(time))
    {
        risk_score += 0.10;
    }

    // Normalize the risk score to a maximum of 0.99
    if (risk_score >= 1.0)
    {
        risk_score = 0.99;
    }

    return risk_score;
}

// Create a transaction with given details
transaction create_transaction(int sender, int receiver, float amount, const char *time, const char *location, loc_freq_array *locations)
{
    transaction t;
    t.sender = sender;
    t.receiver = receiver;
    t.amount = amount;
    strncpy(t.time, time, sizeof(t.time) - 1);
    t.time[sizeof(t.time) - 1] = '\0';
    strncpy(t.location, location, sizeof(t.location) - 1);
    t.location[sizeof(t.location) - 1] = '\0';
    t.trans_risk_score = calculate_trans_risk(amount, location, time, locations);

    return t;
}

// Display the transaction details
void display_transaction(transaction *tr)
{
    printf("     Transaction:\n");
    printf("        Sender: %d\n", tr->sender);
    printf("        Receiver: %d\n", tr->receiver);
    printf("        Amount: %.2f\n", tr->amount);
    printf("        Time: %s\n", tr->time);
    printf("        Location: %s\n", tr->location);
    printf("        Risk Score: %.2f\n", tr->trans_risk_score);
}

// Uncomment and implement if needed

// Initialize the TransactionArray
// void initArray(TransactionArray *array) {
//     array->transactions = NULL;
//     array->size = 0;
// }

// Add a new transaction to the array
// void addTransaction(TransactionArray *array, transaction t) {
//     array->size += 1;
//     array->transactions = realloc(array->transactions, array->size * sizeof(transaction));
//     if (array->transactions == NULL) {
//         printf("Memory allocation failed!\n");
//         exit(1);
//     }
//     array->transactions[array->size - 1] = t;
// }

// Print all transactions in the array
// void printTransactions(const TransactionArray *array) {
//     for (size_t i = 0; i < array->size; i++) {
//         printf("Transaction %zu:\n", i + 1);
//         printf("  Sender: %d\n", array->transactions[i].sender);
//         printf("  Receiver: %d\n", array->transactions[i].receiver);
//         printf("  Amount: %.2f\n", array->transactions[i].amount);
//         printf("  Time: %s\n", array->transactions[i].time);
//         printf("  Location: %s\n", array->transactions[i].location);
//         printf("  Risk Score: %.2f\n\n", array->transactions[i].trans_risk_score);
//     }
// }

// Free the memory allocated for the TransactionArray
// void freeArray(TransactionArray *array) {
//     free(array->transactions);
//     array->transactions = NULL;
//     array->size = 0;
// }