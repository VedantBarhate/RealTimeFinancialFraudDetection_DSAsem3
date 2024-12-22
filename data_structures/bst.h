#ifndef BST_H
#define BST_H

#include "account.h"

// Define the binary search tree node structure
typedef struct bst_node
{
    account *acc;
    char *flag;
    struct bst_node *left;
    struct bst_node *right;
} bst_node;

// Function prototypes
bst_node *create_bst_node(account *acc);
bst_node *insert(bst_node *root, account *acc);
void inorder_traverse(bst_node *root);
void targeted_monitoring(bst_node *root);

#endif // BST_H
