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
# Using pgadmin locally
After logging into pgadmin, create a server by right clicking on `Server`. 
Run `docker inspect postgreslocal | grep IP` to retrieve the IP address of your local postgres container
Under the connection tab fill in the `Host name/address` with the IP address that you have just retrieved
Change the username to `postgres` and password to `mysecretpassword`

## Database
A default database called `postgres` will be created
If `foodDestroyingSystem` does not exists create it by right clicking `Database`
A prompt will appear and just populate the `database` field with `fooddestroyingsystem`

