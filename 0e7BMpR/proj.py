# -*- coding: utf-8 -*-

import pickle, json


def reset(d):
    """
    """
    dd = []
    for e in d:
        if reset_group(e['Gruppo']) != 'ALTRO':
            dd.append({'Gruppo':reset_group(e['Gruppo']),
                       'Titolo':reset_degree(e['Titolo']),
                       u'età': reset_year(e['Anno_nascita']),
                       'Sesso':e['Sesso']})
    return dd


def reset_group(x):
    """
    """
    if x == 'PARTITO DEMOCRATICO': return 'PD'
    elif 'MONTI' in x: return "SC"
    elif 'IL POPOLO DELLA' in x: return 'PDL'
    elif 'MOVIMENTO 5' in x: return 'M5S'
    elif 'LEGA NORD' in x: return 'LN'
    else: return 'ALTRO'


def reset_year(x):
    """
    """
    y = 2013 - int(x)
    if y < 40: return u'<40'
    elif 40 <= y <= 60: return u'40-60'
    elif y > 60: return u'>60'

def reset_year_old(x):
    """
    """
    y = 2013 - int(x)
    if y < 25: return u'<25'
    elif 25 <= y < 30: return u'25-29'
    elif 30 <= y < 40: return u'30-39'
    elif 40 <= y < 50: return u'40-49'
    elif 50 <= y < 60: return u'50-59'
    elif y >= 60: return u'>60'

def reset_degree(x):
    """
    """
    if 'Diploma' in x or 'Liceo' in x: return 'D'
    elif 'Laurea' in x: return 'L'
    else: return 'D'

def mkord(d,p1,p2,p3,p4):
    """
    d = [{p1:x, p2:y, p3:z, p4:w},...]
    """
    nodes = {}
    links = []
    names = {}
    attributes = {}
    for e in d:
        i1 = p1+e[p1]
        i2 = i1+p2+e[p2]
        i3 = i2+p3+e[p3]
        i4 = i3+p4+e[p4]
        nodes[i1] = nodes.setdefault(i1,0) + 1
        nodes[i2] = nodes.setdefault(i2,0) + 1
        nodes[i3] = nodes.setdefault(i3,0) + 1
        nodes[i4] = nodes.setdefault(i4,0) + 1
        links.extend([(i1,i2),(i2,i3),(i3,i4)])
        names[i1] = e[p1]
        names[i2] = e[p2]
        names[i3] = e[p3]
        names[i4] = e[p4]
        attributes[i1] = set_attributes(e[p1])
        attributes[i2] = set_attributes(e[p2])
        attributes[i3] = set_attributes(e[p3])
        attributes[i4] = set_attributes(e[p4])
    return nodes, list(set(links)), names, attributes

def set_attributes(x):
    """
    """
    d = {'F':['#ff007f','#bb0202',"3",'none','Women'],
         'M':['#0000ff','#bb0202',"3",'none','Men'],
         "SC":['#C0C0C0','#bb0202','6','none','Scelta Civica'],
         "PDL":['#0097cc','#bb0202','6','none','Popolo della Libertà'],
         'PD':['#FF2400','#bb0202','6','none','Partito Democratico'],
         'M5S':['#FFD700','#bb0202','6','none','Movimento 5 Stelle'],
         'LN':['#349137','#bb0202','6','none','Lega Nord'],
         'L':['transparent','#bb0202','1','5,1','Master degree'],
         'D':['transparent','#bb0202','1','2','High school diploma'],
         u'<40':['#A7FC00','#bb0202','2','none','Age < 40'],
         u'40-60':['#7BA05B','#bb0202','2','none','40 < Age < 60'],
         u'>60':['#555555','#bb0202','2','none','Age > 60']
        }
    return d[x]


def goo():
    """
    """
    f = open('deputati.pickle')
    d = pickle.load(f)
    dd = reset(d)
    #nodes, links, names, attributes = mkord(dd,'Gruppo',u'et\xe0','Titolo','Sesso')
    #nodes ,links, names, attributes = mkord(dd,'Sesso','Gruppo',u'et\xe0','Titolo')
    nodes ,links, names, attributes = mkord(dd,'Gruppo','Sesso', u'et\xe0','Titolo')

    treegraphdict(nodes,links,names,attributes)

def set_title(x):
    """
    """
    if x in ['PDL','SC','PD','LN','M5S']: return x
    else: return None

def treegraphdict(nodes, links, names, attributes):
    """
    Returns the roots of the tree graph, given the sets of links and nodes.
    Note: it assumes the graph is a directed tree. 
    """
    #Instantiate the nodes
    d = {}
    for k,v in nodes.iteritems():
        d[k] = {'name':k,
                'title':attributes[k][4],
                'parents':None,
                '_children':[],
                'color':attributes[k][0],
                'stroke':attributes[k][1],
                'strokew':attributes[k][2],
                'stroked':attributes[k][3],
                'size': v*1000}
        #d[n[0]] = {'name':n[0], 'parent':None, 'children':[], 'color': n[1], 'size': n[2]*80000}
    #Populate parent and childs attributes
    for parent, child in links:
        d[parent]['_children'].append(d[child])
        d[child]['parents'] = d[parent]['name']
    #Return the roots
    tree = [v for v in d.itervalues() if not v['parents']]

    f = open('bubbletree.json','w')
    json.dump(tree,f)
    return None

