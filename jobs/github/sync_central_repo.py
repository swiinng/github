from dotenv import load_dotenv
from os import getenv
from string import Template

from github import Github, UnknownObjectException
from Levenshtein import ratio as levenshtein_ratio

# type checking
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from utils.auth_utils import AuthUtils

CENTRAL_REPO_DESCRIPTION_TEMPLATE = Template('A central hub for all repositories within `$orgname`')

def generate_markdown(org: Organization, central_repo: Repository, org_repos: PaginatedList[Repository]) -> bytes | str:
    markdown = f"# {org.name}\n"
    markdown += f"[{org.html_url}]({org.html_url})\n\n"
    markdown += f"_{org.description}_\n\n"
    markdown += "---\n\n"

    for repo in org_repos:
        if repo.name == '.github' or repo.name == central_repo.name:
          continue
        markdown += f"## {repo.name}\n"
        markdown += f"🔗 [Source Code]({repo.html_url})  |  🌍 [Website]({repo.homepage})\n\n"
        markdown += f"{repo.description}\n\n"

    return markdown

def update_readme(org: Organization, central_repo: Repository, org_repos: PaginatedList[Repository]) -> None:
  readme_path = "README.md"
  content = generate_markdown(org=org, central_repo=central_repo, org_repos=org_repos)
  commit_message = "Sync Central Repo — Update README.md"

  try:
    file = central_repo.get_contents(readme_path)
    central_repo.update_file(
        path=readme_path,
        message=commit_message,
        content=content,
        sha=file.sha,
    )
  except UnknownObjectException:
    central_repo.create_file(
        path=readme_path,
        message=commit_message,
        content=content,
    )

def create_central_repo(org: Organization, template_repo: Repository) -> Repository:
  return org.create_repo_from_template(
    name=org.name,
    repo=template_repo,
    description=CENTRAL_REPO_DESCRIPTION_TEMPLATE.safe_substitute(orgname=org.name),
    private=False
  )

def get_central_repo(org: Organization, org_repos: PaginatedList[Repository]) -> Repository:
  if not org_repos or not org_repos.totalCount:
    return None
  
  best_match = None
  best_score = 0

  # names should match at least x%
  for repo in org_repos:
      score = levenshtein_ratio(repo.name, org.name)
      if score > best_score and score >= 0.7:
          best_score = score
          best_match = repo

  return best_match
  
def sync_central_repo(org: Organization, template_repo: Repository, github: Github):
  org_repos = github.get_organization(org.login).get_repos()
  central_repo = get_central_repo(org=org, org_repos=org_repos)
  if not central_repo:
    central_repo = create_central_repo(org=org, template_repo=template_repo)

  # set or update repo attributes
  central_repo.edit(
    description=CENTRAL_REPO_DESCRIPTION_TEMPLATE.safe_substitute(orgname=org.name),
    homepage=org.html_url
  )

  update_readme(org=org, central_repo=central_repo, org_repos=org_repos)

def sync_central_repos(template_name: str, github: Github) -> None:
  template_repo = github.get_repo(full_name_or_id=template_name)
  
  orgs = github.get_user().get_orgs()
  for org in orgs:
    try:
      sync_central_repo(org=org, template_repo=template_repo, github=github)
      print(f"Successfully synced central repo for org `{org.name}`")
    except Exception as e:
      print(f"Failed to sync central repository for org: {org.name}: ", e)

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
  
  template_name = getenv("CENTRAL_REPO_TEMPLATE_NAME")
  if not template_name:
    print("Failed to get central repo template name")
    return

  with Github(auth=AuthUtils.with_token(user=botman, name=token_name)) as github:
    sync_central_repos(template_name=template_name, github=github)
  
if __name__ == '__main__':
  main()