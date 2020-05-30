# Text Metaguesser

## Config
This tool is entirely configured with environment variables (as opposed to pdf-to-text, which supports CLI arguments). 
The reason for that is that the `pdf-to-text` tool provides file-based output, so there might be an interest to run it from CLI for different reasons than the `doc-metaguesser`. 
This tool parses the results and writes them to the metadatabase.

### Environment variables

#### General
| **Variable** | **Description** | **Default** |
|---|---|---|
| `TXT_METAGUESSER__INPUT_DIR` | Input directory containing the text files | `/input` |
| `TXT_METAGUESSER__PLUGINS` | Comma-separated list of modules to load from the `plugins/` folder | `meta_date` |
| `TXT_METAGUESSER__SQL_ALCHEMY__URI` | SQL Alchemy URI to define the database connection. Has precedence over the separated variables below | |
| `TXT_METAGUESSER__SQL_ALCHEMY__USER` | User to the metadb | `root` |
| `TXT_METAGUESSER__SQL_ALCHEMY__PASSWORD` | Password for the user | |
| `TXT_METAGUESSER__SQL_ALCHEMY__HOST` | Hostname or IP of the metadb | `localhost` |
| `TXT_METAGUESSER__SQL_ALCHEMY__PORT` | Port of the metadb | `3307` |
| `TXT_METAGUESSER__SQL_ALCHEMY__DATABASE` | Database name  of the metadb | `documents` |
| `TXT_METAGUESSER__SQL_ALCHEMY__LIBRARY` | Which SQL Alchemy connection library to use | `mysql+pymysql` |

There are currently no other databases than MySQL supported.

#### Plugins
| **Variable** | **Plugin** | **Description** | **Default** |
|---|---|---|---|
| `TXT_METAGUESSER__META_DATE__PATTERNS` | `meta_date` | Comma-separated list of which patterns to load in which order. | `GERMAN_LONG,GERMAN_SHORT` |
