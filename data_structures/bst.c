#include "bst.h"
#include <stdlib.h>
#include <stdio.h>

// Function to create a new BST node for an account
bst_node *create_bst_node(account *acc)
{
    bst_node *node = (bst_node *)malloc(sizeof(bst_node));
    node->acc = acc;
    node->flag = (char *)malloc(6 * sizeof(char));
    strcpy(node->flag, "None");
    node->left = NULL;
    node->right = NULL;
    return node;
}

// Function to insert an account into the BST based on risk score
bst_node *insert(bst_node *root, account *acc)
{
    if (root == NULL)
        return create_bst_node(acc);
    if (acc->acc_risk_score < root->acc->acc_risk_score)
        root->left = insert(root->left, acc);
    else if (acc->acc_risk_score >= root->acc->acc_risk_score)
        root->right = insert(root->right, acc);
    return root;
}

// Function to traverse the BST in order and display the accounts
void inorder_traverse(bst_node *root)
{
    if (root != NULL)
    {
        inorder_traverse(root->left);
        printf("Account: %d, Risk Score: %.2f, Flag: %s\n", root->acc->acc_num, root->acc->acc_risk_score, root->flag);
        inorder_traverse(root->right);
    }
}

void targeted_monitoring(bst_node *root)
{
    if (root != NULL)
    {
        // Recursively monitor left subtree
        targeted_monitoring(root->left);

        // If an account's risk score exceeds the threshold, perform further checks or response
        int no_of_trans = root->acc->no_of_transactions;
        float acc_risk_score = root->acc->acc_risk_score;

        if (no_of_trans <= 10)
        {
            strcpy(root->flag, "WHITE");
            printf("Not enough transaction to flag Account: %d, Flagged as %s\n", root->acc->acc_num, root->flag);
        }
        else if (no_of_trans <= 25)
        {
            if (acc_risk_score >= 0.0 && acc_risk_score <= 0.3)
            {
                // Very Low Risk (Green)
                strcpy(root->flag, "GREEN");
                printf("Account: %d, Flagged as %s, Risk Level: Very Low \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.3 && acc_risk_score <= 0.6)
            {
                // Moderate Risk (Yellow)
                strcpy(root->flag, "YELLOW");
                printf("Account: %d, Flagged as %s, Risk Level: Moderate \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.6 && acc_risk_score <= 0.8)
            {
                // High Risk (Orange)
                strcpy(root->flag, "ORANGE");
                printf("Account: %d, Flagged as %s, Risk Level: High \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.8 && acc_risk_score <= 1)
            {
                // Critical Risk (Red)
                strcpy(root->flag, "RED");
                printf("Account: %d, Flagged as %s, Risk Level: Critical \n", root->acc->acc_num, root->flag);
            }
        }
        else
        {
            if (acc_risk_score >= 0.0 && acc_risk_score <= 0.2)
            {
                // Very Low Risk (Green)
                strcpy(root->flag, "GREEN");
                printf("Account: %d, Flagged as %s, Risk Level: Very Low \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.2 && acc_risk_score <= 0.4)
            {
                // Low Risk (Blue)
                strcpy(root->flag, "BLUE");
                printf("Account: %d, Flagged as %s, Risk Level: Low \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.4 && acc_risk_score <= 0.6)
            {
                // Moderate Risk (Yellow)
                strcpy(root->flag, "YELLOW");
                printf("Account: %d, Flagged as %s, Risk Level: Moderate \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.6 && acc_risk_score <= 0.75)
            {
                // High Risk (Orange)
                strcpy(root->flag, "ORANGE");
                printf("Account: %d, Flagged as %s, Risk Level: High \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.75 && acc_risk_score <= 0.9)
            {
                // Critical Risk (Red)
                strcpy(root->flag, "RED");
                printf("Account: %d, Flagged as %s, Risk Level: Critical \n", root->acc->acc_num, root->flag);
            }
            else if (acc_risk_score > 0.9 && acc_risk_score <= 1.0)
            {
                // Extreme Risk (Black)
                strcpy(root->flag, "BLACK");
                printf("Account: %d, Flagged as %s, Risk Level: Extreme \n", root->acc->acc_num, root->flag);
            }
        }

        // Recursively monitor right subtree
        targeted_monitoring(root->right);
    }
}