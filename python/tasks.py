from invoke import task, run

@task
def help(c):
    """Help."""
    print("\033[1mUSAGE:\033[0m")
    print("  inv [task]")
    print("")
    print("\033[1mTASKS:\033[0m")
    print("  install              - install Poetry and project dependencies")
    print("  install_pre_commit   - install and configure pre-commit hooks")
    print("  pre_commit           - run pre-commit hooks on all files")
    print("  recreate_env         - destroy and recreate Poetry's virtualenv")

@task
def install(c):
    """Run Poetry Install."""
    # Check to make sure Python is installed
    if not c.run("command -v python3", warn=True):
        print("Python could not be found")
        print("Please install Python")
        return

    # Check if Poetry is installed
    if not c.run("command -v poetry", warn=True):
        print("Poetry could not be found")
        print("Installing Poetry")
        c.run("curl -sSL https://install.python-poetry.org | python3 -")

    # Install the dependencies
    c.run("poetry install")

@task
def recreate_env(c):
    """Recreate Poetry virtual environment."""
    # Stop the current virtualenv if active or alternative use
    # `exit` to exit from a Poetry shell session
    c.run("deactivate || exit 0", warn=True)

    # Remove all the files of the current environment of the folder we are in
    poetry_location = c.run("poetry env info -p", hide=True).stdout.strip()
    print(f"Poetry is {poetry_location}")
    c.run(f"rm -rf {poetry_location}")

@task
def pre_commit(c):
    """Run pre commit with poetry manually."""
    c.run("poetry run pre-commit run --all-files -c .conf/.pre-commit-config.yaml")

@task
def install_pre_commit(c):
    """Install pre-commit."""
    c.run("poetry run pre-commit install")
    # Edit the pre-commit config file to change the config path
    c.run("sed -i 's|\\.pre-commit-config\\.yaml|\\.conf/\\.pre-commit-config\\.yaml|g' .git/hooks/pre-commit")

@task
def update_pre_commit(c):
    """Update pre-commit file versions lcoated in .conf/.pre-commit-config.yaml."""
    c.run("pre-commit autoupdate --bleeding-edge")