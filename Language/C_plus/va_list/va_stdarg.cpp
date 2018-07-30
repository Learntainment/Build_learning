/* va_arg example */
#include <stdio.h>      /* printf */
#include <stdarg.h>     /* va_list, va_start, va_arg, va_end */

int FindMax (int n, ...) {
    int i,val,largest;
    va_list vl;
    va_start(vl,n);
    largest=va_arg(vl,int);
    for (i=1;i<n;i++) {
        val=va_arg(vl,int);
        largest=(largest>val)?largest:val;
    }
    va_end(vl);
    return largest;
}

void PrintFloats (int n, ...) {
    int i;
    double val;
    printf ("Printing floats:");
    va_list vl;
    va_start(vl,n);
    for (i=0;i<n;i++)
    {
        val=va_arg(vl,double);
        printf (" [%.2f]",val);
    }
    va_end(vl);
    printf ("\n");
}

int main () {
    int m;
    m= FindMax (7,702,422,631,834,892,104,772);
    printf ("The largest value is: %d\n",m);

    PrintFloats (3,3.14159,2.71828,1.41421);
    return 0;
}
