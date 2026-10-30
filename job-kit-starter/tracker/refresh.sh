#!/bin/bash
set -e
cd "$(dirname "$0")"

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

python3 make_data.py || python make_data.py
npm run build --silent
npx wrangler pages deploy dist --project-name=my-job-tracker --commit-dirty=true
