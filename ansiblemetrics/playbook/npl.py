from ansiblemetrics.ansible_metric import AnsibleMetric

class NPL(AnsibleMetric):
    """ This class implements the metric 'Number Of Plays' in an Ansible script. """

    def count(self):
        """ Return the number of plays in a playbook. """
        plays = 0
        for play in self.yml:
            if 'hosts' in play:
                plays += 1 
        
        return plays
