import os, sys
from monkeylearn import MonkeyLearn
import Database
import feedparser
from newspaper import Article  
import logging
from progressbar import ProgressBar
import signal

##Helpful for debugging
pbar = ProgressBar()

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

logging.basicConfig(filename='classifer.log',level=logging.DEBUG)
political_module_id = 'cl_YK3gBdDK'
keyword_module_id = 'ex_y7BPYzNG'
ml = MonkeyLearn(os.environ['MONKEY_LEARN_KEY'])


def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

def update_Feeds():
    feed = Database.getRssFeed()

    d = feedparser.parse(feed['link'])
    for entry in pbar(d.entries):
        try:
            #Set a time limit
            with timeout(seconds=90):
                #already exitis in db so we dont need to redo our work 
                if Database.articleExists(remove_non_ascii(entry["title"])):
                    continue

                #lets download and parse the articles
                article = Article(entry['links'][0]['href'])
                article.download()
                article.parse()

                #Scaffolding out our article entries
                #needs to have authoer in order for it to 
                # representive of the Publisher
                if article.authors:
                    new_entry = {
                        "title": article.title,
                        "Auhtors": ', '.join(article.authors),
                        "Publisher": feed['publisher'],
                        "Keywords" : "",
                        "ps" : None,
                        "psProb" : 0,
                        "text": article.text
                    }

                #at this point we can add the data to the db
                Database.insertArticle(new_entry)


        except Exception as e:
            print e
            logging.error(e)
            logging.error('Could not parse: {0}'.format(remove_non_ascii(entry["title"])))


def update_Classifications(qty=100):
    # get the articles
    entries = Database.get_NonClassified_Articles(qty)
    # just need a array of Strings
    texts = [x["text"] for x in entries ] 
    print texts
    ps =  ml.classifiers.classify(political_module_id, texts, sandbox=True)
    logging.info( ps.result)
    pass
    #Here we are going to gather non  classified articles and classify them, then save them to the db

#         logging.info( article.title)

#             #lets get the sentiment from MonkeyLearn
            
#             ps =  ml.classifiers.classify(political_module_id, article.text, sandbox=True)

#             logging.info( ps.result)
#             new_entry["ps"] = ps.result[0][0]["label"]
#             new_entry["psProb"] = ps.result[0][0]["probability"]

#             #now for to keywords
#             keywords_results =  ml.extractors.extract(keyword_module_id, article.text).result

#             for result in keywords_results:
#                 print result[0]

#             # for result in keywords["result"]:
#             #     new_entry["Keywords"] = new_entry["Keywords"] +" "+ result["keyword"]
#             print new_entry
#             break
#             # print new_entry
#         except Exception as e:
#             print e
#             logging.error(e)
#             logging.error('Could not parse: {0}'.format(remove_non_ascii(entry["title"])))



#     pass

            

if __name__ == '__main__':

    # update_Feeds()
    update_Classifications(2)