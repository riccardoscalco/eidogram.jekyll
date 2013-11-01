# -*- coding: utf-8 -*-
import pickle, gzip, dataset

def read_tweets_gzip(myfile):
    """
    """
    f = gzip.open(myfile)
    tweets = []
    while 1:
        try:
            tweets.append(pickle.load(f))
        except EOFError:
            return tweets


def read_tweets_db():
    """
    """
    db = dataset.connect('sqlite:///tweets.db')
    i = 0
    for t in db['tweet']:
        if t['coordinates']:
            i = i+1
            #print t['coordinates']
    print db.tables
    print db['tweet'].columns
    print len(db['tweet'])
    print i




def amo_odio():
    """
    """
    db = dataset.connect('sqlite:///tweets.db')
    amo = []
    odio = []
    tweets = []
    ids_amo = set()
    ids_odio = set()
    for tweet in db['tweet']:
        if tweet['id'] not in ids_amo and tweet['text'][0:2]!='RT' and ('ti amo' in tweet['text'] or 'io amo' in tweet['text']) and \
           'non ti amo' not in tweet['text']:
            amo.append(tweet)
            ids_amo.add(tweet['id'])
            tweets.append(wrap(tweet['text'],'ti amo','<b class="amo">','</b>'))
            tweets.append(wrap(tweet['text'],'io amo','<b class="amo">','</b>'))

        if tweet['id'] not in ids_odio and tweet['text'][0:2]!='RT' and ('ti odio' in tweet['text'] or 'io odio' in tweet['text']) and \
           'non ti odio' not in tweet['text']:
            odio.append(tweet)
            ids_odio.add(tweet['id'])
            tweets.append(wrap(tweet['text'],'ti odio','<b class="odio">','</b>'))
            tweets.append(wrap(tweet['text'],'io odio','<b class="odio">','</b>'))

    return amo, odio, tweets


def felice_triste():
    """
    """
    db = dataset.connect('sqlite:///tweets.db')
    felice = []
    triste = []
    tweets = []
    ids_felice = set()
    ids_triste = set()
    for tweet in db['tweet']:
        if tweet['id'] not in ids_felice and tweet['text'][0:2]!='RT' and \
           ('sono felice' in tweet['text'] or 'mi sento felice' in tweet['text']) and \
           'non sono felice' not in tweet['text'] and \
           'non mi sento felice' not in tweet['text']:
            felice.append(tweet)
            ids_felice.add(tweet['id'])
            tweets.append(wrap(tweet['text'],'sono felice','<b class="felice">','</b>'))
            tweets.append(wrap(tweet['text'],'mi sento felice','<b class="felice">','</b>'))

        if tweet['id'] not in ids_triste and tweet['text'][0:2]!='RT' and \
           ('sono triste' in tweet['text'] or 'mi sento triste' in tweet['text']) and \
           'non sono triste' not in tweet['text'] and \
           'non mi sento triste' not in tweet['text']:
            triste.append(tweet)
            ids_triste.add(tweet['id'])
            tweets.append(wrap(tweet['text'],'sono triste','<b class="triste">','</b>'))
            tweets.append(wrap(tweet['text'],'mi sento triste','<b class="triste">','</b>'))

    return felice, triste, tweets

def bene_male():
    """
    """
    db = dataset.connect('sqlite:///tweets.db')
    bene = []
    male = []
    tweets = []
    ids_bene = set()
    ids_male = set()
    for tweet in db['tweet']:
        if tweet['id'] not in ids_bene and tweet['text'][0:2]!='RT' and \
           ('sto bene' in tweet['text'] or 'mi sento bene' in tweet['text']) and \
           'non sto bene' not in tweet['text'] and \
           'non mi sento bene' not in tweet['text']:
            bene.append(tweet)
            ids_bene.add(tweet['id'])
            tweets.append(wrap(tweet['text'],'sto bene','<b class="bene">','</b>'))
            tweets.append(wrap(tweet['text'],'mi sento bene','<b class="bene">','</b>'))

        if tweet['id'] not in ids_male and tweet['text'][0:2]!='RT' and \
           ('sto male' in tweet['text'] or 'mi sento male' in tweet['text']) and \
           'non sto male' not in tweet['text'] and \
           'non mi sento male' not in tweet['text']:
            male.append(tweet)
            ids_male.add(tweet['id'])
            tweets.append(wrap(tweet['text'],'sto male','<b class="male">','</b>'))
            tweets.append(wrap(tweet['text'],'mi sento male','<b class="male">','</b>'))

    return bene, male, tweets


