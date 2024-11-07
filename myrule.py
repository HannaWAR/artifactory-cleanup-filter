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
        # List will contain fresh files at the beginning
        artifacts.sort(key=lambda x: sortByUsage(x), reverse=True)

        keptSize = 0
        for artifact in artifacts:
            keptSize += artifact["size"]
            if keptSize > self.keepAtMostBytes:
                # No need to keep files if overflow occurs
                break

            artifacts.keep(artifact)

        return artifacts


# Register your rule in the system
register(RemoveLeastRecentUsedFiles)
