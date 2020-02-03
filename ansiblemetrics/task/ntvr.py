from ansiblemetrics.ansible_metric import AnsibleMetric
from ansiblemetrics.utils import keyValueList
import re

class NTVR(AnsibleMetric):
    """
    This class implements the metric 'Number Of Task Variables' in an Ansible script.
    We create a list of every unique task variable in the script and return the length of it.
    """

    def count(self):
        vars = set() 

        for task in self.yml:
           vars = vars.union(self.__getTaskVars(task))

        return len(vars)

    def __getTaskVars(self, task):
        """
        We check for existence of the following key-values:
            - task['include_vars']['name']
            - task['set_fact']
            - task['vars']

        As well as the 'var' and 'register' keys, and variables
        used in jinja format.
        """
        vars = set()

        if 'include_vars' in task:
            if isinstance(task['include_vars'], str):
                matches = re.findall(r'\{{2,2}\s*(\w+(\[.*\]|\.\w*)*)', task['include_vars'])
                for m in matches:
                    vars.add(str(m[0]).strip())

            elif isinstance(task['include_vars'], dict) and 'name' in task['include_vars']:
                vars.add(task['include_vars']['name'].strip())

        if 'set_fact' in task:
            if isinstance(task['set_fact'], dict):
                for var in task['set_fact'].keys():
                    vars.add(str(var))
            else:
                keyValue = task['set_fact'].split('=', 2)
                vars.add(keyValue[0].strip())
        
        if 'vars' in task:
            for item in keyValueList(task['vars']):
                vars.add(str(item[0]).strip())

        vars = vars.union(self.__setJinjaVars(task))

        for item in keyValueList(task):
            if item[0] in ['var', 'register']:
                vars.add(item[1])
        
        return vars

    def __setJinjaVars(self, d):
        """ Search for varibales defined or called using the Jinja template """
        vars = set()
        
        for item in keyValueList(d):
            matches = re.findall(r'\{{2,2}\s*(\w+(\[.*\]|\.\w*)*)', str(item[1]))
            
            for m in matches:
                vars.add(m[0].strip())
        
        return vars