"""
Simple example to show how we can create our own rules in python
"""
from typing import List

from artifactory_cleanup import register
from artifactory_cleanup.rules import Rule, ArtifactsList

def checkKey(x):
    try:
        return x["stats"]["downloaded"]
    except KeyError:
        return x["created"]

class MySimpleRule(Rule):
    """For more methods look at Rule source code"""

    def __init__(self, maxSize):
        self.maxSize = maxSize

    def aql_add_filter(self, filters: List) -> List:
        print(self.maxSize)
        return filters

    def filter(self, artifacts: ArtifactsList) -> ArtifactsList:
        """I'm here just to print the list"""
        totalSize = 0
        for i in artifacts:
            totalSize += i["size"]

        artifacts.sort(key=lambda x: checkKey(x))

        artifactsForDel = ArtifactsList()
        localSize = 0
        sizeForDel = totalSize - self.maxSize
        for artifact in artifacts:
            if localSize < sizeForDel:
                localSize += artifact["size"]
                artifactsForDel.append(artifact)
            else:
                break
        return artifactsForDel


# Register your rule in the system
register(MySimpleRule)
