#include <cassert>    // Provides assert
#include <set>        // Provides set
#include <iostream>

graph::graph ( ): many_vertices(0) {
    allocated = 10;
    edges = new bool *[allocated];
    for (int i = 0; i < allocated; ++i){
        edges[i] = new bool[allocated];
        for(int j = 0; j<allocated; ++j) edges[i][j] = false;
    }
    labels = new int [allocated];
}

graph::graph(int initial_allocation): many_vertices(0) {
    allocated = initial_allocation;
    edges = new bool *[allocated];
    for (int i = 0; i < allocated; ++i){
        edges[i] = new bool[allocated];
        for(int j = 0; j<allocated; ++j) edges[i][j] = false;
    }
    labels = new int [allocated];
}

graph::graph(const graph &source){
    operator = (source);
}

graph::~graph ( ){
    for (int i = 0; i < allocated; ++i) delete [] edges[i];
    delete [] edges;
    delete [] labels;
}

graph& graph::operator = (const graph &source){
    if(this != &source){
        if(edges) {
            for (int i = 0; i < many_vertices; ++i) delete [] edges[i];
            delete [] edges;
        }
        if(labels) delete [] labels;
        allocated = source.allocated;
        many_vertices = source.many_vertices;
        labels = new int [allocated];
        edges = new bool *[allocated];
        for (int i = 0; i < allocated; ++i){
            labels[i] = source.labels[i];
            edges[i] = new bool[allocated];
            for(int j = 0; j<allocated; ++j) edges[i][j] = source.edges[i][j];
        } 
    }
    return *this;
}

void graph::resize(int new_allocation){
    if(new_allocation < size()) return;
    bool **nedges = new bool *[new_allocation];
    int *nlabels = new int [new_allocation];
    for(int i = 0; i < new_allocation; ++i) nedges[i] = new bool [new_allocation];
    for(int i = 0; i < many_vertices; ++i){
        nlabels[i] = labels[i];
        for(int j = 0; j < many_vertices; ++j) nedges[i][j] = edges[i][j];
        delete [] edges[i];
    }
    delete [] edges; delete [] labels;
    for(int i = many_vertices; i<new_allocation; ++i) for(int j = many_vertices; j < new_allocation; ++j) nedges[i][j] = false;
    allocated = new_allocation;
    labels = nlabels;
    edges = nedges;
}

void graph::add_edge(int source, int target)
{
    assert(source < size());
    assert(target < size());
    edges[source][target] = true;
}

void graph::add_vertex(const int& label)
{
    if(allocated == many_vertices) resize(many_vertices * 2);
    
    int new_vertex_number = many_vertices++;
    for (int other_number = 0; other_number < many_vertices; ++other_number)
    {
        edges[other_number][new_vertex_number] = false;
        edges[new_vertex_number][other_number] = false;
    }
    labels[new_vertex_number] = label;
}

bool graph::is_edge(int source, int target) const
{
    assert(source < size());
    assert(target < size());
    return edges[source][target];
}

int& graph::operator[] (int vertex)
{
    assert(vertex < size());
    return labels[vertex];     // Returns a reference to the label
}

int graph::operator[] (int vertex) const
{
    assert(vertex < size());
    return labels[vertex];     // Returns only a copy of the label
}

std::set<int> graph::neighbors(int vertex) const
{
    assert(vertex < size());
    std::set<int> answer;
    for (int i = 0; i < size(); ++i)
        if (edges[vertex][i]) answer.insert(i);
    return answer;
}

void graph::remove_edge(int source, int target)
{
    assert(source < size());
    assert(target < size());
    edges[source][target] = false;
}
