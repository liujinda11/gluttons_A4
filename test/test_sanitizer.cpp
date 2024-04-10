// test_sanitizer.cpp
#include <iostream>

int main() {
    int *array = new int[100];
    array[0] = 0; // 正常使用分配的内存
    delete [] array; // 忘记删除分配的内存
    return 0;
}
