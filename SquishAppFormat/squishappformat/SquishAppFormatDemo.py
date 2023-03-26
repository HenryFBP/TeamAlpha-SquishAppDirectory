import os
from typing import Dict
import yaml
from pprint import pprint
from git import Repo


class MergedSquishApplicationDefs(object):
    """This class stores SquishAppDefs."""

    def __init__(self) -> None:
        self.applications = []

    def __add__(self, squishAppDef: Dict):
        pprint("__add__ MergedSAD")
        pprint(squishAppDef)
        assert (squishAppDef['type'] == 'SquishAppDef')
        self.applications.append(squishAppDef['application'])
        return self

    def get_all_team_members(self):
        team_members = []
        app: Dict
        for app in self.applications:
            if 'team' in app.keys():
                if 'members' in app['team'].keys():
                    team_members.extend(app['team']['members'])
        return team_members


def fetch_directory_uri(sad_uri: Dict) -> Dict:
    """Given a SquishAppDirectory URI, clone it, and then return the contents of the YAML file as a Dict."""
    print()
    print("Loading {} ...".format(sad_uri))

    repoURI = sad_uri['uri']
    repoType = sad_uri['type']

    if (repoType != 'git'):
        raise NotImplemented(
            "Cloning non-git repositories is not currently supported!")

    repoName = parse_git_uri_to_repository_name(repoURI)

    subDirPath = "./.SquishAppRepos/{}".format(repoName)

    # 1. clone repo
    if not os.path.exists(subDirPath):
        repo = Repo.clone_from(repoURI, subDirPath)
        print("Cloned {} to {}".format(repoURI, subDirPath))
    else:
        print("{} already exists.".format(subDirPath))

    # 2. read yaml file
    squishAppDefPath = os.path.join(subDirPath, 'SquishAppDef.yaml')
    with open(squishAppDefPath, 'r') as f:

        squishAppDef = yaml.safe_load(f)

        pprint("SquishAppDef for {} - {}".format(
            repoName, sad_uri
        ))
        pprint(squishAppDef)

        # 3. return object
        return squishAppDef


def parse_git_uri_to_repository_name(git_uri: str) -> str:
    """Given a Git URI, return the name of the repository."""
    rightmost = git_uri.split('/')[-1]
    if rightmost.endswith('.git'):
        rightmost = rightmost[0:(-1*len('.git'))]
    return rightmost


if __name__ == '__main__':
    with open('../SquishAppDirectory.yaml') as f:
        appDir = yaml.safe_load(f)

        pprint(appDir)

        directoryURIs = appDir['directory-uris']

        print("Found {} directory URIs:".format(len(directoryURIs)))

        for repoURI in directoryURIs:
            print("- {}".format(repoURI))

        if not os.path.exists("./.SquishAppRepos"):
            os.makedirs("./.SquishAppRepos")

        # go through all of our SquishAppDirectory URIs
        mergedSADefs = MergedSquishApplicationDefs()
        for repoURI in directoryURIs:

            # merge our application definitions into one object, so we can query it
            squishAppDef = fetch_directory_uri(repoURI)
            mergedSADefs += squishAppDef

        print("All team members: ")
        pprint(mergedSADefs.get_all_team_members())