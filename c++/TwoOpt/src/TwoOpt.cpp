#include "TwoOpt.h"
#ifdef _TwoOpt_H
#include <bits/stdc++.h>
using namespace std;

const int N = 6;

// final_path[] stores the final solution ie, the
// path of the salesman.
int final_path[N+1];

// visited[] keeps track of the already visited nodes
// in a particular path
bool visited[N];

// Stores the final minimum weight of shortest tour.
int final_res = INT_MAX;

int visits_BnB[20];
int cuts_BnB[20];
int root_visits[20];
double root_score[20];

int number_of_nodes_visited = 0;
int number_of_cuts = 0;

TwoOpt::TwoOpt (){}
TwoOpt::~TwoOpt (){}

//This function takes as input
//a 2d-flattened cost matrix: cost_matrix,
//the initial number of rows of the matrix: size_0,
//the initial number of columns of the matrix: size_1,
//the row number of the desired cost: row_number,
//the column number of the desired cost: column_number,
//And returns the cost stored in the matrix at row_number and col_number: cost

double TwoOpt::getCost (const double* cost_matrix, int size_0, int size_1, int row_number, int col_number){
  double cost = cost_matrix[row_number * size_1 + col_number];
  return cost;
}


//This function takes as input
//an order for the mandatory nodes: currentOrder,
//the number of mandatory nodes: length_order,
//a 2d-flattened cost matrix: cost_matrix,
//the initial number of rows of the matrix: size_0,
//the initial number of columns of the matrix: size_1,
//the departure node in the instance: departure_node,
//the arrival node in the instance: arrival_node,
//And returns the path cost of the order currentOrder: cost

double TwoOpt::pathCost (int* currentOrder, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node){

  //cost of the path to be returned, set to 0
  double cost = 0;
  // cost of the link from the departure node to the 1st node in the order currentOrder
  cost = cost + getCost (cost_matrix, size_0, size_1, departure_node, currentOrder[0]);
  // cost of the link from the last node in the order currentOrder to the arrival node
  cost = cost + getCost (cost_matrix, size_0, size_1, currentOrder[length_order-1], arrival_node);
  //cost of all the paths linking the nodes in currentOrder
  for (int i = 0; i < length_order-1; i++){
    cost = cost + getCost (cost_matrix, size_0, size_1, currentOrder[i], currentOrder[i+1]);
  }

  return cost;
}

//This function takes as input
//an order for the mandatory nodes: currentOrder,
//the number of mandatory nodes: length_order,
//the index of the node in the order from which the swapping starts: i,
//the index of the node in the order from which the swapping ends: j,
//And returns the new path that has been swapped: newPath

int* TwoOpt::pathSwap(int* currentOrder, int length_order, int i, int j){

  //create new space for the new path
  int* newPath = (int*) malloc(length_order * sizeof(int));
  //set new path to current path
  for (int k = 0; k < length_order; k++){
    newPath[k] = currentOrder[k];
  }
  //swap the new path from i to j
  while(i<j){
    int tempI = newPath[i];
    int tempJ = newPath[j];
    newPath[i] = tempJ;
    newPath[j] = tempI;
    i++;
    j--;
  }

  return newPath;
}

// Function to copy temporary solution to
// the final solution
void copyToFinal(int curr_path[])
{
	for (int i=0; i<N; i++)
		final_path[i] = curr_path[i];
	final_path[N] = curr_path[0];
}

// Function to find the minimum edge cost
// having an end at the vertex i
int firstMin(int adj[N][N], int i)
{
	int min = INT_MAX;
	for (int k=0; k<N; k++)
		if (adj[i][k]<min && i != k)
			min = adj[i][k];
	return min;
}

// function to find the second minimum edge cost
// having an end at the vertex i
int secondMin(int adj[N][N], int i)
{
	int first = INT_MAX, second = INT_MAX;
	for (int j=0; j<N; j++)
	{
		if (i == j)
			continue;

		if (adj[i][j] <= first)
		{
			second = first;
			first = adj[i][j];
		}
		else if (adj[i][j] <= second &&
				adj[i][j] != first)
			second = adj[i][j];
	}
	return second;
}

