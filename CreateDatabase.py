import dataset
import glob
import os
db = dataset.connect('sqlite:///dataset.db')
db.text_factory = str


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
    table = db['raw_data']
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


if __name__ == '__main__':
    importData()
