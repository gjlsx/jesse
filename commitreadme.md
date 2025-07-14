# Commit and Push Workflow

This document outlines the standard procedure for making changes to this project.

## Step-by-Step Guide

1.  **Check for Changes:** Before making any changes, ensure your local repository is up-to-date with the remote repository.
    ```bash
    git pull
    ```

2.  **Make Your Changes:** Modify the necessary files in the project.

3.  **Check the Status:** After making your changes, use the `git status` command to see which files have been modified.
    ```bash
    git status
    ```

4.  **Stage Your Changes:** Add the files you want to commit to the staging area using the `git add` command.
    ```bash
    git add <file_name>
    ```
    To add all modified files, you can use:
    ```bash
    git add .
    ```

5.  **Commit Your Changes:** Commit the staged files with a clear and descriptive commit message.
    ```bash
    git commit -m "Your descriptive commit message"
    ```

6.  **Push to Remote:** Push your committed changes to the remote repository.
    ```bash
    git push
    ```

## Example

```bash
# Make sure you are up-to-date
git pull

# Make your changes to a file, for example, README.md

# Check the status
git status

# Stage the changed file
git add README.md

# Commit the change
git commit -m "docs: Update README.md with new instructions"

# Push the commit to the remote repository
git push
```
