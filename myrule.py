"""
Simple example to show how we can create our own rules in python
"""
from typing import List

from artifactory_cleanup import register
from artifactory_cleanup.rules import Rule, ArtifactsList

def sortByUsage(x):
    try:
        return x["stats"]["downloaded"]
    except:
        return x["created"]

class RemoveLeastRecentUsedFiles(Rule):
    """
    Remove the least recently used files until the total size is kept at most passed value.
    Creation is interpreted as a first usage
    """

    def __init__(self, keepAtMostBytes):
        self.keepAtMostBytes = keepAtMostBytes

    def aql_add_filter(self, filters: List) -> List:
        return filters

    def filter(self, artifacts: ArtifactsList) -> ArtifactsList:
        totalSize = 0
        for artifact in artifacts:
            totalSize += artifact["size"]

        artifacts.sort(key=lambda x: sortByUsage(x))

        artifactsForDel = ArtifactsList()
        removedSize = 0
        maxSizeToRemove = totalSize - self.keepAtMostBytes
        for artifact in artifacts:
            if removedSize >= maxSizeToRemove:
                break

            removedSize += artifact["size"]
            artifactsForDel.append(artifact)

        return artifactsForDel


# Register your rule in the system
register(RemoveLeastRecentUsedFiles)
