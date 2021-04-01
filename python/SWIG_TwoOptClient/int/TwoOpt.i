%module TwoOpt

%{
  #define SWIG_FILE_WITH_INIT
  #include "TwoOpt.h"
%}

%include "numpy.i"

%init %{
  import_array();
%}

%apply (double* INPLACE_ARRAY1, int DIM1) {(double* order, int length_order)};
%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(const double* cost_matrix, int size_0, int size_1)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* inf, int size_of_inf)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* cuts_group, int size_of_group)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* score_value, int size_of_score)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* visits_group, int size_of_visits_group)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double* root_visits_group, int size_of_root_visits_group)};

class TwoOpt
{
        public:
        TwoOpt ();
        ~TwoOpt ();
        double getCost (const double* cost_matrix, int size_0, int size_1, int row_number, int col_number);
        double pathCost(int* currentOrder, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node);
        int* pathSwap(int* currentOrder, int length_order, int i, int j);
        void optimize (double* order, int length_order, const double* cost_matrix, int size_0, int size_1, int departure_node, int arrival_node, double* inf, int size_of_inf, double* cuts_group, int size_of_group, double* score_value, int size_of_score, double upper_bound, double* visits_group, int size_of_visits_group, double* root_visits_group, int size_of_root_visits_group);
};
