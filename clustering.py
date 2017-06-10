__author__ = 'uritwig'
import random as rand
import math as math

class Point:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_
    def __str__(self):
        return "Point { x: %s, y: %s }" % (str(self.x),str(self.y))

    def __repr__(self):
        return str(self)

class clustering:
    def __init__(self, points_, k_):
        self.points = points_
        self.k = k_
        self.clusters = []  #clusters of nodes
        self.means = []     #means of clusters
        self.debug = True  #debug flag
    #this method returns the next random node
    def next_random(self, index, points, clusters):
        #pick next node that has the maximum distance from other nodes
        dist = {}
        for point_1 in points:
            if self.debug:
                print 'point_1: %f %f' % (point_1.x, point_1.y)
            #compute this node distance from all other points in cluster
            for cluster in clusters.values():
                point_2 = cluster[0]
                if self.debug:
                    print 'point_2: %f %f' % (point_2.x, point_2.y)
                if point_1 not in dist:
                    dist[point_1] = math.sqrt(math.pow(point_1.x - point_2.x,2.0) + math.pow(point_1.y - point_2.y,2.0))
                else:
                    dist[point_1] += math.sqrt(math.pow(point_1.x - point_2.x,2.0) + math.pow(point_1.y - point_2.y,2.0))
        if self.debug:
            for key, value in dist.items():
                print "(%f, %f) ==> %f" % (key.x,key.y,value)
        #now let's return the point that has the maximum distance from previous nodes
        count_ = 0
        max_ = 0
        for key, value in dist.items():
            if count_ == 0:
                max_ = value
                max_point = key
                count_ += 1
            else:
                if value > max_:
                    max_ = value
                    max_point = key
        return max_point
    #this method computes the initial means
    def initial_means(self, points):
        #pick the first node at random
        point_ = rand.choice(points)

        if self.debug:
            print 'point#0: %f %f' % (point_.x, point_.y)
        clusters = dict()
        clusters.setdefault(0, []).append(point_)
        points.remove(point_)
        #now let's pick k-1 more random points
        for i in range(1, self.k):
            point_ = self.next_random(i, points, clusters)
            if self.debug:
                print 'point#%d: %f %f' % (i, point_.x, point_.y)
            #clusters.append([point_])
            clusters.setdefault(i, []).append(point_)
            points.remove(point_)
        #compute mean of clusters
        #self.print_clusters(clusters)
        self.means = self.compute_mean(clusters)
        if self.debug:
            print "initial means:"
            self.print_means(self.means)
    def compute_mean(self, clusters):
        means = []
        for cluster in clusters.values():
            mean_point = Point(0.0, 0.0)
            cnt = 0.0
            for point in cluster:
                #print "compute: point(%f,%f)" % (point.x, point.y)
                mean_point.x += point.x
                mean_point.y += point.y
                cnt += 1.0
            mean_point.x = mean_point.x/cnt
            mean_point.y = mean_point.y/cnt
            means.append(mean_point)
        return means
    #this method assign nodes to the cluster with the smallest mean
    def assign_points(self, points):
        if self.debug:
            print "assign points"
        clusters = dict()
        for point in points:
            dist = []
            if self.debug:
                print "point(%f,%f)" % (point.x, point.y)
            #find the best cluster for this node
            for mean in self.means:
                dist.append(math.sqrt(math.pow(point.x - mean.x,2.0) + math.pow(point.y - mean.y,2.0)))
            #let's find the smallest mean
            if self.debug:
                print dist
            cnt_ = 0
            index = 0
            min_ = dist[0]
            for d in dist:
                if d < min_:
                    min_ = d
                    index = cnt_
                cnt_ += 1
            if self.debug:
                print "index: %d" % index
            clusters.setdefault(index, []).append(point)
        return clusters
    def update_means(self, means, threshold):
        #check the current mean with the previous one to see if we should stop
        for i in range(len(self.means)):
            mean_1 = self.means[i]
            mean_2 = means[i]
            if self.debug:
                print "mean_1(%f,%f)" % (mean_1.x, mean_1.y)
                print "mean_2(%f,%f)" % (mean_2.x, mean_2.y)
            if math.sqrt(math.pow(mean_1.x - mean_2.x,2.0) + math.pow(mean_1.y - mean_2.y,2.0)) > threshold:
                return False
        return True
    #debug function: print cluster points
    def print_clusters(self, clusters):
        cluster_cnt = 1
        for cluster in clusters.values():
            print "nodes in cluster #%d" % cluster_cnt
            cluster_cnt += 1
            for point in cluster:
                print "point(%f,%f)" % (point.x, point.y)
    #print means
    def print_means(self, means):
        for point in means:
            print "%f %f" % (point.x, point.y)
    #k_means algorithm
    def k_means(self, plot_flag):

        if len(self.points) < self.k:
            return -1   #error
        points_ = [point for point in self.points]
        #compute the initial means

        self.initial_means(points_)
        stop = False
        while not stop:
            #assignment step: assign each node to the cluster with the closest mean
            points_ = [point for point in self.points]
            clusters = self.assign_points(points_)
            if self.debug:
                self.print_clusters(clusters)
            means = self.compute_mean(clusters)
            if self.debug:
                print "means:"
                self.print_means(means)
                print "update mean:"
            stop = self.update_means(means, 0.01)
            if not stop:
                self.means = []
                self.means = means
        self.clusters = clusters

        #plot cluster for evluation
        if plot_flag:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(111)
            markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['r', 'k', 'b', [0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
            cnt = 0
            for cluster in clusters.values():
                xs = []
                ys = []
                for point in cluster:
                    xs.append(point.x)
                    ys.append(point.y)
                ax.scatter(ys, xs, s=60, c=colors[cnt], marker=markers[cnt])
                cnt += 1
            plt.show()

        return clusters