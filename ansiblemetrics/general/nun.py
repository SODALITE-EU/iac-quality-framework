from collections import Counter
from ansiblemetrics.ansible_metric import AnsibleMetric
from ansiblemetrics.utils import keyValueList

class NUN(AnsibleMetric):
    """  This class implements the metric 'Number Of Unique Names' in an Ansible script. """

    def count(self, relative=False):
        """ 
        Return the number of unique names in a Ansible script. 
        relative -- if True returns the relative number of unique names over the total number of names in plays of the playbook. Default is False.
        """
        names = []

        for item in keyValueList(self.yml):  # [(key, value)]
            if item[0] == 'name':
                names.append(str(item[1]).strip())

        frequencies = Counter(names).values() # counts the elements' frequency
        nuniques = sum(1 for v in frequencies if v == 1)

        if relative:
            if len(names) == 0:
                return 0
            return float(nuniques)/float(len(names))
        else:   
            return nuniques