// function that takes as arguments:
// curr_bound -> lower bound of the root node
// curr_weight-> stores the weight of the path so far
// level-> current level while moving in the search
//		 space tree
// curr_path[] -> where the solution is being stored which
//			 would later be copied to final_path[]
void TSPRec(int adj[N][N], int curr_bound, int curr_weight,
			int level, int curr_path[])
{
  number_of_nodes_visited += 1;
  if (level < 20){
    visits_BnB[level-1] += 1;
  }
  else{
    visits_BnB[19] += 1;
  }
	// base case is when we have reached level N which
	// means we have covered all the nodes once
	if (level==N)
	{
		// check if there is an edge from last vertex in
		// path back to the first vertex
		if (adj[curr_path[level-1]][curr_path[0]] != 0)
		{
			// curr_res has the total weight of the
			// solution we got
			int curr_res = curr_weight +
					adj[curr_path[level-1]][curr_path[0]];

			// Update final result and final path if
			// current result is better.
			if (curr_res < final_res)
			{
				copyToFinal(curr_path);
				final_res = curr_res;
			}
		}
		return;
	}

	// for any other level iterate for all vertices to
	// build the search space tree recursively
	for (int i=0; i<N; i++)
	{
    if(level == 1 && i==1)
      i = 2;
		// Consider next vertex if it is not same (diagonal
		// entry in adjacency matrix and not visited
		// already)
		if (adj[curr_path[level-1]][i] != 0 &&
			visited[i] == false)
		{
			int temp = curr_bound;
			curr_weight += adj[curr_path[level-1]][i];

			// different computation of curr_bound for
			// level 2 from the other levels
			if (level==1)
			curr_bound -= ((secondMin(adj, curr_path[level-1]) +
							secondMin(adj, i))/2);
			else
			curr_bound -= ((firstMin(adj, curr_path[level-1]) +
							secondMin(adj, i))/2);

			// curr_bound + curr_weight is the actual lower bound
			// for the node that we have arrived on
			// If current lower bound < final_res, we need to explore
			// the node further
			if (curr_bound + curr_weight < final_res)
			{
				curr_path[level] = i;
				visited[i] = true;

				// call TSPRec for the next level
				TSPRec(adj, curr_bound, curr_weight, level+1,
					curr_path);
			}
      else{
        number_of_cuts +=1;
        if (level < 20){
          cuts_BnB[level-1] += 1;
        }
        else{
          cuts_BnB[19] += 1;
        }

      }


			// Else we have to prune the node by resetting
			// all changes to curr_weight and curr_bound
			curr_weight -= adj[curr_path[level-1]][i];
			curr_bound = temp;


			// Also reset the visited array
			memset(visited, false, sizeof(visited));
			for (int j=0; j<=level-1; j++)
				visited[curr_path[j]] = true;
      if(level == 1){
        root_visits[i-1] = number_of_nodes_visited;
        root_score[i-1] = final_res - 2;
      }
		}
	}
}

// This function sets up final_path[]
void TSP(int adj[N][N])
{
	int curr_path[N+1];

	// Calculate initial lower bound for the root node
	// using the formula 1/2 * (sum of first min +
	// second min) for all edges.
	// Also initialize the curr_path and visited array
	int curr_bound = 0;
	memset(curr_path, -1, sizeof(curr_path));
	memset(visited, 0, sizeof(curr_path));

	// Compute initial bound
	for (int i=0; i<N; i++)
		curr_bound += (firstMin(adj, i) +
					secondMin(adj, i));

	// Rounding off the lower bound to an integer
	curr_bound = (curr_bound&1)? curr_bound/2 + 1 :
								curr_bound/2;

	// We start at vertex 1 so the first vertex
	// in curr_path[] is 0
	visited[0] = true;
	curr_path[0] = 0;

	// Call to TSPRec for curr_weight equal to
	// 0 and level 1
	TSPRec(adj, curr_bound, 0, 1, curr_path);
}



