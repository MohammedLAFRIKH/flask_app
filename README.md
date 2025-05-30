[![Code Style: flake8](https://github.com/aya-cyber/flask_app/actions/workflows/flake8.yml/badge.svg)](https://github.com/aya-cyber/flask_app/actions/workflows/flake8.yml)

# flask_app

## Résolution de l’erreur "module 'werkzeug' has no attribute '__version__'"

Si vous obtenez l’erreur suivante lors des tests :
```
AttributeError: module 'werkzeug' has no attribute '__version__'
```
**Solution :**  
Ajoutez la dépendance suivante dans votre `requirements.txt` pour forcer une version compatible :
```
werkzeug==2.3.7
```
Puis, réinstallez les dépendances :
```
pip install -r requirements.txt
```

## Conseils pour Jenkins Pipeline

- Vérifiez que tous les outils (flake8, bandit, pip-audit, etc.) sont bien installés dans le virtualenv.
- Ajoutez une étape de nettoyage (`cleanWs()`) en début de pipeline pour éviter les conflits de fichiers.
- Si une étape échoue (ex : flake8, bandit), corrigez les erreurs avant de relancer le pipeline.
- Consultez les rapports générés (`flake8-report.xml`, `bandit-report.xml`, `flask_app.log`) dans Jenkins pour plus de détails sur la qualité et la sécurité du code.
