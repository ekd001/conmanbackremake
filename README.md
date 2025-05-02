# conmanbackremake

### Installer les dépendances
pip install -r requirements.txt

### Connexion front et back
- lancer le front avec **localhost:3000** et le backend avec **py manage.py runserver localhost:8000**
- Pour la base de données utiliser l'extension **database connector de vscode**, ensuite selectionner le sgbd **sqlite** ensuite retourner
dans le projet django et selectionner le chemin d'accès au fichier **db.sqlite3** et le coller dans le **champ path de sqlite de db connector** et 
crée une connection, à partir de là vous pouvez visualiser le contenu de la base de données.