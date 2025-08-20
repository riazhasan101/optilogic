# Create the main app directory
New-Item -ItemType Directory -Force -Path "app\api\auth"
New-Item -ItemType Directory -Force -Path "app\api\users"
New-Item -ItemType Directory -Force -Path "app\api\tenant"
New-Item -ItemType Directory -Force -Path "app\models"
New-Item -ItemType Directory -Force -Path "app\services"
New-Item -ItemType Directory -Force -Path "app\schemas"
New-Item -ItemType Directory -Force -Path "app\core"
New-Item -ItemType Directory -Force -Path "app\db"
New-Item -ItemType Directory -Force -Path "app\tests"

# Creating the files in the directories
New-Item -ItemType File -Force -Path "app\api\auth\__init__.py"
New-Item -ItemType File -Force -Path "app\api\auth\auth.py"
New-Item -ItemType File -Force -Path "app\api\auth\schemas.py"
New-Item -ItemType File -Force -Path "app\api\auth\dependencies.py"

New-Item -ItemType File -Force -Path "app\api\users\__init__.py"
New-Item -ItemType File -Force -Path "app\api\users\users.py"
New-Item -ItemType File -Force -Path "app\api\users\schemas.py"
New-Item -ItemType File -Force -Path "app\api\users\dependencies.py"

New-Item -ItemType File -Force -Path "app\api\tenant\__init__.py"
New-Item -ItemType File -Force -Path "app\api\tenant\tenant.py"
New-Item -ItemType File -Force -Path "app\api\tenant\schemas.py"
New-Item -ItemType File -Force -Path "app\api\tenant\dependencies.py"

New-Item -ItemType File -Force -Path "app\models\__init__.py"
New-Item -ItemType File -Force -Path "app\models\user.py"
New-Item -ItemType File -Force -Path "app\models\tenant.py"
New-Item -ItemType File -Force -Path "app\models\role.py"
New-Item -ItemType File -Force -Path "app\models\page.py"
New-Item -ItemType File -Force -Path "app\models\pages_roles.py"

New-Item -ItemType File -Force -Path "app\services\__init__.py"
New-Item -ItemType File -Force -Path "app\services\auth_service.py"
New-Item -ItemType File -Force -Path "app\services\user_service.py"
New-Item -ItemType File -Force -Path "app\services\tenant_service.py"
New-Item -ItemType File -Force -Path "app\services\role_service.py"

New-Item -ItemType File -Force -Path "app\schemas\__init__.py"
New-Item -ItemType File -Force -Path "app\schemas\user.py"
New-Item -ItemType File -Force -Path "app\schemas\tenant.py"
New-Item -ItemType File -Force -Path "app\schemas\role.py"
New-Item -ItemType File -Force -Path "app\schemas\page.py"
New-Item -ItemType File -Force -Path "app\schemas\token.py"

New-Item -ItemType File -Force -Path "app\core\__init__.py"
New-Item -ItemType File -Force -Path "app\core\config.py"
New-Item -ItemType File -Force -Path "app\core\security.py"
New-Item -ItemType File -Force -Path "app\core\logging.py"

New-Item -ItemType File -Force -Path "app\db\__init__.py"
New-Item -ItemType File -Force -Path "app\db\database.py"
New-Item -ItemType File -Force -Path "app\db\migration.py"

New-Item -ItemType File -Force -Path "app\tests\__init__.py"
New-Item -ItemType File -Force -Path "app\tests\test_auth.py"
New-Item -ItemType File -Force -Path "app\tests\test_user.py"
New-Item -ItemType File -Force -Path "app\tests\test_tenant.py"
New-Item -ItemType File -Force -Path "app\tests\test_role.py"
New-Item -ItemType File -Force -Path "app\tests\test_utils.py"

# Creating the main entry point
New-Item -ItemType File -Force -Path "app\main.py"

# Creating the requirements.txt file
New-Item -ItemType File -Force -Path "requirements.txt"

# Creating migrations folder
New-Item -ItemType Directory -Force -Path "migrations\versions"
New-Item -ItemType File -Force -Path "migrations\env.py"
New-Item -ItemType File -Force -Path "migrations\script.py.mako"

Write-Host "Project folder structure created successfully!"
