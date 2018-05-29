#include <set>      // Provides set

class graph
{
public:
    // CONSTRUCTOR
    graph( );
    graph(int initial_allocation);
    graph(const graph &source);
    // DESTRUCTOR
    virtual ~graph();
    // MODIFICATION MEMBER FUNCTIONS
    void add_vertex(const int& label);
    void add_edge(int source, int target);
    void remove_edge(int source, int target);
    int& operator [ ] (int vertex);
    virtual void resize(int new_allocation);
    graph& operator = (const graph &source);
    // CONSTANT MEMBER FUNCTIONS
    int size( ) const { return many_vertices; }
    bool is_edge(int source, int target) const;
    std::set<int> neighbors(int vertex) const;
    int operator[ ] (int vertex) const;
protected:
    int many_vertices;
    int allocated;
private:
    bool **edges;
    int *labels;
};
#include "graph.cpp"