# Using pyenv
Install a version of python for this project
```bash
pyenv install 3.6.5
```

Create virtual environment for this project
```bash
pyenv virtualenv 3.6.5 foodDestroyingSystem
```

Activate virtual environment
```bash
pyenv local foodDestroyingSystem
pyenv activate foodDestroyingSystem
```
Confirm virtual environment is activated
```bash
pyenv activate foodDestroyingSystem
```

Remove virtual environment
```bash
pyenv uinstall foodDestroyingSystem
```

Configure poetry to create virtual environments inside the project's root directory (If u want to do so)
```bash
poetry config virtualenvs.in-project true
```

