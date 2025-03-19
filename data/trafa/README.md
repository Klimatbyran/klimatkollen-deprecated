# Trafa Data Fetching and Processing

### Files
- index.ts: This is the main script that fetches data from the TRAFA API, processes it, and writes it to files.
- client.ts: This file contains the TrafaClient class, which is used to build queries for the api.
- types.ts: typescript types for trafa api. 


### What the Script Does
The script fetches data from the TRAFA API based on the options you choose when running it. It can fetch data for the current year, a specific year, or all years from 2015 to the present.

The fetched data is then processed and written to JSON files in the data/trafa/downloads directory. Metadata about the fetch operation, including the date and time of the fetch and the Git user who performed it, is also written to a metadata.yml file in the same directory.

After the data is written to files, a Python script is run to further process the data into Excel file trafa-output.xlsx. 

### How to run 

```bash
    npm run trafa:process
```