#ifndef _TwoOpt_H
#define _TwoOpt_H
#include<iostream>
#include <iostream>
#include <cstdlib>
using namespace std;

class TwoOpt
{
        private:
        int _a;
        int _b;



        public:
        TwoOpt ();
        ~TwoOpt ();
        double getCost (const double* cost_matrix, int size_0, int size_1, int row_number, int col_number);
        double pathCost(int* currentOrder, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node);
        int* pathSwap(int* currentOrder, int length_order, int i, int j);
        void optimize (double* order, int length_order,const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node, double* inf, int size_of_inf, double* cuts_group, int size_of_group, double* score_value, int size_of_score, double upper_bound, double* visits_group, int size_of_visits_group, double* root_visits_group, int size_of_root_visits_group);

}; // TwoOpt

#endif // _TwoOpt_H
