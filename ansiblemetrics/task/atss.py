import yaml
from io import StringIO

from ansiblemetrics.ansible_metric import AnsibleMetric
from ansiblemetrics.general.loc import LOC

class ATSS(AnsibleMetric):
    """ This class implements the metric 'Average Task Size' in an Ansible script. """
    
    def count(self):
        """ Return the average size of the tasks. """
        tasks = self.yml
        size = 0
        for task in tasks:
            size += self.__loc(task)

        return int(round(size/len(tasks)))

    def __loc(self, task:dict):
        """ Returns the size of a task"""
        plainYaml = StringIO(yaml.dump(task))
        return LOC(plainYaml).count()