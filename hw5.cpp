#include <iostream>
#include "words2.h"
#include "words2.cpp"

int main(){
    typedef int value_type;
    Words<value_type> intBag;
    for(int i=0; i<3; i++) intBag.append(i);
    for(Words<value_type>::iterator iter=intBag.begin(); iter!=intBag.end(); ++iter){
        std::cout<< *iter<<"\n";
    }

    // Words<int> intBag;
    // for(int i=0; i<3; i++) intBag.append(i);
    // for(Words<int>::iterator iter=intBag.begin(); iter!=intBag.end(); ++iter){
    //     std::cout<< *iter<<"\n";
    // }
}