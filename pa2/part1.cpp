#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include "wtdgraph.h"
#include "paths.h"
#include <iostream>
using namespace std;

int main(int args, char *argv[]){

    // Read file
    ifstream infile;
    infile.open("pa2_ip2.txt"); //argv[1]

    vector<int*> lines;
    set<int> vertices;
    string line;
    int startingNode, endingNode, weight;
    getline(infile, line);
    while(infile >> startingNode >> endingNode >> weight){
        int* arr = new int [3] { startingNode, endingNode, weight };
        for(int i = 0; i < lines.size(); i++){
            vertices.insert(startingNode);
            vertices.insert(endingNode);
        }
        lines.push_back(arr);
    }
    infile.close();

    // initialize
    wtdgraph g(vertices.size());
    int count = 0;
    map<int, int> labels;
    for(auto iter = vertices.begin(); iter != vertices.end(); ++iter){
        g.add_vertex(*iter);
        labels[*iter] = count++;
    }
    for(int i = 0; i < lines.size(); i++){
        g.add_edge(labels[lines[i][0]], labels[lines[i][1]], lines[i][2]);
    }

    // calculate shortest path for each node
    vector<int> node_distances;
    map<int, int> sum_distances;
    for(int i = 0; i < count; i++){
        vector<int> distances(count, INF);
        vector<list<int>> paths(count);
        shortest(g, i, distances, paths);
        auto max = max_element(begin(distances), end(distances));
        node_distances.push_back(*max);
        int sum = 0;
        for(int j = 0; j < count - i; j++) sum += distances[i];
        sum_distances[g[i]] = sum;
        distances.clear();
        paths.clear();
    }
    // find diameter and radius
    auto diameter = max_element(begin(node_distances), end(node_distances));
    auto radius = min_element(begin(node_distances), end(node_distances));
    string output = to_string(*diameter) + '\n' + to_string(*radius) + '\n';

    // find center
    int min_distance = sum_distances[g[0]];
    for(auto iter = sum_distances.begin(); iter != sum_distances.end(); ++iter)
        if(iter->second < min_distance)
            min_distance = iter->second;
    for(auto iter = sum_distances.begin(); iter != sum_distances.end(); ++iter)
        if(iter->second == min_distance)
            output = to_string(iter->first) + ' ';
    output += '\n';
    
    ofstream outfile;
    outfile.open("pa2_op1.txt"); //argv[2]
    outfile << output;
    outfile.close();
}

int MaxDistance(vector<int>& distances){
    int max = distances[0];
    for(int i = 0; i < distances.size(); i++)
        if(distances[i] != INF && max < distances[i])
            max = distances[i];
    return max;
}