//This function takes as input
//an order for the mandatory nodes: order,
//the number of mandatory nodes: length_order,
//a 2d-flattened cost matrix: cost_matrix,
//the initial number of rows of the matrix: size_0,
//the initial number of columns of the matrix: size_1,
//the departure node in the instance: departure_node,
//the arrival node in the instance: arrival_node,
//a table where to store computation information: inf,
//the size of the information table: size_of_inf,
//!!!! order and inf are modified in memory, and exploited !!!!
//!!!! in python after the call to this function, no explicit return !!!!

void TwoOpt::optimize (double* order, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node, double* inf, int size_of_inf, double* cuts_group, int size_of_group, double* score_value, int size_of_score, double upper_bound, double* visits_group, int size_of_visits_group, double* root_visits_group, int size_of_root_visits_group) {
  if (upper_bound > 0){
    for(int i = 0; i <= N; i++){
      final_path[i] = order[i];
      final_res = upper_bound + 2;
    }
  }
  //number of swap attempts
  int attempts = 0;
  //number of swaps
  int swap_cnt = 0;
  int swap_ind = 0;
  //new container for the initial order, cast to int type.
  //this container will be optimized and copied back to order
  int* order_int = (int*) malloc(length_order * sizeof(int));
  for (int i = 0; i < length_order; i++){
    order_int[i] = (int) order[i];
  }

  //improvement boolean set to true. Will break the following loop
  //if no improvement after one iteration of twoOpt
  bool improvement = true;
  //best order found so far
  double best_distance;



  int new_cost_matrix[N][N];
  for (int i = 0; i < size_0; i++){
    for (int j = 0; j < size_1; j++){
      new_cost_matrix[i][j] = getCost (cost_matrix, size_0, size_1, i, j);
    }
  }
  for (int i = 0; i < size_0; i ++){
    new_cost_matrix[i][size_0-1] = 1000000;
  }
  for (int j = 0; j < size_0; j ++){
    new_cost_matrix[size_0-1][j] = 1000000;
  }
  new_cost_matrix[0][size_0-1] = 1;
  new_cost_matrix[size_0-1][0] = 1;
  new_cost_matrix[1][size_0-1] = 1;
  new_cost_matrix[size_0-1][1] = 1;
  //new_cost_matrix[0][1] = 1;
/*
  for (int i = 0; i < size_0; i ++){
    for(int j = 0; j < size_1; j++){
      printf("%d and %d : %f\n",i,j,new_cost_matrix[i][j]);
    }
  }*/

  for(int i=0 ; i<=size_0-1 ; i++) {
        for(int j=0 ; j<=size_1-1 ; j++)
            cout<< *(*(new_cost_matrix+i)+j)<<" ";
        cout<<endl;
    }

  for (int i = 0; i < 20; i++){
    cuts_BnB[i] = 0;
  }
  for (int i = 0; i < 20; i++){
    visits_BnB[i] = 0;
  }
  for (int i = 0; i < 20; i++){
    root_visits[i] = 0;
  }
  for (int i = 0; i < 20; i++){
    root_score[i] = INT_MAX;
  }
  number_of_nodes_visited = 0;
  number_of_cuts = 0;
  root_score[0] = final_res - 2;
  TSP(new_cost_matrix);


  final_res = final_res - 2;
  printf("Minimum cost : %d\n", final_res);
  printf("Path Taken : ");
  for (int i=0; i<=N; i++)
      printf("%d ", final_path[i]);


  //copy new order to shared memory variable
  for (int i = 0; i < length_order; i++){
    order[i] = (double) final_path[i];
  }

//shared memory variable
  inf[0] = final_res;
  inf[1] = number_of_nodes_visited;
  inf[2] = number_of_cuts;
  for (int i = 0; i < 20; i++){
    cuts_group[i] = cuts_BnB[i];
  }
  for (int i = 0; i < 20; i++){
    visits_group[i] = visits_BnB[i];
  }
  for (int i = 0; i < 20; i++){
    root_visits_group[i] = root_visits[i];
  }
  for (int i = 0; i < 20; i++){
    score_value[i] = root_score[i];
  }
  final_res = INT_MAX;
  return;
}

#endif
