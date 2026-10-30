$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

if (-not $env:CLOUDFLARE_API_TOKEN) {
    $env:CLOUDFLARE_API_TOKEN = [Environment]::GetEnvironmentVariable("CLOUDFLARE_API_TOKEN", "User")
}

python make_data.py
npm run build --silent
npx wrangler pages deploy dist --project-name=my-job-tracker --commit-dirty=true
