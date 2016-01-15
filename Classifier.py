import os
from monkeylearn import MonkeyLearn
from newspaper import Article
import logging, signal
from progressbar import ProgressBar
import Database
import feedparser




class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)

#With webscraping of anykind there are always edge cases, their needs to be
logging.basicConfig(filename='classifer.log', level=logging.DEBUG)

#setting up the monkey learn Variables
political_module_id = 'cl_YK3gBdDK'
keyword_module_id = 'ex_y7BPYzNG'
ml = MonkeyLearn(os.environ['MONKEY_LEARN_KEY'])


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])


def update_Feeds():
    for _ in xrange(Database.rssFeedCount()):

        feed = Database.getRssFeed()
        print "Updating {0}:".format(feed['publisher'])
        d = feedparser.parse(feed['link'])
        pbar = ProgressBar()
        for entry in pbar(d.entries):
            try:
                # Set a time limit
                with timeout(seconds=90):
                    # already exitis in db so we dont need to redo our work
                    if Database.articleExists(remove_non_ascii(entry["title"])):
                        continue

                    # lets download and parse the articles
                    article = Article(entry['links'][0]['href'])
                    article.download()
                    article.parse()

                    # Scaffolding out our article entries
                    # needs to have authoer in order for it to
                    # representive of the Publisher
                    if article.authors:
                        new_entry = {
                            "title": article.title,
                            "Authors": ', '.join(article.authors),
                            "Publisher": feed['publisher'],
                            "Keywords": "",
                            "ps": None,
                            "psProb": 0,
                            "text": article.text
                        }

                    # at this point we can add the data to the db
                    Database.insertArticle(new_entry)

            except Exception as e:
                print e
                logging.error(e)
                logging.error(
                    'Could not parse: {0}'.format(remove_non_ascii(entry["title"])))


def update_Classifications(qty=100):

    # get the article's text for classification
    texts =  [entry["text"] for entry in Database.get_NonClassified_Articles(qty)]

    #get the actual DB rows
    entries = Database.get_NonClassified_Articles(qty)

    #send the text to MonkeyLearn
    request = ml.classifiers.classify(political_module_id, texts, sandbox=True)


    # link the results to the entries and them save them back to the db
    for entry, result in zip(entries,request.result):
        entry["ps"] = result[0]["label"]
        entry["psProb"] = result[0]["probability"]
        Database.updateArticle(entry)



if __name__ == '__main__':

    update_Feeds()
    #update_Classifications()
