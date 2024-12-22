#ifndef ACCOUNT_H
#define ACCOUNT_H

#include "transaction.h"
#include "loc_freq.h"

// Define the account struct to hold account details, transaction history, and risk score
typedef struct Account
{
    int acc_num;
    int no_of_transactions;
    double avg_trans_amnt;
    double avg_trans_risk_score;
    loc_freq_array locations;
    double acc_risk_score;
} account;

// Function declarations
account *create_account(int acc_num);
float calculate_location_risk(loc_freq_array *locations, const char *location);
void update_account_risk(account *acc, const transaction *t);
void display_account(const account *acc);

#endif // ACCOUNT_H
