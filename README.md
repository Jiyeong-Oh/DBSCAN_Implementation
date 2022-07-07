# DBSCAN_Implementation
## DBSCAN 구현으로 Clustering하기 (Clustering with DBSCAN)

DBSCAN을 파이썬으로 직접 구현하여 클러스터링해보았다.

구현한 DBSCAN은, 인자로 받은 input data file, n, Eps, Minpts에 대해 DBSCAN한 후, n개의 클러스터링 결과 output file을 생성하는 과정을 수행한다.

반복문을 돌며, 점을 방문할 때 다음 네 가지 경우 각각에 따라 재귀적으로 수행한다.

 

#### 1. 이미 process 된 점일 때

가장 먼저, 방문하려는 점이 이미 process된 것으로 확인되는 경우가 있다. 이 때는 아무 작업도 하지 않고 넘어간다.

 

#### 2. process되지 않고, border point일 때

process되지 않은 점에 대해서는 일괄적으로 그 주변 점들 (neighbors)에 대한 탐색이 필요하다. 자기 자신을 포함한 이웃의 수가 minpoint를 넘지 않는다면, 해당 점은 outlier 또는 border point일 것이다. 이 때, 자기 주변에 core point가 있는 것이 확인되면 해당 점은 border이다. Border point임이 확인되면 그 점을 방문하고, 그 점에 대해 cluster를 부여한다. 단, 가장 처음으로 방문한 점이 border일 때는, cluster가 생성되기 이전이기 때문에, 아무 조치 없이 다음 점으로 넘어가야 할 것이다.

 

#### 3. process되지 않고, outlier일 때

자기 자신을 포함한 이웃의 수가 minpoint를 넘지 않고, 주변에 core point도 존재하지 않는 경우다. 이 때는 해당 점을 방문하지 않고, 아무 조치 없이 넘어간다.

 

#### 4. process되지 않고, core일 때

재귀적인 과정이 수행되는 경우다. 점을 방문하고, 그 점에 대해 cluster를 부여한다. 이후, 해당 core의 모든 이웃들에 대해 재귀적으로 dbscan을 수행한다.
- - -
 
## 함수 생성
먼저 DBSCAN 위한 몇 가지 함수들을 정의했다.

 

### 점과 점 사이의 거리 계산 함수

```
def dist_calc(p1,p2):
    x_dist = float(p1[1]) - float(p2[1])
    y_dist = float(p1[2]) - float(p2[2])
    dist = math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2))
    return dist
 
```

해당 점이 core인지/border인지/outlier인지 등을 파악하기 위해서는, 먼저 그 이웃 점들에 대해서 알아야 한다. 위 함수는 ‘이웃’을 판단하기 위한 점 사이 거리를 계산하는 함수다.

 

### 이웃 반환 함수
```
def get_neighbors(p):
    global input_db
    neighbor_list = []
    for k in input_db:
        distance = dist_calc(p, k)
        if distance <= Eps:
            neighbor_list.append(int(k[0]))
    return input_db[np.array(neighbor_list)]
```

계산한 거리 안에 들어온 이웃들의 목록을 저장해 반환하는 함수다.

 

### DBSCAN 수행 함수
```
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
```

인자로 받은 점 p에 대해 재귀적으로 dbscan을 수행하는 함수다. 위 알고리즘 요약에서 설명한 네 가지 경우 (방문하지 않은 경우, border인 경우, outlier인 경우, core인 경우) 각각에 대해 다음 과정을 지시하고 있다.

 - - -

## DBSCAN 수행
정의한 함수들을 바탕으로, DBSCAN을 수행하는 과정은 다음과 같이 설계되었다.

 
```
process_list = [False for i in range(len(input_db))]
cluster_list = [-1 for i in range(len(input_db))]
```
먼저, 점을 방문했는지 여부를 확인하기 위한 리스트와, cluster 결과가 저장되는 리스트를 생성했다. Cluster 리스트의 기본값은 -1, 방문여부 리스트의 초기값은 False로 설정되었다.

 
```
# dbscan
class_start = 0
for i in input_db:
    dbscan(i,class_start)
    if class_start in cluster_list:
        class_start+=1
```
이후, input database에 존재하는 모든 점에 대해 DBSCAN을 수행한다. 이 때, 한 cluster를 분류하는 것이 마무리되면, 다음 clustering으로 넘어간다.

 

 

## +) Limiting the Number of Clusters

n 개의 클러스터링 결과를 원했지만, 그보다 많은 수의 클러스터링 결과가 나올 경우를 대비해, 포함되는 점의 수가 적은 extra 클러스터를 제거하는 과정을 추가해주었다.
```
# optional (eliminating extra clusters)
final_cluster_list = list(range(class_start))
cluster_count = []
for i in range(class_start):
    cluster_count.append(cluster_list.count(i))
for i in range(class_start-n):
    final_cluster_list.remove(cluster_count.index(min(cluster_count)))
    cluster_count.remove(min(cluster_count))
```
