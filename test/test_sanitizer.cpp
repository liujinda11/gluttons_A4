// test_sanitizer.cpp
#include <iostream>

int main() {
    int *array = new int[100];
    array[0] = 0; // Use allocated memory normally
    delete [] array; // Forgot to delete allocated memory
    return 0;
}
