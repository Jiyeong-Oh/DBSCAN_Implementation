#settings
import numpy as np
import math
import sys

sys.setrecursionlimit(10**7)
input_data_file_name = sys.argv[1]
n = sys.argv[2]
Eps = sys.argv[3]
MinPts = sys.argv[4]

n= int(n)
Eps = int(Eps)
MinPts = int(MinPts)



file_path = '{}'.format(input_data_file_name)
input_num = file_path.split('.')[0]
# reading train file
with open(file_path) as f:
    lines = f.read().splitlines()
input_db = [i.split('\t') for i in lines]
input_db = np.array([np.array(i) for i in input_db])


process_list = [False for i in range(len(input_db))]
cluster_list = [-1 for i in range(len(input_db))]

# 함수들
def dist_calc(p1,p2):
    x_dist = float(p1[1]) - float(p2[1])
    y_dist = float(p1[2]) - float(p2[2])
    dist = math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))
    return dist

def get_neighbors(p):
    global input_db
    neighbor_list = []
    for k in input_db:
        distance = dist_calc(p, k)
        if distance <= Eps:
            neighbor_list.append(int(k[0]))
    return input_db[np.array(neighbor_list)]


def dbscan(p, class_num):
    global cluster_list
    global process_list
    if process_list[int(p[0])] == True:
        return
    # process 되지 않은 경우
    neighbor = get_neighbors(p)
    if len(neighbor) < MinPts: # border이나 outlier이면
        if class_num in cluster_list: # border이면
            process_list[int(p[0])] = True
            cluster_list[int(p[0])] = class_num
            return
        else:
            return
    # process 안되었고 core인 경우
    process_list[int(p[0])] = True
    cluster_list[int(p[0])] = class_num
    for i in neighbor:
        dbscan(i, class_num)

# dbscan
class_start = 0
for i in input_db:
    dbscan(i,class_start)
    if class_start in cluster_list:
        class_start+=1
        
# optional (eliminating extra clusters)
final_cluster_list = list(range(class_start))
cluster_count = []
for i in range(class_start):
    cluster_count.append(cluster_list.count(i))
for i in range(class_start-n):
    final_cluster_list.remove(cluster_count.index(min(cluster_count)))
    cluster_count.remove(min(cluster_count))

# 파일 생성   
for i in range(n):
    pos = np.where(np.array(cluster_list) == final_cluster_list[i])[0]
    # get ready to write the output file
    f = open("./{}".format("{}_cluster_{}.txt".format(input_num,i)), 'w')
    for j in range(len(pos)):
        answer = str(pos[j])+'\n'
        f.write("{}".format(answer))
    f.close()
