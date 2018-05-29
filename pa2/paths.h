#ifndef PATHS_H
#define PATHS_H

#include <climits> // provides ULONG_MAX, maximum int
#include <list>
#include <vector>
#include <string>
#include "wtdgraph.h"
using std::vector;
using std::list;
using std::string;

const int INF = LONG_MAX;

int closest_vertex(vector<int> &distances, bool *allowed_vertices, int size){
    int dmin = INF, index;
    for(int i = 0; i < size; i++){
        if(!allowed_vertices[i] && distances[i] < dmin){
            index = i;
            dmin = distances[i];
        } 
    }
    return index;
}          

void shortest(wtdgraph &g,
              int start,
              vector<int> &distances,
              vector<list<int>> &paths){
    int size = g.size();
    bool allowed_vertices[size];
    int predecessor[size];
    // initialize
    for (int i = 0; i < size; ++i) allowed_vertices[i] = false;
    distances[start] = 0;

    cout << "Start: " << g[start] << "\n";
    for (int allowed_size = 1; allowed_size < size; ++allowed_size){
        int next = closest_vertex(distances, allowed_vertices, size);
        cout << "  Next: "<< g[next] << "\n";
        allowed_vertices[next] = true;
        for (int v = 0; v < size; ++v){
            if (!allowed_vertices[v] && g.is_edge(next, v)){
                int sum = distances[next] + g.edge_weight(next, v);
                if (sum < distances[v]){
                    distances[v] = sum;
                    predecessor[v] = next;
                    if (paths[v].size()) paths[v].clear();
                    int vertex_on_path = v;cout << "    GV: " << g[v] << '\n';
                    paths[v].push_front(vertex_on_path);
                    while (vertex_on_path != start){
                        vertex_on_path = predecessor[vertex_on_path];cout << "    Vertex: " <<g[vertex_on_path] << "\n";
                        paths[v].push_front(vertex_on_path);
                    }
                }
            }

        }
        cout << "  Distance: " << distances[next] << "\n";
    }
}
    

#endif