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
