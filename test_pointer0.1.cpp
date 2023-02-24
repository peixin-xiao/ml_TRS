#include <iostream>

using namespace std;

void gen(int** ptr1, int** ptr2) {
    *ptr1 = new int(42);
    *ptr2 = new int(100);
}

int main() {
    int* ptr1 = nullptr;
    int* ptr2 = nullptr;
    gen(&ptr1, &ptr2);

    // 在main函数中可以使用ptr1和ptr2指向的内存空间
    cout << "Value of ptr1: " << *ptr1 << endl;
    cout << "Value of ptr2: " << *ptr2 << endl;

    // 记得在使用完后释放分配的内存
    delete ptr1;
    delete ptr2;

    return 0;
}





