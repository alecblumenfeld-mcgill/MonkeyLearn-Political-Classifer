from monkeylearn import MonkeyLearn
from apiKeys import getKey
from Database import getConservativeText, getLiberalText
from progressbar import ProgressBar
pbar = ProgressBar()

# Use the API key from your account
ml = MonkeyLearn(getKey())

text_list = ["The early actions taken by the federal government in the war focused around uniting Americans both in terms of accessibility to one another as well "]
module_id = 'cl_YK3gBdDK'
res = ml.classifiers.classify(module_id, text_list, sandbox=True)
print res.result

# # conData = getConservativeText()
# # conSamples = []
# # for entry in conData:
# #     conSamples.append((entry,con_id))
# # res = ml.classifiers.upload_samples(module_id, conSamples)


# # Now let's train the module!
# res = ml.classifiers.train(module_id)

# # Classify some texts
# res = ml.classifiers.classify(module_id, ['I love the movie', 'I hate the movie'], sandbox=True)
# print res.result