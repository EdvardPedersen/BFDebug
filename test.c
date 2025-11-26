#include <stdio.h>

int main() {
    int a = 10;
    for(int i = 0; i < 10; i++) {
        a += 10;
        printf("Hello world %d\n", i);
    }
    return 0;
}
