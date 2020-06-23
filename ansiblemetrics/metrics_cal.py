# Python modules
import argparse
import inspect
import json
import os.path
import re
import sys
from io import StringIO

import yaml

# Own modules
from ansiblemetrics.import_metrics import general_metrics, playbook_metrics, tasks_metrics

def load(path):
    """ Returns a StringIO object representing the content of the file at <path>, if any; None otherwise """
    if not os.path.isfile(path):
        return None

    content = StringIO()
    with open(path, 'r') as file:
        for line in file.readlines():
            content.write(re.sub(r'\s{2,2}', '\\t', line).expandtabs(2))

    return content


class MetricsCal():

    def _execute(self, metric, script):
        """
        Returns a triple (count, relative=None, occurrences=None) as result of the metric.
        Relative and occurrences are None by default. If the metric provides a relative or occurreces value, they will be set to their actual value
        """

        try:
            m = metric(script)
            count = m.count()

            relative = None
            occurrences = None

            # Check if the metric uses the argument 'relative' or 'occurrences.'
            spec = inspect.getfullargspec(m.count)
            if 'relative' in spec.args:
                relative = round(m.count(relative=True), 2)
            if 'occurrences' in spec.args:
                occurrences = round(m.count(occurrences=True), 2)

            return (count, relative, occurrences)

        except Exception:
            return (None, None, None)

    def _executeOnPlaybookTasks(self, script):
        try:
            yml = yaml.safe_load(script.getvalue())
            if yml is None:
                return {}

            tasks = []

            for d in yml:
                if d.get('pre_tasks') is not None:
                    tasks.extend(d.get('pre_tasks'))

                if d.get('tasks') is not None:
                    tasks.extend(d.get('tasks'))

            # using list comprehension to remove None values in list
            tasks = [i for i in tasks if i]

            if len(tasks) == 0:
                return {}

            tasks = StringIO(yaml.dump(tasks))
        except yaml.YAMLError:
            return {}

        results = {}

        for name in tasks_metrics:
            metric_tuple = self._execute(tasks_metrics[name], tasks)

            results[name] = {}
            results[name]['count'] = metric_tuple[0]

            if metric_tuple[1] is not None:
                results[name]['count_relative'] = metric_tuple[1]
            elif metric_tuple[2] is not None:
                results[name]['count_occurrences'] = metric_tuple[2]

        return results

    def execute(self, script, metrics_type):
        """
        Executes metrics on a given script and returns a dictionary of results
        script: str  -- a StringIO object representing a IaC script in Ansible
        metrics: str -- possible options: 'general', 'playbook', 'tasks', 'playbook_and_general', tasks_and_general'
        """

        metrics = general_metrics
        results = {}

        if metrics_type == 'playbook':
            metrics = playbook_metrics
            results = self._executeOnPlaybookTasks(script)

        elif metrics_type == 'tasks':
            metrics = tasks_metrics

        elif metrics_type == 'playbook_and_general':
            metrics = dict(list(general_metrics.items()) + list(playbook_metrics.items()))
            results = self._executeOnPlaybookTasks(script)

        elif metrics_type == 'tasks_and_general':
            metrics = dict(list(general_metrics.items()) + list(tasks_metrics.items()))

            # Execute metrics
        for name in metrics:
            metric_tuple = self._execute(metrics[name], script)

            results[name] = {}
            results[name]['count'] = metric_tuple[0]

            if metric_tuple[1] is not None:
                results[name]['count_relative'] = metric_tuple[1]
            elif metric_tuple[2] is not None:
                results[name]['count_occurrences'] = metric_tuple[2]

        return results

    def calculate(self, file, metrics_type):
        script = load(file)
        if script is None:
            print('\033[91m' + 'Error: failed to load the file {}. Please insert a valid file!'.format(
               file) + '\033[0m')
            sys.exit(1)

        yml = None
        try:
            yml = yaml.safe_load(script.getvalue())
            for value in yml:
                print (value)
        except yaml.YAMLError:
            print('The input file is not a yaml file')
            exit(2)

        if yml is None or len(yml) == 0:
            print('An error occurred')
            exit(2)

        # if dict(yml):
        #     yml = [yml]

        i = 0

        results = self.execute(script, metrics_type)

        script.close()
        return json.dumps(results, indent=4, sort_keys=True)
