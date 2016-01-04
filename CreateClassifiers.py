from monkeylearn import MonkeyLearn

# Use the API key from your account
ml = MonkeyLearn('<YOUR API KEY HERE>')

# Create a new classifier
res = ml.classifiers.create('Test Classifier')

# Get the id of the new module
module_id = res.result['classifier']['hashed_id']

# Get the id of the root node
res = ml.classifiers.detail(module_id)
root_id = res.result['sandbox_categories'][0]['id']