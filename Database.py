
import dataset
import glob
import os
import datetime
db = dataset.connect('sqlite:///database.db')
db.text_factory = str

######### Import data #############
def formatLine(string):
    toRet = string.rstrip()
    l = toRet.split("=")
    if len(l) > 1:
        toRet = l[1]
    else:
        toRet = l[0]
    return toRet.decode('utf-8', 'ignore')


def classicalViews(entry):
    """I am following the ideas put forth ni the pitt paper
     (http://people.cs.pitt.edu/~swapna/papers/SomasundaranWiebe-naaclWkshp2010.pdf)
    and thouhg i do not intended to or belive that these 
    labels are 100 percent acurate they must be applied in some fashion to classify the data"""
    if entry['stance'] == "stance1":
        entry['stance'] = 'lib'
    else:
        entry['stance'] = 'con'
    return entry


def importData():
    table = db['entries']
    topics = ['abortion', 'creation', 'gayRights', 'god', 'guns', 'healthcare']

    for t in topics:
        path = 'SomasundaranWiebe-politicalDebates/data/{0}'.format(t)
        for filename in glob.glob(os.path.join(path, '*')):
            f = open(filename, 'r')
            data = [
                f.readline().rstrip('\n') for x in xrange(4)]
            data = map(formatLine, data)
            data = dict(topic=t, stance=data[0], originalStanceText=data[
                1], originalTopic=data[2], text=data[3])
            entry = classicalViews(data)
            table.insert(entry)
        pass


def getConservativeText():
    result = db.query("SELECT text FROM entries WHERE stance='con' ")
    toRet = []
    for x in result:
        toRet.append((x['text']))
    return toRet


def getLiberalText():
    result = db.query("SELECT text FROM entries WHERE stance='lib' ")
    toRet = []
    for x in result:
        toRet.append((x['text']))
    return toRet


########### Manage Db Tables ##############
def articleExists(text):
    table = db['articles']
    if table.find_one(title=text) != None:
        return True
    else:
        return False

def insertArticle(toInsert):
    table = db['articles']
    table.insert(toInsert)
    pass

def get_NonClassified_Articles(qty):
    result = db.query('''SELECT  * 
        from articles 
        where ps IS NULL 
        Limit {0}'''.format(qty))
    return result
    # table = db['articles']
    # db.
    pass

def updateArticle(toUpdate):
    table = db['articles']
    table.update(toUpdate, ['id'])

def getRssFeed():
    table = db['rssFeeds']
    #get the feed that has not been updated the longest time ago
    result = db.query("SELECT * FROM rssFeeds ORDER BY updatedAt ASC Limit 1").next()
    t = datetime.datetime.now()
    result['updatedAt'] = (t-datetime.datetime(1970,1,1)).total_seconds()
    table.update(result, ['id'])
    return result

def rssFeedCount():
    table = db['rssFeeds']

    return len(db['rssFeeds'])

if __name__ == '__main__':
    # importData()
    pass
