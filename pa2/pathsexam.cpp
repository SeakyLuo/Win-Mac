// pathsexam.cpp
// cmc, 10/28/2017
// non-interactive test program for function shortest.
// Run with a test number 1 or 2 as first command line argument,
// and a starting airport code as second argument.
// For example, to run test number 2, starting from SBA, type:
//    ./pathsexam 2 SBA
// Needs files "airports.txt" and "routes.txt" in working directory.

#include <iostream>
#include <fstream>
#include <list>
#include <map>
#include <vector>
#include "wtdgraph.h"
#include "paths.h"

using namespace std;
using namespace main_savitch_15;

// Descriptions and points for each of the tests:
const size_t MANY_TESTS = 2;
const int POINTS[MANY_TESTS+1] = {
    30,  // Total points for all tests.
    15,  // Test 1 points
    15,  // Test 2 points
};
const string DESCRIPTION[MANY_TESTS+1] = {
    "tests for shortest distances and paths function",
    "Testing distances",
    "Testing paths",
};

const string APTS("airports.txt"), RTES("routes.txt");

string START;

void new_line(ifstream &in)
{
    char symbol;
    do
    {
        in.get(symbol);
    } while (symbol != '\n');
}

bool setup(wtdgraph<string> &g, size_t &start) {
    map<string,size_t> labels;
    ifstream aptstream;
    aptstream.open(APTS);
    if (aptstream.fail()) {
        cout << "missing file: " << APTS << endl;
        return false;
    }
    string s;
    size_t i = 0;
    while (aptstream >> s) {
        new_line(aptstream); // get rid of any excess data after label
        labels[s] = i++;
        g.add_vertex(s);
    }
    aptstream.close();
    if (labels.count(START) != 1) {
        cout << "\"" << START << "\" not in " << APTS << endl;
        return false;
    }
    start = labels[START];
    
    ifstream rtestream;
    rtestream.open(RTES);
    if (rtestream.fail()) {
        cout << "missing file: " << RTES << endl;
        return false;
    }
    string d;
    size_t w;
    while (rtestream >> s >> d >> w) {
        g.add_edge(labels[s], labels[d], w);
        new_line(rtestream); // get rid of any excess data after edge
    }
    rtestream.close();
    return true;
}

int test1() {
    wtdgraph<string> g;
    size_t start;
    
    if (!setup(g, start))
        return 0;
    
    size_t n = g.size();
    
    vector<size_t> distances(n);
    vector<list<size_t> > paths(n);
    shortest(g, start, distances, paths);
    
    cout << "Shortest distances (miles) to places reachable from "
        << g[start] << ":\n";
    for (size_t v = 0; v < n; ++v)
        if (distances[v] < INF && v != start)
            cout << g[v] << " " << distances[v] << endl;

    return POINTS[1];
}

int test2() {
    wtdgraph<string> g;
    size_t start;
    
    if (!setup(g, start))
        return 0;
    
    size_t n = g.size();
    
    vector<size_t> distances(n);
    vector<list<size_t> > paths(n);
    shortest(g, start, distances, paths);
    
    cout << "Shortest paths available from " << g[start] << ":\n";
    for (size_t v = 0; v < n; ++v) {
        if (distances[v] < INF && v != start) {
            size_t i = 0;
            for (size_t j : paths[v]) {
                cout << g[j];
                if (++i < paths[v].size())
                    cout << "->";
            }
            cout << endl;
        }
    }
    return POINTS[2];
}

int run_a_test(int number, const string message, int test_function( ), int max)
{
    int result;
    
    cout << endl << "START OF TEST " << number << ":" << endl;
    cout << message << " (" << max << " points)." << endl;
    result = test_function( );
    if (result > 0)
    {
        cout << "Test " << number << " may earn up to " << result;
        cout << " points.\n";
    }
    else
        cout << "Test " << number << " failed." << endl;
    cout << "END OF TEST " << number << "." << endl << endl;
    
    return result;
}

// **************************************************************************
// int main(int argc, char *argv[])
//   The main program calls one test, and prints test ID and the points
//   earned from that test.
// **************************************************************************
int main(int argc, char *argv[]) {
    typedef int (*testfunc)();
    testfunc tests[MANY_TESTS] =  // array of function pointers
    {test1, test2};
    
    if (argc > 2) {
        size_t testnum = argv[1][0] - '0';
        START = string(argv[2]);
        if (testnum > 0 && testnum <= MANY_TESTS)
            run_a_test(testnum, DESCRIPTION[testnum],
                                tests[testnum-1], POINTS[testnum]);
        else {
            cout << "bad test id: " << argv[1] << endl;
            return 1;
        }
        cout << "Completed test " << argv[1] << endl;
        cout << "Results depend on comparison to correct output.\n";
    }
    else {
        cout << "error: missing command line argument" << endl;
        cout << "usage: " << argv[0] << "  test_id  airport_code" << endl;
        return 2;
    }
    return 0;
}