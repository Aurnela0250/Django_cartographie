# GitHub Flow Guide for our Django Project

## Introduction

This document describes our Git branch strategy based on GitHub Flow, a lightweight and efficient approach adapted to our Django project. GitHub Flow allows continuous development with frequent deployments, while maintaining stable and quality code.

## Branch Structure

GitHub Flow uses a minimalist structure with only two types of branches:

1. **`main`** - The main branch

   - Always deployable to production
   - Contains stable and validated code
   - Protected against direct commits

2. **Feature branches** - Created from `main`
   - Named descriptively (e.g., `feature/auth-system`, `fix/login-error`)
   - Short lifetime
   - One branch = one feature or fix

## Branch Naming Conventions

To maintain clear organization, we will use the following prefixes for our branches:

- `feature/` - For new features

  - Example: `feature/user-authentication`
  - Example: `feature/payment-integration`

- `fix/` - For bug fixes

  - Example: `fix/login-error`
  - Example: `fix/api-response-format`

- `refactor/` - For code refactoring

  - Example: `refactor/clean-architecture-implementation`
  - Example: `refactor/performance-optimization`

- `docs/` - For documentation updates
  - Example: `docs/api-documentation`
  - Example: `docs/setup-instructions`

## Commit Message Structure

Follow this format:

```
<type>(<scope>): <short description>

<detailed description>

<references>
```

For example:

1. For a simple feature:

```bash
git commit -m "feat(auth): add password reset functionality"
```

2. For a fix with a detailed description:

```bash
git commit -m "fix(api): correct user data response format

- Ensure consistent date format across all endpoints
- Add missing user profile fields

Fixes #123"
```

The main commit types are:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation change
- `style`: Formatting (no code change)
- `refactor`: Code refactoring
- `test`: Adding or fixing tests
- `chore`: Maintenance tasks

The scope (in parentheses) is optional and indicates the concerned module (auth, api, models, etc.).

This convention makes the history more readable and facilitates automatic changelog generation.

## GitHub Flow Workflow

### 1. Branch Creation

Always start from an up-to-date `main` branch:

```bash
git checkout main
git pull
git checkout -b feature/my-new-feature
```

### 2. Development

Work on your branch by making regular commits:

```bash
# After making changes
git add .
git commit -m "Clear description of changes"
```

Commit message tips:

- Use the present imperative: "Add feature" instead of "Added feature"
- Be precise but concise (< 50 characters)
- If necessary, add details after a blank line

### 3. Regular Synchronization

Push your branch to the remote repository regularly:

```bash
git push -u origin feature/my-new-feature
```

If `main` has evolved, synchronize your branch:

```bash
git checkout main
git pull
git checkout feature/my-new-feature
git merge main
# Resolve conflicts if necessary
```

### 4. Pull Request (PR)

When your feature is ready:

1. Create a Pull Request on GitHub
2. Add a detailed description
3. Associate the PR with relevant issues
4. Request a review from at least one team member

### 5. Code Review

The review process includes:

- Checking compliance with code standards
- Functional testing
- Requirements validation

### 6. Test Deployment

Our GitHub Actions workflow automatically deploys to the test environment when a PR is created to validate changes.

### 7. Merging

Once approved and tested, the PR can be merged into `main`:

- Use "Squash and merge" to keep the history clean
- Ensure the commit message properly summarizes the changes

### 8. Production Deployment

After merging into `main`, our GitHub Actions workflow automatically deploys to production.

### 9. Branch Deletion

Once merged, delete the feature branch:

```bash
git checkout main
git pull
git branch -d feature/my-new-feature
git push origin --delete feature/my-new-feature
```

## Environment Management

We use GitHub Environments to manage our different environments:

1. **Test Environment**

   - Automatic deployment when a PR is created
   - URL: `https://test.our-project.com`

2. **Production Environment**
   - Automatic deployment after merging into `main`
   - URL: `https://our-project.com`

## Emergency Situation (hotfix)

In case of a critical bug in production:

1. Create a `fix/` branch from `main`
2. Develop and test the fix
3. Create a PR with the "Urgent" label
4. After expedited review, merge into `main`

## FAQ

### How to handle a complex feature that will take several weeks?

Break it down into smaller sub-features that can be developed and merged separately.

### How to undo a change that has already been merged?

Create a new `fix/` branch that reverts the problematic change and follow the normal process.

### Should I update my feature branch if `main` has changed?

Yes, it is recommended to regularly synchronize your branch with `main` to avoid major conflicts when merging.

---

Document created on: 03/23/2025  
Last updated: 03/23/2025

---
