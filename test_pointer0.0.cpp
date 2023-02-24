#include <iostream>
#include <stdio.h>
#include <tuple>
#define N 1000
int* model_generator(int* T){
    T = (int*)malloc(sizeof(int)*N);
    for(int i=0;i<N;i++){
        *(T+i) = i;
    }
    return T;
}

int* main_0(int* T1){
    //int* T1 = nullptr;
    T1 = model_generator(T1);
    // for(int i=0;i<N;i++){
    //     std::cout<<*(T1+i)<<"\n";
    // }

}
int main(){
    int* T1 = nullptr;
    T1 = main_0(T1);
    for(int i=0;i<N;i++){
         std::cout<<*(T1+i)<<"\n";
     }
}
