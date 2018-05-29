#ifndef WTDGRAPH_H
#define WTDGRAPH_H
#include <set>      // Provides set
#include <map>
#include <vector>
#include <cassert>
#include "graph.h"
#include <string>
#include <algorithm>
#include <iostream>

using namespace std;

class wtdgraph : public graph
{
public:
    // CONSTRUCTOR
    wtdgraph();
    wtdgraph(int initial_allocation);
    wtdgraph(const wtdgraph &source);
    // DESTRUCTOR
    virtual ~wtdgraph();
    // MODIFICATION MEMBER FUNCTIONS
    virtual void resize(int new_allocation);
    void add_edge(int source, int target, int Weight=0);
    int edge_weight(int source, int target) const;
    void remove_edge(int source, int target);
    wtdgraph& operator = (const wtdgraph &source);
private:
    map<int, int> *weight;
};

wtdgraph::wtdgraph() : graph(){
    weight = new map<int,int> [10];
}

wtdgraph::wtdgraph(int initial_allocation) : graph(initial_allocation){
    weight = new map<int,int> [initial_allocation];
}

wtdgraph::wtdgraph(const wtdgraph &source){
    operator = (source);
}

wtdgraph::~wtdgraph(){
    delete [] weight;
}

void wtdgraph::resize(int new_allocation){
    if(new_allocation < wtdgraph::size()) return;
    map<int,int> *tmp = new map<int,int> [new_allocation];
    for(int i = 0; i < wtdgraph::many_vertices; i++) tmp[i] = weight[i];
    delete [] weight;
    weight = tmp;
    graph::resize(new_allocation);
}

void wtdgraph::add_edge(int source, int target, int Weight){
    graph::add_edge(source, target);
    weight[source][target] = Weight;
}

int wtdgraph::edge_weight(int source, int target) const{
    assert(graph::is_edge(source, target));
    return weight[source][target];
}

void wtdgraph::remove_edge(int source, int target){
    graph::remove_edge(source, target);
    weight[source].erase(target);
}

wtdgraph& wtdgraph::operator=(const wtdgraph &source){
    if(this != &source){
        if(wtdgraph::many_vertices != source.many_vertices){
            delete [] weight;
            weight = new map<int, int> [source.many_vertices];
        }
        for(int i = 0; i < source.many_vertices; i++) weight[i] = source.weight[i];
        graph::operator =(source);
    }
    return *this;
}
#endif
