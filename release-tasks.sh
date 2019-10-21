# Heroku Release Phase Script
# https://devcenter.heroku.com/articles/release-phase
# https://devcenter.heroku.com/articles/pipelines#can-i-run-scripts-such-as-rake-db-migrate-when-promoting

# Run migration
python server/manage.py migrate --no-input

# clear cache
python server/manage.py clear_cache

# Run production checks
python server/manage.py check --deploy

# Index data into elastic
python server/manage.py update_index
