def dijkstra(graph,src):
	length = len(graph)
	type_ = type(graph)
	if type_ == list:
	    nodes = [i for i in xrange(length)]
	elif type_ == dict:
	    nodes = graph.keys()

	visited = [src]
	path = {src:{src:[]}}
	nodes.remove(src)
	distance_graph = {src:0}
	pre = next = pre2 = src
	list1 = []
	paths = {}

	while nodes:
	    distance = float('inf')
	    for v in visited:
	         for d in nodes:
	         	if d in graph[v].keys():
					new_dist = graph[src][v] + graph[v][d]
					if new_dist < distance:
					    distance = new_dist
					    next = d
					    pre = v
					    graph[src][d] = new_dist
					elif new_dist == distance:
						#print 'nisha'
					    #pdb.set_trace()
					    pre2 = v
					    next = d
					    graph[src][d] = new_dist
					    if d in paths.keys():
					        list1 = [i for i in path[src][pre2]]
					        list1.append(next)
					        #paths[d].append([i for i in path[src][pre2]])
					        paths[d].append(list1)
					    else:
					        paths[d] = [i for i in path[src][pre2]]
					        paths[d].append(next)


	    path[src][next] = [i for i in path[src][pre]]
	    path[src][next].append(next)
	    distance_graph[next] = distance

	    visited.append(next)
	    nodes.remove(next)
	#print "paths: " + str(paths)
    for i in path[src].keys():
        if i in paths.keys():
            if path[src][i] != paths[i]:
                path[src][i].append(paths[i])
	return distance_graph, path


if __name__ == '__main__':
    graph_list = [   [0, 2, 1, 4, 5, 1],
            [1, 0, 4, 2, 3, 4],
            [2, 1, 0, 1, 2, 4],
            [3, 5, 2, 0, 3, 3],
            [2, 4, 3, 4, 0, 1],
            [3, 4, 7, 3, 1, 0]]

    graph_dict = {  "s1":{"s1": 0, "s2": 2, "s10": 1, "s12": 4, "s5":3},
                    "s2":{"s1": 1, "s2": 0, "s10": 4, "s12": 2, "s5":2},
                    "s10":{"s1": 2, "s2": 1, "s10": 0, "s12":1, "s5":4},
                    "s12":{"s1": 3, "s2": 5, "s10": 2, "s12":0,"s5":1},
                    "s5":{"s1": 3, "s2": 5, "s10": 2, "s12":4,"s5":0},
    }

    topo_dict = {"1001":{"1001": 0, "2001": 1, "2003": 1, "2005": 1, "2007":1},
                 "1002":{"1002": 0, "2001": 1, "2003": 1, "2005": 1, "2007":1},
                 "1003":{"1003": 0, "2002": 1, "2004": 1, "2006": 1, "2008":1},
                 "1004":{"1003": 0, "2002": 1, "2004": 1, "2006": 1, "2008":1},
                 "2001":{"2001": 0, "1001": 1, "1002": 1, "3001": 1, "3002":1},
                 "2002":{"2002": 0, "1003": 1, "1004": 1, "3001": 1, "3002":1},
                 "2003":{"2003": 0, "1001": 1, "1002": 1, "3003": 1, "3004":1},
                 "2004":{"2004": 0, "1003": 1, "1004": 1, "3003": 1, "3004":1},
                 "2005":{"2005": 0, "1001": 1, "1002": 1, "3005": 1, "3006":1},
                 "2006":{"2006": 0, "1003": 1, "1004": 1, "3005": 1, "3006":1},
                 "2007":{"2007": 0, "1001": 1, "1002": 1, "3007": 1, "3008":1},
                 "2008":{"2008": 0, "1003": 1, "1004": 1, "3007": 1, "3008":1},
                 "3001":{"3001": 0, "2001": 1, "2002": 1},
                 "3002":{"3002": 0, "2001": 1, "2002": 1},
                 "3003":{"3003": 0, "2003": 1, "2004": 1},
                 "3004":{"3004": 0, "2003": 1, "2004": 1},
                 "3005":{"3005": 0, "2005": 1, "2006": 1},
                 "3006":{"3006": 0, "2005": 1, "2006": 1},
                 "3007":{"3007": 0, "2007": 1, "2008": 1},
                 "3008":{"3008": 0, "2007": 1, "2008": 1},
    			}

    #distance, path = dijkstra(graph_list, 2)
    #print distance, '\n', path
    distance, path = dijkstra(topo_dict, '3001')
    print 'path: ' + str(path)