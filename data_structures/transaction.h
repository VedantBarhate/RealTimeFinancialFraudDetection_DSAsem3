#ifndef TRANSACTION_H
#define TRANSACTION_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "loc_freq.h"

// KARTA-DHARTA of Project
typedef struct Transaction
{
    int sender;
    int receiver;
    float amount;
    char time[19]; // Format: YYYY-MM-DD_HH:MM:SS
    char location[30];
    float trans_risk_score;
} transaction;

// Function prototypes
float calculate_trans_risk(float amount, const char *location, const char *time, loc_freq_array *locations);
transaction create_transaction(int sender, int receiver, float amount, const char *time, const char *location, loc_freq_array *locations);
void display_transaction(transaction *tr);



// typedef struct TransactionArray 
// {
//     transaction *transactions;
//     size_t size;
// } TransactionArray;

// void initArray(TransactionArray *array);
// void addTransaction(TransactionArray *array, transaction t);
// void printTransactions(const TransactionArray *array);
// void freeArray(TransactionArray *array);

#endif // TRANSACTION_H
