#include <stdio.h>

int main(void)
{
    // // CS50 Week 4 Pointers Example
    // int n = 50;
    // int *p = &n;
    // printf("%p\n", p);
    // printf("%i\n", *p);
    
    // From 
    int *pa, x;
    int a[20] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19};
    double d;
    
    // pa = &a[5]; // Address of 6th element in a.
    // x = *pa; // int value stored in pa.
    // printf("%p\n", pa);
    // printf("%i\n", x);
    // printf("%i\n", *&x);
    
    typedef struct twentypiece
    {
        int (*var)[5];
    }
    twentypiece;
    
    twentypiece b;
    b.var = &a[1];
    int *c = &(*b.var)[4];
    printf("*c = %i\n", *c);
    printf("(*b.var) = %i\n", (*b.var)[4]);
    printf("a[4] = %i\n", a[4]);
    printf("\n");
    
    *c = 302;
    printf("*c = %i\n", *c);
    printf("(*b.var) = %i\n", (*b.var)[4]);
    printf("a[4] = %i\n", a[4]);
    printf("\n");
    
    int e = *c;
    int *f = c;
    
    printf("e = %i\n", e);
    printf("*f = %i\n", *f);
    printf("\n");
    
    *c = 100;
    *f = 20;
    printf("*C = %i\n", *c);
    printf("(*b.var) = %i\n", (*b.var)[4]);
    printf("a[4] = %i\n", a[4]);
    printf("e = %i\n", e);
    printf("*f = %i\n", *f);
    
}