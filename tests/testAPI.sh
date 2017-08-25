#!/bin/bash

# program
BASEURL="http://127.0.0.1:8000"


curl -G "$BASEURL"/brapi/v1/programs \
    > programs.json


curl -G "$BASEURL"/brapi/v1/programs \
    --data-urlencode "programName=Program 5" \
    --data-urlencode "abbreviation=P5" \
    > programs1.json


curl "$BASEURL"/brapi/v1/germplasm/1 > germplasm1.json

curl -G "$BASEURL"/brapi/v1/germplasm-search \
    --data-urlencode "germplasmName=Name001" \
    --data-urlencode "germplasmDbId=1" \
    > germplasm2.json

curl -H "Content-Type: application/json" -X POST "$BASEURL"/brapi/v1/germplasm-search \
    -d '{"germplasmPUIs" : [ "http://pui.per/accession/A000001", "http://pui.per/accession/A000009" ],
        "germplasmDbIds" : [1,2,3,4,5,6,9],
        "germplasmSpecies": ["novus"]}' \
    > germplasm-search3.json


curl "$BASEURL"/brapi/v1/trials/102 > trials1.json
