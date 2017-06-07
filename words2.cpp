// words2.cpp - implements class Words
// (fixed size array version)
// Seaky Luo, Xingxing geng, 2017/4/25

#include <cassert>
#include "words2.h"


template<class Item>
Words<Item>::Words(unsigned int initial_capacity){
    used = 0;
    capacity = initial_capacity;
    data = new Item[capacity];
}

template<class Item>
Words<Item>::Words(const Words &source){
    operator=(source);
}

template<class Item>
Words<Item>::~Words() {
    delete [] data;
}

template<class Item>
void Words<Item>::append(Item word) {
    if (used == capacity){
        capacity = 2 * used;
        Item *new_data = new Item[capacity];
        std::copy(data,data+used,new_data);
        delete [] data;
        data = new_data;
    }
    data[used] = word;
    ++used;
}

template<class Item>
Item& Words<Item>::operator[] (unsigned int index) {
    assert(index < used);
    return data[index];
}

template<class Item>
Words<Item>& Words<Item>::operator=(const Words &source){
    if(this==&source) return *this;
    used = source.used;
    capacity = source.capacity;
    Item *new_data = new Item[capacity];
    delete [] data;
    data = new_data;
    std::copy(source.data,source.data+capacity,data);
    return *this;
}

template<class Item>
unsigned int Words<Item>::size() const {
    return used;
}

template<class Item>
unsigned int Words<Item>::get_capacity() const {
    return capacity;
}

template<class Item>
Item Words<Item>::operator[] (unsigned int index) const {
    assert(index < used);
    return data[index];
}


