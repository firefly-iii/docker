#!/bin/bash

echo "Now in entrypoint.sh for Firefly III"
echo "Entrypoint script version is 1.0.1"

# https://github.com/docker-library/wordpress/blob/master/docker-entrypoint.sh
# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
		exit 1
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}

# envs that can be appended with _FILE
envs=(
	SITE_OWNER
	APP_KEY
	DB_CONNECTION
	DB_HOST
	DB_PORT
	DB_DATABASE
	DB_USERNAME
	DB_PASSWORD
	PGSQL_SSL_MODE
	PGSQL_SSL_ROOT_CERT
	PGSQL_SSL_CERT
	PGSQL_SSL_KEY
	PGSQL_SSL_CRL_FILE
	REDIS_HOST
	REDIS_PASSWORD
	REDIS_PORT
	COOKIE_DOMAIN
	MAIL_DRIVER
	MAIL_HOST
	MAIL_PORT
	MAIL_FROM
	MAIL_USERNAME
	MAIL_PASSWORD
	MAIL_ENCRYPTION
	MAILGUN_DOMAIN
	MAILGUN_SECRET
	MAILGUN_ENDPOINT
	MANDRILL_SECRET
	SPARKPOST_SECRET
	MAPBOX_API_KEY
	FIXER_API_KEY
	LOGIN_PROVIDER
	ADLDAP_CONNECTION_SCHEME
	ADLDAP_CONTROLLERS
	ADLDAP_PORT
	ADLDAP_BASEDN
	ADLDAP_ADMIN_USERNAME
	ADLDAP_ADMIN_PASSWORD
	ADLDAP_ACCOUNT_PREFIX
	ADLDAP_ACCOUNT_SUFFIX
	WINDOWS_SSO_DISCOVER
	WINDOWS_SSO_KEY
	ADLDAP_SYNC_FIELD
	TRACKER_SITE_ID
	TRACKER_URL
)

echo "Now parsing _FILE variables."
for e in "${envs[@]}"; do
  file_env "$e"
done

echo "done!"

# make sure the correct directories exists (suggested by @chrif):
echo "Making directories..."
mkdir -p $FIREFLY_PATH/storage/app/public
mkdir -p $FIREFLY_PATH/storage/build
mkdir -p $FIREFLY_PATH/storage/database
mkdir -p $FIREFLY_PATH/storage/debugbar
mkdir -p $FIREFLY_PATH/storage/export
mkdir -p $FIREFLY_PATH/storage/framework/cache/data
mkdir -p $FIREFLY_PATH/storage/framework/sessions
mkdir -p $FIREFLY_PATH/storage/framework/testing
mkdir -p $FIREFLY_PATH/storage/framework/views/twig
mkdir -p $FIREFLY_PATH/storage/framework/views/v1
mkdir -p $FIREFLY_PATH/storage/framework/views/v2
mkdir -p $FIREFLY_PATH/storage/logs
mkdir -p $FIREFLY_PATH/storage/upload

if [[ $DKR_CHECK_SQLITE != "false" ]]; then
  echo "Touch DB file (if SQLite)..."
  if [[ $DB_CONNECTION == "sqlite" ]]; then
    touch $FIREFLY_PATH/storage/database/database.sqlite
    echo "Touched!"
  fi
fi

# make sure we own the volumes:
echo "Run chown on ${FIREFLY_PATH}/storage..."
chown -R www-data:www-data -R $FIREFLY_PATH/storage
echo "Run chmod on ${FIREFLY_PATH}/storage..."
chmod -R 775 $FIREFLY_PATH/storage

# remove any lingering files that may break upgrades:
echo "Remove log file..."
rm -f $FIREFLY_PATH/storage/logs/laravel.log

echo "Dump auto load..."
composer dump-autoload
echo "Discover packages..."
sudo -u www-data php artisan package:discover

echo "Wait for the database."
if [[ -z "$DB_PORT" ]]; then
  if [[ $DB_CONNECTION == "pgsql" ]]; then
    DB_PORT=5432
  elif [[ $DB_CONNECTION == "mysql" ]]; then
    DB_PORT=3306
  fi
