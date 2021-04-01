import sys
sys.path.insert(0, 'src/')
from TwoOptClient import twoOptCompute
import numpy as np
import csv

exec(open("./../input/graph.py").read())

exec(open("./pi.py").read())

order_file = open('../crt_order.txt', 'w', newline='')
no_init_file = open('../crt_no_init.txt', 'w', newline='')
with_init_file = open('../crt_with_init.txt', 'w', newline='')
compare_results = open('../crt_compare_results.txt', 'w', newline='')

no_init_mean = []
with_init_mean = []


no_init_mean_cuts = []
with_init_mean_cuts = []

no_init_mean_visits = []
with_init_mean_visits = []

no_init_mean_root_visits = []
with_init_mean_root_visits = []

no_init_mean_root_score = []
with_init_mean_root_score = []

no_init_inf = 0
with_init_inf = 0
no_init_with_init_equal = 0
improve = 0

o = open('../prob_log_crt.csv','rt')
r = csv.reader(o, delimiter=';')

print("\n............Processing the data............")
num_rows = 0
for row in r:
    num_rows += 1
o.close()
o = open('../prob_log_crt.csv','rt')
r = csv.reader(o, delimiter=';')

processed_rows = 0
for row in r:
    processed_rows +=1
    print("\n Processed %2.f %%"%(processed_rows/num_rows*100))
    depArr = row[0].split("-")
    mandatoryPassThruList = row[1].replace("[", "").replace("]", "").split(",")
    depArr = list(map(int, depArr))
    if mandatoryPassThruList[0] != '':
        mandatoryPassThruList = list(map(int, mandatoryPassThruList))
    else:
        mandatoryPassThruList = []
    depNode = depArr[0]
    arrivalNode = depArr[1]

    instance = [depNode, arrivalNode, mandatoryPassThruList]
    nv = instance.copy()
    nv[2] = instance[2].copy()
    gcn_order = pi(nv)
    order_inst = instance.copy()
    order_inst[2] = gcn_order.copy()

    order_chain = "(" + str(instance[0])+","+ str(instance[1]) + "," + "[" + ','.join(map(str, instance[2])) + "]" + "," + "[" + ','.join(map(str, gcn_order)) + "]" + ")" + ","  + "\n"
    order_file.write(order_chain)

    #without init

    results = twoOptCompute(A,instance,-1)
    path = results[0]
    solution_cost = results[1]
    mand_order_int = results[2]
    visits = results[3]
    cuts = results[4]
    compute_time = float(results[5])
    cuts_group = results[6]
    visits_group = results[7]
    root_visits_group = results[8]
    root_score = results[9]

    no_init_chain = str(instance[0])+"-"+ str(instance[1]) + ";" + "[" + ','.join(map(str, instance[2])) + "]" + ";" + "[" + ','.join(map(str, path)) + "]" + ";" + str(solution_cost) + ";" + "[" + ','.join(map(str, mand_order_int)) + "]" + ";" + str(visits) + ";" + str(cuts) + ";" + "[" + ','.join(map(str, cuts_group)) + "]" + ";" + str(compute_time) + "\n"
    no_init_file.write(no_init_chain)
    no_init_mean.append([solution_cost, visits, cuts, compute_time])
    no_init_mean_cuts.append(cuts_group)
    no_init_mean_visits.append(visits_group)
    no_init_mean_root_visits.append(root_visits_group)
    no_init_mean_root_score.append(root_score)

    #with init
    order_results = twoOptCompute(A,order_inst,1)
    order_path = order_results[0]
    order_solution_cost = order_results[1]
    order_mand_order_int = order_results[2]
    order_visits = order_results[3]
    order_cuts = order_results[4]
    order_compute_time = float(order_results[5])
    order_cuts_group = order_results[6]
    order_visits_group = order_results[7]
    order_root_visits_group = order_results[8]
    order_root_score = order_results[9]

    with_init_chain = str(instance[0])+"-"+ str(instance[1]) + ";" + "[" + ','.join(map(str, instance[2])) + "]" + ";" + "[" + ','.join(map(str, order_path)) + "]" + ";" + str(order_solution_cost) + ";" + "[" + ','.join(map(str, order_mand_order_int)) + "]" + ";" + str(order_visits) + ";" + str(order_cuts) + ";" + "[" + ','.join(map(str, order_cuts_group)) + "]" + ";" + str(order_compute_time) + "\n"
    with_init_file.write(with_init_chain)
    with_init_mean.append([order_solution_cost, order_visits, order_cuts, order_compute_time])
    with_init_mean_cuts.append(order_cuts_group)
    with_init_mean_visits.append(order_visits_group)
    with_init_mean_root_visits.append(order_root_visits_group)
    with_init_mean_root_score.append(order_root_score)

    if solution_cost < order_solution_cost:
        no_init_inf += 1
    elif order_solution_cost < solution_cost:
        with_init_inf +=1
    else:
        no_init_with_init_equal +=1
    if order_mand_order_int.tolist() != gcn_order:
        improve +=1



