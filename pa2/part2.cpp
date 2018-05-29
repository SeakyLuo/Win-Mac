#include <fstream>
#include <string>
#include <vector>
#include <list>
#include <set>
#include <queue>
#include <utility>
#include "wtdgraph.h"
#include "paths.h"
#include <iostream>
using namespace std;

int main(int args, char *argv[]){

    // Read file
    vector<int*> lines;
    ifstream infile;
    infile.open("pa2_ip2.txt"); //argv[1]
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

    string output1 = "";
    string output2 = "";
    priority_queue<pair<int, double>> pq;
    map<int, int> centrality_count;
    for(int i = 0; i < count; i++){
        vector<int> distances(count);
        vector<list<int>> paths(count);
        shortest(g, i, distances, paths);
        for(int j = i + 1; j < count; j++)
            output1 += to_string(g[i]) + ' ' + to_string(g[j]) + ' ' + to_string(distances[j]) + '\n';
        for(auto iter = paths.begin(); iter != paths.end(); ++iter){
            for(auto node = iter->begin(); node != iter->end(); ++node){

            }
        }
    }
    for(auto iter = centrality_count.begin(); iter != centrality_count.end(); ++iter)
        pq.push(iter->second, iter->first);
    for(int i = 0; i < g.size(); i++){
        output2 += to_string(pq.top().second) + ' ' + to_string(pq.top().first) + '\n';
        pq.pop();
    }
    
    // output1
    ofstream outfile1;
    outfile1.open("pa2_op2_1.txt"); //argv[2]
    outfile1 << output1;
    outfile1.close();

    // output2
    ofstream outfile2;
    outfile2.open("pa2_op2_2.txt"); //argv[3]
    outfile2 << output2;
    outfile2.close();

    for(auto iter = lines.begin(); iter != lines.end(); ++iter)
        delete [] *iter;
}