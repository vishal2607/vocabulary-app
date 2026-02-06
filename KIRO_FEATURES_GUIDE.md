# Kiro AI Features Guide

This guide explains Kiro's special features: Steering Docs, Specs, and Agent Hooks.

---

## Table of Contents

1. [Steering Docs](#steering-docs)
2. [Specs](#specs)
3. [Agent Hooks](#agent-hooks)
4. [Practical Examples](#practical-examples)

---

## Steering Docs

### What Are Steering Docs?

**Steering docs** are instructions that guide how Kiro AI works on your project. Think of them as "rules" or "guidelines" that Kiro follows automatically.

**Location**: `.kiro/steering/*.md`

### Your Current Steering Docs

You have 3 steering docs in your project:

1. **`product.md`** - Describes what your app does
2. **`structure.md`** - Explains your project structure and conventions
3. **`tech.md`** - Lists your technology stack and common commands

### How Steering Docs Work

Every time you ask Kiro to do something, it reads these docs first:

```
You: "Add a new field to the vocabulary model"
      ↓
Kiro reads steering docs:
  - product.md: "This is a vocabulary app..."
  - structure.md: "Models are in backend/app/models/"
  - tech.md: "We use Python 3.13, SQLAlchemy 2.0..."
      ↓
Kiro knows:
  - What your app does
  - Where to find files
  - What technologies you use
  - Your coding conventions
      ↓
Kiro makes changes following your guidelines
```

### Workspace vs Global Steering

**Workspace Steering** (`.kiro/steering/`):
- Specific to THIS project
- Only applies when working in this folder
- Example: "Use Python for backend, React for frontend"

**Global Steering** (if you had it):
- Applies to ALL your projects
- Example: "Always write comments in Spanish"
- Example: "Prefer functional programming style"

**Precedence**: Workspace steering overrides global steering

### When to Use Steering Docs

Use steering docs to tell Kiro:
- **Project conventions**: "Use snake_case for Python, camelCase for JavaScript"
- **Technology choices**: "We use pytest for testing, not unittest"
- **File organization**: "Tests go in tests/ folder, not next to source files"
- **Coding standards**: "Always add type hints to Python functions"
- **Business rules**: "User passwords must be at least 8 characters"

### Example: Adding a Steering Doc

Let's say you want Kiro to always add docstrings to Python functions:

**Create `.kiro/steering/coding-standards.md`**:
```markdown
# Coding Standards

## Python

- Always add docstrings to functions
- Use Google-style docstrings
- Include parameter types and return types

Example:
```python
def create_user(username: str, password: str) -> User:
    """
    Creates a new user with hashed password.
    
    Args:
        username: The user's username
        password: The user's plain text password
        
    Returns:
        The newly created User object
        
    Raises:
        ValueError: If username already exists
    """
    ...
```
```

Now when you ask Kiro to create a function, it will automatically add docstrings!

---

## Specs

### What Are Specs?

**Specs** (specifications) are detailed plans for building features. They're like blueprints for construction.

**Location**: `.kiro/specs/{feature-name}/`

### Your Current Spec

You have one spec: `vocabulary-visualization-app`

**Location**: `.kiro/specs/vocabulary-visualization-app/`

**Files**:
1. **`requirements.md`** - What the feature should do (user stories, acceptance criteria)
2. **`design.md`** - How to build it (architecture, data models, API design)
3. **`tasks.md`** - Step-by-step implementation tasks (checklist)

### Spec Workflow

```
1. REQUIREMENTS (What to build)
   ↓
   User stories: "As a user, I want to add vocabulary..."
   Acceptance criteria: "System must validate word length..."
   
2. DESIGN (How to build it)
   ↓
   Database schema, API endpoints, component structure
   
3. TASKS (Build it step by step)
   ↓
   [ ] Create database models
   [ ] Create API endpoints
   [ ] Create React components
   
4. IMPLEMENTATION
   ↓
   Kiro executes tasks one by one
```

### Steering Docs vs Specs

| Feature | Steering Docs | Specs |
|---------|---------------|-------|
| **Purpose** | General guidelines | Specific feature plans |
| **Scope** | Entire project | One feature |
| **Duration** | Permanent | Temporary (until feature is done) |
| **Content** | "How we work" | "What we're building" |
| **Example** | "Use Python 3.13" | "Add CSV import feature" |

**Analogy**:
- **Steering docs** = Company policies (always apply)
- **Specs** = Project plan (specific to one project)

### When to Create a Spec

Create a spec when you want to build a complex feature:
- "Add user authentication"
- "Add word cloud visualization"
- "Add mobile app support"

For simple changes, just ask Kiro directly:
- "Fix this bug"
- "Add a new field"
- "Update the README"

---

## Agent Hooks

### What Are Agent Hooks?

**Agent hooks** are automations that trigger Kiro to do something when an event happens.

Think of them as "If this happens, then do that" rules.

### Hook Events (Triggers)


**When can hooks trigger?**

1. **fileEdited** - When you save a file
2. **fileCreated** - When you create a new file
3. **fileDeleted** - When you delete a file
4. **promptSubmit** - When you send a message to Kiro
5. **agentStop** - When Kiro finishes a task
6. **userTriggered** - When you manually click a button

### Hook Actions (What Happens)

**What can hooks do?**

1. **askAgent** - Send a message to Kiro (Kiro does something)
2. **runCommand** - Run a shell command (like `npm test`)

### Hook Rules

- **askAgent** works with ALL events
- **runCommand** ONLY works with `promptSubmit` and `agentStop`
- You can't run commands when files change (security reasons)

---

## Practical Examples

### Example 1: Auto-Format Python Files

**Trigger**: When you save a Python file
**Action**: Ask Kiro to format it

**Hook**: `.kiro/hooks/format-python.json`
```json
{
  "name": "Format Python on Save",
  "version": "1.0.0",
  "description": "Automatically format Python files with black when saved",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Format the edited Python file using black style. Fix any obvious style issues."
  }
}
```

**What happens**:
1. You edit `backend/app/models/user.py`
2. You save the file
3. Hook triggers
4. Kiro formats the file automatically
5. You see the formatted code

### Example 2: Run Tests After Changes

**Trigger**: When you save a test file
**Action**: Ask Kiro to run tests

**Hook**: `.kiro/hooks/run-tests.json`
```json
{
  "name": "Run Tests on Save",
  "version": "1.0.0",
  "description": "Run pytest when test files are saved",
  "when": {
    "type": "fileEdited",
    "patterns": ["backend/tests/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Run pytest for the edited test file and show me the results. If tests fail, explain what went wrong."
  }
}
```

### Example 3: Lint Code After Kiro Finishes

**Trigger**: When Kiro finishes a task
**Action**: Run linter

**Hook**: `.kiro/hooks/lint-after-changes.json`
```json
{
  "name": "Lint After Changes",
  "version": "1.0.0",
  "description": "Run linter after Kiro makes changes",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "runCommand",
    "command": "cd backend && source venv/bin/activate && flake8 app/"
  }
}
```

### Example 4: Remind About Documentation

**Trigger**: When you create a new Python file
**Action**: Remind to add docstrings

**Hook**: `.kiro/hooks/remind-docs.json`
```json
{
  "name": "Remind About Documentation",
  "version": "1.0.0",
  "description": "Remind to add docstrings when creating new Python files",
  "when": {
    "type": "fileCreated",
    "patterns": ["backend/app/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check if the newly created Python file has docstrings. If not, add them following Google style."
  }
}
```

### Example 5: Update README After Prompt

**Trigger**: When you send a message to Kiro
**Action**: Run a command to update docs

**Hook**: `.kiro/hooks/update-readme.json`
```json
{
  "name": "Update README",
  "version": "1.0.0",
  "description": "Regenerate README after making changes",
  "when": {
    "type": "promptSubmit"
  },
  "then": {
    "type": "runCommand",
    "command": "python scripts/generate_readme.py"
  }
}
```

---

## Practical Use Cases for Your Vocabulary App

### Use Case 1: Auto-Test Backend Changes

**Problem**: You want to make sure backend changes don't break tests

**Solution**: Hook that runs tests when you edit backend code

```json
{
  "name": "Test Backend on Save",
  "version": "1.0.0",
  "description": "Run backend tests when backend code changes",
  "when": {
    "type": "fileEdited",
    "patterns": ["backend/app/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Run pytest for the backend and show me if any tests failed. Focus on tests related to the edited file."
  }
}
```

### Use Case 2: Check Frontend TypeScript Errors

**Problem**: You want to catch TypeScript errors immediately

**Solution**: Hook that checks types when you edit frontend files

```json
{
  "name": "Check TypeScript",
  "version": "1.0.0",
  "description": "Check for TypeScript errors when editing frontend files",
  "when": {
    "type": "fileEdited",
    "patterns": ["frontend/src/**/*.ts", "frontend/src/**/*.tsx"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check for TypeScript errors in the edited file. If there are errors, fix them."
  }
}
```

### Use Case 3: Update Documentation

**Problem**: You want to keep documentation in sync with code

**Solution**: Hook that reminds you to update docs

```json
{
  "name": "Update Docs Reminder",
  "version": "1.0.0",
  "description": "Remind to update documentation when API routes change",
  "when": {
    "type": "fileEdited",
    "patterns": ["backend/app/routes/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Check if the API endpoint changes require updating the README or ARCHITECTURE.md. If yes, update them."
  }
}
```

### Use Case 4: Database Migration Reminder

**Problem**: You want to remember to create migrations when models change

**Solution**: Hook that reminds you about migrations

```json
{
  "name": "Database Migration Reminder",
  "version": "1.0.0",
  "description": "Remind about database migrations when models change",
  "when": {
    "type": "fileEdited",
    "patterns": ["backend/app/models/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "The database model was changed. Remind me if I need to create a database migration or update the schema."
  }
}
```

### Use Case 5: Code Review Checklist

**Problem**: You want to ensure code quality before committing

**Solution**: Hook that runs when Kiro finishes making changes

```json
{
  "name": "Code Review Checklist",
  "version": "1.0.0",
  "description": "Run code quality checks after Kiro makes changes",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review the changes I just made. Check for: 1) Missing error handling, 2) Missing type hints, 3) Missing tests, 4) Security issues. Report any problems."
  }
}
```

---

## How to Create Hooks

### Method 1: Ask Kiro (Easiest)

Just ask me:
```
"Create a hook that runs tests when I save Python files"
```

I'll create the hook file for you!

### Method 2: Use Command Palette

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
2. Type "Open Kiro Hook UI"
3. Click to open the hooks panel
4. Click "Create New Hook"
5. Fill in the form
6. Save

### Method 3: Create Manually

1. Create folder: `.kiro/hooks/`
2. Create file: `.kiro/hooks/my-hook.json`
3. Write JSON following the schema
4. Save

---

## Hook Best Practices

### Do's

✅ **Use hooks for repetitive tasks**
- Running tests
- Formatting code
- Checking for errors

✅ **Use hooks for reminders**
- Update documentation
- Add tests
- Check security

✅ **Keep hooks simple**
- One hook = one task
- Clear, specific prompts

✅ **Use file patterns wisely**
- `*.py` - All Python files
- `backend/**/*.py` - All Python files in backend
- `tests/**/*.py` - Only test files

### Don'ts

❌ **Don't create too many hooks**
- Hooks slow down your workflow
- Only automate what's truly repetitive

❌ **Don't use hooks for complex logic**
- Hooks should be simple
- Complex tasks should be manual

❌ **Don't run slow commands on every file save**
- Running full test suite on every save = slow
- Run only relevant tests

❌ **Don't use runCommand for file events**
- Security restriction
- Use askAgent instead

---

## Viewing and Managing Hooks

### View All Hooks

1. Open Explorer panel in VS Code
2. Look for "Agent Hooks" section
3. See all your hooks listed

### Enable/Disable Hooks

1. Find the hook in Explorer
2. Right-click
3. Choose "Enable" or "Disable"

### Edit Hooks

1. Find the hook file in `.kiro/hooks/`
2. Edit the JSON
3. Save
4. Hook updates automatically

### Delete Hooks

1. Delete the JSON file from `.kiro/hooks/`
2. Or right-click in Explorer and choose "Delete"

---

## Summary

### Steering Docs
- **What**: Guidelines for how Kiro works on your project
- **Where**: `.kiro/steering/*.md`
- **When**: Always active
- **Example**: "Use Python 3.13, pytest for testing"

### Specs
- **What**: Detailed plans for building features
- **Where**: `.kiro/specs/{feature-name}/`
- **When**: While building a specific feature
- **Example**: "Build vocabulary visualization feature"

### Agent Hooks
- **What**: Automations triggered by events
- **Where**: `.kiro/hooks/*.json`
- **When**: When specific events happen (file save, etc.)
- **Example**: "Run tests when I save a file"

### Key Differences

| Feature | Steering | Specs | Hooks |
|---------|----------|-------|-------|
| **Purpose** | Guidelines | Feature plans | Automations |
| **Scope** | Whole project | One feature | Specific events |
| **Active** | Always | During feature dev | When triggered |
| **Format** | Markdown | Markdown | JSON |
| **Created** | Once | Per feature | As needed |

---

## Your Turn!

Now you understand:
- ✅ What steering docs are and how they guide Kiro
- ✅ What specs are and how they plan features
- ✅ What agent hooks are and how they automate tasks
- ✅ Practical examples for your vocabulary app

Ready to create your first hook? Just ask me!