def bello_brutto():
    """
    """
    db = dataset.connect('sqlite:///tweets.db')
    bello = []
    brutto = []
    tweets = []
    ids_bello = set()
    ids_brutto = set()
    for tweet in db['tweet']:
        if tweet['id'] not in ids_bello and tweet['text'][0:2]!='RT' and \
           u'è bello' in tweet['text'] and \
           u'non è bello' not in tweet['text']:
            bello.append(tweet)
            ids_bello.add(tweet['id'])
            tweets.append(wrap(tweet['text'],u'è bello','<b class="bello">','</b>'))
        if tweet['id'] not in ids_brutto and tweet['text'][0:2]!='RT' and \
           u'è brutto' in tweet['text'] and \
           u'non è brutto' not in tweet['text']:
            brutto.append(tweet)
            ids_brutto.add(tweet['id'])
            tweets.append(wrap(tweet['text'],u'è brutto','<b class="brutto">','</b>'))
    return bello, brutto, tweets


def hist(data):
    """
    """
    # create a histogram of tweets based on 5 minutes intervals
    res = [0 for i in xrange(12*24)]
    for i in data:
        day = i['created_at'][8:10]
        time = i['created_at'][11:16].split(':')
        if (day == "28" and time[0] < "22"):
            minutes = 60 * (int(time[0])+2) + int(time[1])
            index = minutes // 5
            res[index] += 1
        elif (day == "27" and int(time[0]) >= 22):
            minutes = 60 * (int(time[0])-22) + int(time[1])
            index = minutes // 5
            res[index] += 1

    return res

def normalize(h1,h2):
    """
    """
    s = float(sum(h1) + sum(h2))
    h1 = [i/s for i in h1]
    h2 = [i/s for i in h2]
    return h1, h2


import csv, codecs
def mkcsv():
    """
    make csv file
    """
    amo, odio, t1 = amo_odio()
    felice, triste, t2 = felice_triste()
    bene, male, t3 = bene_male()
    bello, brutto, t4 = bello_brutto()


    t1.extend(t2)
    t1.extend(t3)
    t1.extend(t4)
    print "saved tweets: ", len(t1)
    with codecs.open('tweets.txt','w', 'utf-8') as outfile:
        outfile.writelines(t1)


    intervals = [5 * i for i in xrange(12*24)]
    x = ['%02d' % (i // 60) + ':' + '%02d' % (i % 60) for i in intervals]
    y1 = hist(amo)
    y2 = hist(odio)
    #y1, y2 = normalize(y1,y2)

    y3 = hist(felice)
    y4 = hist(triste)
    #y3, y4 = normalize(y3,y4)

    y5 = hist(bene)
    y6 = hist(male)
    #y5, y6 = normalize(y5,y6)

    y7 = hist(bello)
    y8 = hist(brutto)
    #y7, y8 = normalize(y7,y8)

    print len(x),len(y1),len(y2)
    with open('file.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['time','amo','odio','felice','triste','bene','male','bello','brutto'])
        for i in xrange(len(x)):
            spamwriter.writerow([str(x[i]),str(y1[i]),str(y2[i]),str(y3[i]),str(y4[i]),str(y5[i]),str(y6[i]),str(y7[i]),str(y8[i])])

def wrap(tweet, text, tagin, tagout):
    """
    wrap <text> in <tweet> with <tagin> and <tagout>.
    """
    l = len(text)
    L = len(tweet)
    i = tweet.find(text)
    if i != -1:
        return '<p>' + tweet[0:i] + tagin + text + tagout + tweet[i+l:L] + '</p>\n'
    else:
        return ''


