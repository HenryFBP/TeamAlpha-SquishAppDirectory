import os
from typing import Dict
import yaml
from pprint import pprint
from git import Repo


"""
Given a SquishAppDirectory URI, return the contents of the YAML file as a Dict. 
"""
def fetch_directory_uri(duri:str)->Dict:
    # 1. clone repo
    # 2. read yaml file
    # 3. return object
    pass

"""
Given a Git remote URI, return the name of the repository.
"""
def parse_git_remote_to_repository_name(git_remote:str)->str:
    rightmost = git_remote.split('/')[-1]
    if rightmost.endswith('.git'):
        rightmost = rightmost[0:(-1*len('.git'))]
    return rightmost


if __name__ == '__main__':
    with open('SquishAppDirectory.yaml') as f:
        appDir = yaml.safe_load(f)

        pprint(appDir)

        directoryURIs = appDir['directory-uris']

        print("Found {} directory URIs:".format(len(directoryURIs)))

        for repoURI in directoryURIs:
            print("- {}".format(repoURI))

        if not os.path.exists("./.SquishAppRepos"):
            os.makedirs("./.SquishAppRepos")

        # go through all of our SquishAppDirectory URIs
        for repoURI in directoryURIs:

            print()
            print("Loading {} ...".format(repoURI))

            repoName = parse_git_remote_to_repository_name(repoURI)
            subDirPath = "./.SquishAppRepos/{}".format(
                repoName
            )

            # make sure the repository is cloned
            if not os.path.exists(subDirPath):
                repo = Repo.clone_from(repoURI, subDirPath)
                print("Cloned {} to {}".format(repoURI, subDirPath))                
            else:
                print("{} already exists.".format(subDirPath))
            
            # load our appDef as an object
            squishAppDefPath = os.path.join(subDirPath, 'SquishAppDef.yaml')
            with open(squishAppDefPath, 'r') as f:
                
                squishAppDef = yaml.safe_load(f)

                pprint("SquishAppDef for {} - {}".format(
                    repoName, repoURI
                ))
                pprint(squishAppDef)
