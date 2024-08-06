What is the structure of the paper:

ollama run llama2

```bash
python3 -m venv venv # <- file name
```
- Sei im Ordner drinnen wo das erstellt werden muss

**AKTIVIERUNG DER VENV**
```bash
source venv/bin/activate
riccardo-dandrea-projects
```

Erstellung eine `requirements.txt`
```bash
pip freeze > requirements.txt
```

Wenn du mergen willst musst du in main branch sein und dann folgenden Befehl eingeben:
```bash
git merge feature_dataset
```
Darduch nimmst du den code von `feature_dataset` und fügst in in der `main` branch

Deleting a branch 
```bash
git branch -d <branch>
```

```bash
conda list --export > requirements.txt
```

```bash
cookiecutter https://github.com/drivendata/cookiecutter-data-science
```
