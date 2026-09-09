#!/bin/zsh
# Regenerate tracker data from applications.csv, rebuild, deploy to Cloudflare Pages.
# First time: run `npx wrangler login` (the CANDIDATE's Cloudflare account) and
# `npx wrangler pages project create my-job-tracker` — then this script just works.
set -e
cd "$(dirname "$0")"
python3 make_data.py
npm run build --silent
npx wrangler pages deploy dist --project-name=my-job-tracker --commit-dirty=true
