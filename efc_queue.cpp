#include <bits/stdc++.h>
#include <limits.h>
#define V 36
using namespace std;

float graph_time[V][V];
// A utility function to find the vertex with minimum
// distance value, from the set of vertices not yet included
// in shortest path tree
int minDistance(vector<float> dist, bool sptSet[])
{

	// Initialize min value
	float min = INT_MAX, min_index;

	for (int v = 0; v < V; v++)
		if (sptSet[v] == false && dist[v] <= min)
			min = dist[v], min_index = v;

	return min_index;
}

// A utility function to print the constructed distance
// array
void printSolution(float dist[])
{
	cout << "Vertex \t Distance from Source" << endl;
	for (int i = 0; i < V; i++)
		cout << i << " \t\t\t\t" << dist[i] << endl;

}
float max(float a, float b) {
    if(a > b)
        return a;
    return b;
}
vector<float> dijkstra(float graph[V][V], int src);
float dijkstra_best(int EV_start, vector<int> EVCS, int& EVCS_chosen, vector<float> &EVCS_queue) {
    vector<float> dist  = dijkstra(graph_time, EV_start); 
    float mini = FLT_MAX;
    int temp = 0;
    float c = 0.005;// c = charging time
    for(int i = 0; i < EVCS.size(); i++) {
        if(mini > max(dist[EVCS[i]], EVCS_queue[i])) {
            mini = max(dist[EVCS[i]] ,EVCS_queue[i]);
            EVCS_chosen = EVCS[i];
            temp = i;
        }
    }
   
    EVCS_queue[temp] = mini + c;//charging
    return mini + c;
}
// Function that implements Dijkstra's single source
// shortest path algorithm for a graph represented using
// adjacency matrix representation
vector<float> dijkstra(float graph[V][V], int src)
{
    vector<float> dist(V,0);
	// float dist[V]; // The output array. dist[i] will hold the
				// shortest
	// distance from src to i

	bool sptSet[V]; // sptSet[i] will be true if vertex i is
					// included in shortest
	// path tree or shortest distance from src to i is
	// finalized

	// Initialize all distances as INFINITE and stpSet[] as
	// false
	for (int i = 0; i < V; i++)
		dist[i] = INT_MAX, sptSet[i] = false;

	// Distance of source vertex from itself is always 0
	dist[src] = 0;

	// Find shortest path for all vertices
	for (int count = 0; count < V - 1; count++) {
		// Pick the minimum distance vertex from the set of
		// vertices not yet processed. u is always equal to
		// src in the first iteration.
		int u = minDistance(dist, sptSet);

		// Mark the picked vertex as processed
		sptSet[u] = true;

		// Update dist value of the adjacent vertices of the
		// picked vertex.
		for (int v = 0; v < V; v++)

			// Update dist[v] only if is not in sptSet,
			// there is an edge from u to v, and total
			// weight of path from src to v through u is
			// smaller than current value of dist[v]
			if (!sptSet[v] && graph[u][v]
				&& dist[u] != FLT_MAX
				&& dist[u] + graph[u][v] < dist[v])
				dist[v] = dist[u] + graph[u][v];
	}

	// print the constructed distance array
	// printSolution(dist);
    // dis = dist; //maybe error
    return dist;
}

void assign_values(vector<vector<vector<float>>> &m, unordered_map<int,set<int>> adj) {
    for(int i = 1; i < V; i++) {
		//changing j = 0 -> j = i
        for(int j = i; j < V; j++) {
            if(adj[i].find(j) != adj[i].end()) {
                //random distance (in km) to each segment
                m[i][j][0] = 1.0/(rand()%50 + 1);
				m[j][i][0] = m[i][j][0];
                //random speed to each segment
                m[i][j][1] = 30 + rand()%15;
                m[j][i][1] = m[i][j][1];
                //time of each segment
                graph_time[i][j] = m[i][j][0]/m[i][j][1];;
                graph_time[j][i] = graph_time[i][j];
                // m[i][j][2] = m[i][j][0]/m[i][j][1];
                // m[j][i][2] = m[i][j][2];
            } 
        }
    }
}

int main() {
    vector<vector<vector<float>>> map(V, vector<vector<float>>(V,vector<float>(2,0)));
    unordered_map<int,set<int>> adj;
    vector<vector<int>> v(36);
    v[1] = {2,24,23};
    v[2] = {1,3,25};
    v[3] = {2,3};
    v[4] = {3,5,25};
    v[5] = {4,6,26};
    v[6] = {5,7,28};
    v[7] = {6,8,10};
    v[8] = {7,10,9};
    v[9] = {8,11};
    v[10] = {6,7,8,9,11,28};
    v[11] = {9,10,12,29};
    v[12] = {11,13};
    v[13] = {12,14,29};
    v[14] = {13,15,30};
    v[15] = {14,16};
    v[16] = {15,17,30,31};
    v[17] = {16,18,19};
    v[18] = {17,19};
    v[19] = {18,20};
    v[20] = {19,21,31,32};
    v[21] = {20,22,32};
    v[22] = {21,23,33};
    v[23] = {1,22,33};
    v[24] = {1,25,33,34};
    v[25] = {2,4,24,26};
    v[26] = {5,25,27,34};
    v[27] = {26,28,31};
    v[28] = {6,10,35};
    v[29] = {11,13,35};
    v[30] = {14,16,35};
    v[31] = {16,20,27,34};
    v[32] = {20,21,33,34};
    v[33] = {22,23,24,32};
    v[34] = {24,26,31,32};
    v[35] = {28,29,30};

    // int n = 1;
    // for(auto& i : v) {
    //     i = v[n++];
    // }
    for(int i = 1; i < V; i++) {
        set<int> s;
        for(int& j : v[i]) {
            s.insert(j);
        }
        adj[i] = s;
    }
    assign_values(map,adj);

    vector<int> EVCS = {31,16,33,10,25};
    vector<int> EVCS_best_chosen, EV_start = {16,23,29,3,9,14,25,8,34,7,11,6};
    vector<float> EVCS_queue(EVCS.size(),0);
    vector<float> EV_best_time;
    
    //Shortest Path Algorithm
    for(int i = 0; i < EV_start.size(); i++) {
        int EVCS_chosen = EVCS[0];  //default
        float optimal_time = dijkstra_best(EV_start[i], EVCS, EVCS_chosen, EVCS_queue);
        EV_best_time.push_back(optimal_time);
        EVCS_best_chosen.push_back(EVCS_chosen);
    }
    // for(int i = 0; i < V; i++) {
    //     for(int j = 0; j < V; j++) {
    //         cout << graph_time[i][j] << ", ";
    //     }
    //     cout << endl;
    // }
    unordered_map<int,int> EVCS_count;
    for(int i = 0; i < EV_start.size(); i++) {
        cout << EV_start[i] << " : " << EVCS_best_chosen[i] << " : " << EV_best_time[i] << endl;
        EVCS_count[EVCS_best_chosen[i]]++;
    }
    cout << "\nCOUNT" << endl;
    for(auto i : EVCS_count) {
        cout << i.first << " : " << i.second << endl;
    }

    return 0;
}