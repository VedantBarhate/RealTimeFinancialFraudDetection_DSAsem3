#include "account.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// Function to create a new account
account *create_account(int acc_num)
{
    account *acc = (account *)malloc(sizeof(account));
    acc->acc_num = acc_num;
    acc->no_of_transactions = 0;
    acc->avg_trans_amnt = 0.0;
    acc->avg_trans_risk_score = 0.0; // Initialize average transaction risk score
    acc->locations = create_loc_freq_array();
    acc->acc_risk_score = 0.0;
    return acc;
}

// Function to calculate location risk based on location frequency
float calculate_location_risk(loc_freq_array *locations, const char *location)
{
    for (int i = 0; i < locations->size; i++)
    {
        if (strcmp(locations->arr[i].loc, location) == 0)
        {
            return 1.0 / locations->arr[i].freq; // Inverse relation to frequency
        }
    }
    return 1.0; // Higher risk for unseen locations
}

// Function to update account risk score based on a new transaction
void update_account_risk(account *acc, const transaction *t)
{
    acc->no_of_transactions++;

    // Update the average transaction amount
    acc->avg_trans_amnt = ((acc->avg_trans_amnt * (acc->no_of_transactions - 1)) + t->amount) / acc->no_of_transactions;

    // Update location frequencies
    append_element(&acc->locations, t->location, 1);

    // Calculate and update location risk
    float location_risk = calculate_location_risk(&acc->locations, t->location);

    // Update the average transaction risk score
    acc->avg_trans_risk_score = ((acc->avg_trans_risk_score * (acc->no_of_transactions - 1)) + t->trans_risk_score) / acc->no_of_transactions;

    // Base alpha value - smoothing constant
    float alpha = 0;
    if (acc->no_of_transactions <= 10)
    {
        alpha = 0.7;
    }
    else if (acc->no_of_transactions <= 25)
    {
        alpha = 0.5;
    }
    else
    {
        alpha = 0.3;
    }

    // Modify alpha based on the current transaction risk score
    if (t->trans_risk_score >= 0.7)
    {
        alpha += 0.05; // Increase alpha for high-risk transactions
    }
    else if (t->trans_risk_score <= 0.35)
    {
        alpha -= 0.05; // Decrease alpha for low-risk transactions
    }

    // normalize alpha between 0 and 1
    if (alpha > 1.0)
        alpha = 0.99;
    if (alpha < 0.0)
        alpha = 0.01;

    // Calculate new risk score based on current transaction
    float new_risk_score = (0.5 * acc->avg_trans_risk_score) +
                           (0.25 * t->amount / acc->avg_trans_amnt) + //
                           (0.25 * location_risk);

    // Apply exponential smoothing with alpha
    acc->acc_risk_score = (alpha * new_risk_score) + ((1 - alpha) * acc->acc_risk_score);
}

// Function to display account details
void display_account(const account *acc)
{
    printf("  Account ID: %d\n", acc->acc_num);
    printf("  Number of Transactions: %d\n", acc->no_of_transactions);
    printf("  Average Transaction Amount: %.2f\n", acc->avg_trans_amnt);
    printf("  Average Transaction Risk Score: %.2f\n", acc->avg_trans_risk_score);
    printf("  Account Risk Score: %.2f\n", acc->acc_risk_score);
    printf("  Usual Locations:\n");
    for (int i = 0; i < acc->locations.size; i++)
    {
        printf("    Location: %s, Frequency: %d\n", acc->locations.arr[i].loc, acc->locations.arr[i].freq);
    }
}
