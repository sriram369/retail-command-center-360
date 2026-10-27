# Optional AI analysis

Run `python scripts/ai_summary.py` without credentials to create a clearly labeled deterministic demonstration.
The core project never needs an API key. The prompt in the script requests qualitative observations and references to validated metric keys.
Numbers are rendered from those references rather than trusting generated figures. Unknown keys or digits in narrative are rejected.
This guard prevents unsourced numeric claims, but it does not prove qualitative causality or recommendation quality; review both.

To use Claude voluntarily, set ANTHROPIC_API_KEY and ANTHROPIC_MODEL in the local environment, then run the same script.
Only validated aggregate scalar metrics are submitted. No raw customer records or credentials are embedded in source.
The live API path is optional and has not been tested without account credentials. Check current model availability and pricing before running it.
