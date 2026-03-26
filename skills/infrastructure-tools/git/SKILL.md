---
name: git
description: Manages source code version control and collaborative workflows. Use when tracking changes, managing branches, or configuring CI/CD. Do NOT use for basic file operations (use windows-cli) or for large binary data storage (use s3).
---
# Git and GitLab

This skill provides a guide to using Git for version control and collaborating on projects with GitLab.

## Git Fundamentals

### Initial Configuration
Before you start using Git, configure your user name and email address.
```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```

### Creating a Repository
Initialize a new Git repository or clone an existing one.
```bash
# Initialize a new repository in the current directory
git init

# Clone an existing repository from a URL
git clone <repository_url>
```

### Staging and Committing
Track changes to your files by staging and committing them.
```bash
# Check the status of your working directory
git status

# Add a file to the staging area
git add <file_name>

# Add all changed files to the staging area
git add .

# Commit the staged changes with a message
git commit -m "Your descriptive commit message"
```

### Branching and Merging
Use branches to work on different features or fixes simultaneously.
```bash
# List all branches
git branch

# Create a new branch
git branch <branch_name>

# Switch to a branch
git checkout <branch_name>

# Create and switch to a new branch
git checkout -b <new_branch_name>

# Merge a branch into your current branch
git merge <branch_name>
```

### Working with Remotes
Collaborate with others by using remote repositories.
```bash
# List your remote repositories
git remote -v

# Add a new remote repository
git remote add <remote_name> <repository_url>

# Fetch changes from a remote repository
git fetch <remote_name>

# Pull changes from a remote repository
git pull <remote_name> <branch_name>

# Push your changes to a remote repository
git push <remote_name> <branch_name>
```

### Viewing History
Inspect the history of your repository.
```bash
# View the commit history
git log

# View a more concise log
git log --oneline --graph --decorate
```

## GitLab Workflow

GitLab is a web-based Git repository manager that provides features for the entire DevOps lifecycle.

### Merge Requests (MRs)
Merge Requests (or Pull Requests in other platforms) are the primary way to get your code reviewed and merged into the main branch.

1.  **Push your branch to GitLab:**
    ```bash
    git push origin your-feature-branch
    ```
2.  **Create a Merge Request:** In the GitLab UI, you will see a prompt to create a Merge Request from your newly pushed branch. Click the button, fill out the title and description, and assign a reviewer.

3.  **Review and Discussion:** Your team can now review your code, leave comments, and discuss the changes in the Merge Request.

4.  **Merging:** Once the MR is approved, it can be merged into the target branch (e.g., `main` or `develop`).

### GitLab CI/CD
GitLab has powerful built-in Continuous Integration/Continuous Deployment (CI/CD) capabilities. You define your CI/CD pipelines in a `.gitlab-ci.yml` file in the root of your repository.

**Example `.gitlab-ci.yml`:**
```yaml
stages:
  - test
  - build
  - deploy

test_job:
  stage: test
  script:
    - echo "Running tests..."
    - python -m pytest

build_job:
  stage: build
  script:
    - echo "Building the application..."
    # Add build commands here

deploy_job:
  stage: deploy
  script:
    - echo "Deploying the application..."
    # Add deployment commands here
  only:
    - main # This job only runs on the main branch
```

### Issue Tracking
GitLab provides a comprehensive issue tracking system. You can create issues for bugs, feature requests, or other tasks. You can also link issues to Merge Requests to automatically close them when the MR is merged.
