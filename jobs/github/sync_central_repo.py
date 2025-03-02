from dotenv import load_dotenv
from os import getenv

from github import Github
from Levenshtein import distance as levenshtein_distance
# type checking
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from utils.auth_utils import AuthUtils

# find which one is monorepo (closest levenshtein to org name)
# create if does not exist
# set the about/repo description + link
# create or update readme
# build a repo cache? lucene or whoosh? and dont update if nothing's changed

def get_central_repo(org: Organization, org_repos: PaginatedList[Repository]) -> Repository:
  return min(org_repos, key=lambda repo: levenshtein_distance(repo.name, org.name))

def sync_central_repo(org: Organization, github: Github):
  org_repos = github.get_organization(org.login).get_repos()
  central_repo = get_central_repo(org=org, org_repos=org_repos)

  # validate looks like central repo

  print(central_repo)
  # for repo in org_repos:
  #   print(repo)

def sync_central_repos(github: Github) -> None:
  orgs = github.get_user().get_orgs()
  for org in orgs:
    try:
      sync_central_repo(org=org, github=github)
    except Exception as e:
      print(f"Failed to sync central repository for org: {org.login}: ", e)

def main():
  if not load_dotenv():
    print("Failed to load enviromnent")
    return
  
  botman = getenv("BOTMAN")
  if not botman:
    print("Failed to get botman")
    return
  
  token_name = getenv("BOTMAN_SYNCCENTRALREPO_TOKEN")
  if not token_name:
    print("Failed to get token")
    return

  with Github(auth=AuthUtils.with_token(user=botman, name=token_name)) as github:
    sync_central_repos(github=github)
  
if __name__ == '__main__':
  main()