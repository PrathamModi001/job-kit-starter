const fs = require('fs');
const b64 = fs.readFileSync('scratch/dpdzero_b64.txt', 'utf8').trim();

// We will test in browser_evaluate with this b64 string