np_no_init_mean = np.array(no_init_mean).mean(axis=0)
np_no_init_mean_cuts = np.array(no_init_mean_cuts).mean(axis=0)
np_no_init_mean_visits = np.array(no_init_mean_visits).mean(axis=0)
np_with_init_mean = np.array(with_init_mean).mean(axis=0)
np_with_init_mean_cuts = np.array(with_init_mean_cuts).mean(axis=0)
np_with_init_mean_visits = np.array(with_init_mean_visits).mean(axis=0)
float_formatter = lambda x: "%.2f" % x
np_no_init_mean_root_visits = np.array(no_init_mean_root_visits).mean(axis=0)
np_with_init_mean_root_visits = np.array(with_init_mean_root_visits).mean(axis=0)
np_no_init_mean_root_score = np.array(no_init_mean_root_score).mean(axis=0)
np_with_init_mean_root_score = np.array(with_init_mean_root_score).mean(axis=0)

np.set_printoptions(formatter={'float_kind':float_formatter})
compare_results.write("\n NO INIT STATS : %s"%np_no_init_mean)
compare_results.write("\n WITH INIT STATS : %s"%np_with_init_mean)

compare_results.write("\n NUMBER OF TIMES NO INIT BETTER : %d  Overall percentage: %2.f"%(no_init_inf,no_init_inf/num_rows*100))
compare_results.write("\n NUMBER OF TIMES WITH INIT BETTER : %d  Overall percentage: %2.f"%(with_init_inf,with_init_inf/num_rows*100))
compare_results.write("\n NUMBER OF TIMES EQUAL : %d  Overall percentage: %2.f"%(no_init_with_init_equal,no_init_with_init_equal/num_rows*100))
compare_results.write("\n NUMBER BNB IMROVED GCN RESULT : %d  Overall percentage: %2.f"%(improve,improve/num_rows*100))


compare_results.write("\n NO INIT MEAN CUTS PER LEVEL: %s"%np_no_init_mean_cuts)
compare_results.write("\n WITH INIT MEAN CUTS PER LEVEL: %s"%np_with_init_mean_cuts)





compare_results.write("\n NO INIT MEAN VISITS PER LEVEL: %s"%np_no_init_mean_visits)
compare_results.write("\n WITH INIT MEAN VISITS PER LEVEL: %s"%np_with_init_mean_visits)


compare_results.write("\n NO INIT MEAN TOTAL ROOT VISITS AFTER EACH ROOT CHILD: %s"%np_no_init_mean_root_visits)
compare_results.write("\n WITH INIT MEAN TOTAL ROOT VISITS AFTER EACH ROOT CHILD : %s"%np_with_init_mean_root_visits)

compare_results.write("\n NO INIT MEAN ROOT VISITS PER ROOT CHILD: %s"%np.diff(np_no_init_mean_root_visits))
compare_results.write("\n WITH INIT MEAN ROOT VISITS PER ROOT CHILD : %s"%np.diff(np_with_init_mean_root_visits))


compare_results.write("\n NO INIT MEAN ROOT SCORE : %s"%np_no_init_mean_root_score)
compare_results.write("\n WITH INIT MEAN ROOT SCORE : %s"%np_with_init_mean_root_score)



o.close()
order_file.close()
no_init_file.close()
with_init_file.close()
compare_results.close()
