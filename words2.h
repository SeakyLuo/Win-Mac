// words2.h - version 2 of class Words

#ifndef WORDS2_H
#define WORDS2_H

template <class Item>
class words_iterator;

template<class Item>
class Words
{
public:
    typedef words_iterator<Item> iterator;
    friend class words_iterator<Item>;

    Words(unsigned int initial_capacity = 10); // revised
    Words(const Words &source); // new
    ~Words(); // new
    
    void append(Item word);
    Item& operator[] (unsigned int curr);
    Words& operator=(const Words &source); // new
    
    unsigned int size() const;
    unsigned int get_capacity() const;
    Item operator[] (unsigned int curr) const;

    iterator begin() { return iterator(0);}
    iterator end() { return iterator(used);} 
    
private:
    Item *data; // now a pointer
    unsigned int used;
    unsigned int capacity;
};

template <class Item>
class words_iterator: public std::iterator <std::forward_iterator_tag, Item>
{
    public:
        words_iterator(int myCurr) { curr=myCurr; }
        Item operator *() { return data[curr]; }
        void operator ++(){ ++curr; }
        bool operator !=(words_iterator other){ return curr!=other.curr; }
    private:
        int curr;
};

#endif
