This file documents the columns present in the `prefeituras.csv` dataset.

Columns
- **id:** Unique numeric identifier for the row. Use this to reference a specific prefeitura programmatically.
- **prefeitura:** Full official name of the prefeitura (municipal government office).
- **municipio:** City name (plain text, often lowercase and without diacritics normalized for lookups).
- **url:** Base URL of the transparency portal API or site for that prefeitura. May include a trailing `/api/` or point to a portal homepage.
- **empresa:** Vendor or company responsible for maintaining the transparency portal (e.g., `portaltp`, `Agape`, `tectrilha`).
- **unidadegestora:** Optional numeric identifier used by the portal to identify the municipal management unit when querying financial or transactional endpoints. May be empty when not required or unknown.

Notes
- Encoding: the CSV contains non-ASCII characters (accents). Read it with UTF-8 encoding to preserve characters like `ã`, `ç`, `ó`.
- URLs: some entries may be HTTP (not HTTPS) or include ports. Validate and normalize before automated requests.
- Missing values: fields such as `unidadegestora` can be empty — handle these cases in scripts.

Examples
- Lookup by `municipio` (normalized): search `municipio` = `vila velha` to find the corresponding `url` and `empresa`.
- Querying APIs: when `unidadegestora` is present, some API endpoints accept it as a query parameter to filter results for that prefeitura.

Suggested usage
- Load the file into a DataFrame (pandas) with `encoding='utf-8'`.
- Normalize `municipio` (strip accents, lower-case) for robust joins and lookups.

File path
- See [portal_lists/prefeituras.csv](portal_lists/prefeituras.csv) for the full dataset.