fi
if [[ -n "$DB_PORT" ]]; then
  /wait-for-it.sh "${DB_HOST}:${DB_PORT}" -t 60 -- echo "DB is up. Time to execute artisan commands."
fi

echo "Run various artisan commands..."

sudo -u www-data php artisan cache:clear

if [[ $DKR_RUN_MIGRATION == "false" ]]; then
  echo "Will NOT run migration commands."
else
  echo "Running migration commands..."
  sudo -u www-data php artisan firefly-iii:create-database
  sudo -u www-data php artisan migrate --seed --no-interaction --force
  sudo -u www-data php artisan firefly-iii:decrypt-all
fi

# there are 13 upgrade commands
if [[ $DKR_RUN_UPGRADE == "false" ]]; then
  echo 'Will NOT run upgrade commands.'
else
  echo 'Running upgrade commands...'
  sudo -u www-data php artisan firefly-iii:transaction-identifiers
  sudo -u www-data php artisan firefly-iii:migrate-to-groups
  sudo -u www-data php artisan firefly-iii:account-currencies
  sudo -u www-data php artisan firefly-iii:transfer-currencies
  sudo -u www-data php artisan firefly-iii:other-currencies
  sudo -u www-data php artisan firefly-iii:migrate-notes
  sudo -u www-data php artisan firefly-iii:migrate-attachments
  sudo -u www-data php artisan firefly-iii:bills-to-rules
  sudo -u www-data php artisan firefly-iii:bl-currency
  sudo -u www-data php artisan firefly-iii:cc-liabilities
  sudo -u www-data php artisan firefly-iii:back-to-journals
  sudo -u www-data php artisan firefly-iii:rename-account-meta
  sudo -u www-data php artisan firefly-iii:migrate-recurrence-meta
fi

# there are 15 verify commands
if [[ $DKR_RUN_VERIFY == "false" ]]; then
  echo 'Will NOT run verification commands.'
else
  echo 'Running verification commands...'
  sudo -u www-data php artisan firefly-iii:fix-piggies
  sudo -u www-data php artisan firefly-iii:create-link-types
  sudo -u www-data php artisan firefly-iii:create-access-tokens
  sudo -u www-data php artisan firefly-iii:remove-bills
  sudo -u www-data php artisan firefly-iii:enable-currencies
  sudo -u www-data php artisan firefly-iii:fix-transfer-budgets
  sudo -u www-data php artisan firefly-iii:fix-uneven-amount
  sudo -u www-data php artisan firefly-iii:delete-zero-amount
  sudo -u www-data php artisan firefly-iii:delete-orphaned-transactions
  sudo -u www-data php artisan firefly-iii:delete-empty-journals
  sudo -u www-data php artisan firefly-iii:delete-empty-groups
  sudo -u www-data php artisan firefly-iii:fix-account-types
  sudo -u www-data php artisan firefly-iii:rename-meta-fields
  sudo -u www-data php artisan firefly-iii:fix-ob-currencies
  sudo -u www-data php artisan firefly-iii:fix-long-descriptions
  sudo -u www-data php artisan firefly-iii:fix-recurring-transactions
fi

# report commands
if [[ $DKR_RUN_REPORT == "false" ]]; then
  echo 'Will NOT run report commands.'
else
  echo 'Running report commands...'
  sudo -u www-data php artisan firefly-iii:report-empty-objects
  sudo -u www-data php artisan firefly-iii:report-sum
fi


php artisan firefly-iii:restore-oauth-keys

if [[ $DKR_RUN_PASSPORT_INSTALL == "false" ]]; then
  echo 'Will NOT generate new OAuth keys.'
else
  echo 'Generating new OAuth keys...'
  sudo -u www-data php artisan passport:install
fi

sudo -u www-data php artisan firefly-iii:set-latest-version --james-is-cool
sudo -u www-data php artisan cache:clear
sudo -u www-data php artisan config:cache

# make sure we own everything (again)
echo "Run chown on ${FIREFLY_PATH}/storage"
chown -R www-data:www-data -R $FIREFLY_PATH/storage

sudo -u www-data php artisan firefly:instructions install

echo "Go!"
exec apache2-foreground
