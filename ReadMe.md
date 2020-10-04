# ReadMe

## Files
 - baselines.py: in this file we can find the original baselines, the RuleBased one, uses the rules defined in ````rules.json````
 and uses as its baseline BaselineBasic 
 - ML_algorithms.py: in this file, there are functions to train all of the machine learning algorithms that we considered
 to process the input
 - Reasoning.py: in this file we implemented the addition to the new features according to the rules that we defined
 - similarities.json: here we define the similarities of preferences in order to make simpler the search for alternatives
 - dialog_system.py: in this file we define the dialog manager and the possible states, it is where most of the code is,
 and it includes the structure to manage dialog and guide the user in order to fill the preferences and all the possible options
 - main.py: in this file we provide an example of use of the dialog system, we also provide the option of selecting
  any ml algorithm or the rule based baseline.
  
 ## Use
 To run our code it is necessary to install the requirements, `````pip install -r requirements.txt````` . After that run
 the main.py file with python 3.7