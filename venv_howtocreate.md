1. install python
    > https://www.python.org/

2. latest pip, wheel, and virtualenv 
    > py -m pip install --upgrade pip wheel setuptools virtualenv

3. delete the current venv(from powershell with administrator preivilege)
    > rm .\venv -force

2. install venv in the git root
    > py -m venv venv

3. activate the virtual environment
    > .\venv\Scripts\activate

4. install pip, whell, and virtualenv again
    > py -m pip install --upgrade pip wheel setuptools virtualenv

5. install PyQt5
    > pip install PyQt5

6. install mido
    > pip install mido<br />
    > pip install python-rtmidi

7. check with 'helloword examples'

8. setup settings.json
    ```
    {
        "python.pythonPath": "venv\\Scripts\\python.exe",
        "python.linting.pylintPath": "venv\\Scripts\\pylint.exe",
        "python.linting.pylintEnabled": true,
        "python.linting.enabled": true    
    }
    ```
9. create pylintrc (beware using utf8 for powershell)
pylint --generate-rcfile | Out-File -Encoding utf8 .pylintrc

10. pylintrc setup - ignore subdirectory    
    > Add files or directories matching the regex patterns to the blacklist.<br/>
    > regex matches against base names, not paths.
    ```
    ignore-patterns=
        **/examples/*
    ```

1.  pylintrc setup - whitelist packages using c exntensions
    > A comma-separated list of package or module names from where C extensions may be loaded.<br />
    > Extensions are loading into the active Python interpreter and may run arbitrary code.<br />
    > extension-pkg-whitelist=PyQt5, mido

12. run vscode from venv!

13. setup PYTHONPATH in venv    
    > create venv/lib/site-packages/pypron.pth <br />
    > write c:/repos/pyprone to the pypron.pth file. that's it.
