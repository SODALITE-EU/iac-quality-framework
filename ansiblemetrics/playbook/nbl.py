from ansiblemetrics.ansible_metric import AnsibleMetric

class NBL(AnsibleMetric):
    """ This class implements the metric 'Number Of Blocks' in an Ansible script. """

    def count(self):
        """ Return the number of blocks. """
        blocks = 0

        for task in self.yml:
            if 'block' in task:
                blocks += 1
                        
        return blocks