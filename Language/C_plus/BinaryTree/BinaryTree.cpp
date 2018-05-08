#include <iostream>

using namespace std;

class BinaryNode {
    public:
        char data;
        BinaryNode *left;
        BinaryNode *right;

        BinaryNode(char c) {
            data = c;
        }
};

void CreateTree(BinaryNode *&t) {
    char c;
    cin>>c;
    if(c == '#')
        t = NULL;
    else {
        t = new BinaryNode(c);
        t->left = NULL;
        t->right = NULL;
        CreateTree(t->left);
        CreateTree(t->right);
    }
}

void PreOrder(BinaryNode *&t) {
    if(t) {
        cout<<" "<<t->data;
        PreOrder(t->left);
        PreOrder(t->right);
    }
}

void MidOrder(BinaryNode *t) {
    if(t) {
        MidOrder(t->left);
        cout << " " << t->data;
        MidOrder(t->right);
    }
}

void PostOrder(BinaryNode *t) {
    if (t) {
        PostOrder(t->left);
        PostOrder(t->right);
        cout << " " << t->data;
    }
}

int main() {
    BinaryNode *p1;
    CreateTree(p1);
    cout << "Pre order print" << endl;
    PreOrder(p1);
    cout << "\n" ;
    cout << "Middle order print" << endl;
    InOrder(p1);
    cout << "\n";
    cout << "Post order print" << endl;
    PostOrder(p1);
    return 0;
}

