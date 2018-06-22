#include <iostream>
#include <stdlib.h>

using namespace std;

typedef struct Node {
    int data;
    struct Node *pNext;
} NODE, *pNODE;


pNODE CreatLinkList(void) {
    int i, length, data;
    pNODE p_new = NULL, pTail = NULL;
    pNODE pHead = (pNODE)malloc(sizeof(NODE));

    if(pHead == NULL) {
        cout << "error" << endl;
        return NULL;
    }
    pHead->data = 0;
    pHead->pNext = NULL;
    pTail = pHead;

    cout << "input length" << endl;
    cin >> length;

    for (i = 1; i < length; i++) {
        p_new = (pNODE)malloc(sizeof(NODE));
        if(p_new == NULL) {
            cout << "error" << endl;
            return NULL;
        }

        cout << "input data for  " << i << endl;
        cin >> data;
        p_new->data = data;
        p_new->pNext = NULL;
        pTail->pNext = p_new;
        pTail = p_new;
    }
    return pHead;
}

void OutputLinkList(pNODE p_node) {
    pNODE o_node = p_node;
    while (o_node != NULL) {
        cout << "node data  " << o_node->data << endl;
        o_node = o_node->pNext;
    }
    cout << "\n" << endl;
}

bool IsEmpty(pNODE p_node) {
    pNODE e_node = p_node->pNext;
    if (e_node ==NULL) {
        return true;
    }
    return false;
}

// Á´±í·´×ª

pNODE ReverseLinkList(pNODE p_node) {
    pNODE pHead, p, q;
    pHead = p_node;
    if (pHead->pNext == NULL) {
        cout << "NONE" << endl;
        return NULL;
    } else if(pHead->pNext != NULL && pHead->pNext->pNext != NULL) {
        p = pHead->pNext;
        q = pHead->pNext->pNext;
    } else {
        return pHead;
    }

    while (p != NULL && q != NULL) {
        pNODE temp;
        temp = q->pNext;
        q->pNext = p;
        p = q;
        q = temp;
    }
    pHead->pNext->pNext = NULL;
    pHead->pNext = p;
    return pHead;
}

int Backward_k (pNODE p_node, int k) {
    pNODE p_fast = p_node;
    pNODE p_slow = p_node;
    int number = 0;
    while (p_fast != NULL) {
        ++number;
        if (number < k) {
            p_fast = p_fast->pNext;
        } else {
            p_fast = p_fast->pNext;
            if (p_fast == NULL)
                return p_slow->data;
            p_slow = p_slow->pNext;
        }
    }
    return 0;
}

int main()
{
    cout << "Hello world!" << endl;
    pNODE head = NULL, re_head = NULL;
    int k_data = 0;
    head = CreatLinkList();
    OutputLinkList(head);
    re_head = ReverseLinkList(head);
    OutputLinkList(re_head);
    k_data = Backward_k(re_head, 4);
    cout << "backwards k is  " << k_data << endl;
    return 0;
}
