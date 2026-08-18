

-- Create CSV file format
CREATE OR REPLACE FILE FORMAT IPRA_DB.RAW.IPRA_CSV_FORMAT
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    TRIM_SPACE = TRUE
    NULL_IF = ('NULL', '');

-- Create internal stage for loading data
CREATE OR REPLACE STAGE IPRA_DB.RAW.IPRA_STAGE
    FILE_FORMAT = IPRA_DB.RAW.IPRA_CSV_FORMAT
    COMMENT = 'Internal stage for loading clean CSV data';

-- Verify stage exists
LIST @IPRA_DB.RAW.IPRA_STAGE;