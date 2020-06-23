# General metrics
from ansiblemetrics.general.loc   import LOC
from ansiblemetrics.general.bloc  import BLOC
from ansiblemetrics.general.cloc  import CLOC
from ansiblemetrics.general.nun   import NUN

# Playbook scope
from ansiblemetrics.playbook.nts  import NTS
from ansiblemetrics.playbook.nbl   import NBL
from ansiblemetrics.playbook.npl   import NPL

# Tasks scope
from ansiblemetrics.task.atss  import ATSS
from ansiblemetrics.task.ntvr  import NTVR

general_metrics ={
    'loc'   :   LOC, 
    'bloc'  :   BLOC, 
    'cloc'  :   CLOC,
    'nun'   :   NUN
}

playbook_metrics = {
    'npl'   :   NPL,
    'nbl'   :   NBL,
    'nts'  :    NTS
}

tasks_metrics = {
    'atss'  :   ATSS, 
    'ntvr'  :   NTVR
}