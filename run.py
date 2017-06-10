from clustering import Point, clustering

__author__ = 'uritwig'
import os
import json

postreqdata = json.loads(open(os.environ['req']).read())

print postreqdata
response = open(os.environ['res'], 'w')

if "k" not in postreqdata:
    response.write(json.dumps({"status":"error",
                               "message":"parameter 'k' is mandatory"}))
    response.close()

elif "points" not in postreqdata:
    response.write(json.dumps({"status":"error",
                              "message":"parameter 'points' is mandatory"}))
    response.close()

else:
    k = postreqdata["k"]
    points = postreqdata["points"]
    point_objs = []
    for point in points:
        point_objs.append(Point(point[0],point[1]))

    km = clustering(point_objs,k)
    clusters = km.k_means(False)

    clusters_res = {}

    for cluster_key,cluster in clusters.items():
        clusters_res[cluster_key] = []
        for point in cluster:
            clusters_res[cluster_key].append([point.x,point.y])

    response = open(os.environ['res'], 'w')
    response.write(json.dumps({"status":"ok",
                            "clusters":clusters_res}))
    response.close()