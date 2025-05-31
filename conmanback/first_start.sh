# Install all dependencies with pip
echo "Installing dependencies using pip"
pip install django djangorestframework drf-yasg pyjwt cryptography requests pillow pyyaml djangorestframework-simplejwt

# Install all dependencies with conda
# echo "Installing dependencies using conda"
# conda install -y -c conda-forge django djangorestframework drf-yasg pyjwt cryptography requests pillow pyyaml
# pip install djangorestframework-simplejwt

# Remove Sqlite Database file
echo "Removing db.sqlite3 file if it exists"
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
    echo "db.sqlite3 removed"
else
    echo "No db.sqlite3 file found"
fi

# Apply migrations and create mock data
echo "Applying migrations and creating mock data: Please ensure you have activated your Python environment"
python manage.py makemigrations
python manage.py migrate

# Navigate to the API directory
cd api || exit

# Run the mock data script
python mocks_data.py
echo "Mock Data Created!"
echo "You can access Admin user at code_access: admin123 , password: adminpass"
echo "You can access Utilisateur user at code_access: user123 , password: userpass"

# Return to the root directory and start the server
cd ..
echo "Starting the development server"
python manage.py runserver