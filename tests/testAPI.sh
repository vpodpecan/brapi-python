#!/bin/bash

# program
BASEURL="http://127.0.0.1:8000"


curl -G "$BASEURL"/brapi/v1/programs \
    | python3 -m json.tool > programs.json


curl -G "$BASEURL"/brapi/v1/programs \
    --data-urlencode "programName=Program 5" \
    --data-urlencode "abbreviation=P5" \
    | python3 -m json.tool > programs1.json


curl "$BASEURL"/brapi/v1/germplasm/1 | python3 -m json.tool > germplasm1.json

curl -G "$BASEURL"/brapi/v1/germplasm-search \
    --data-urlencode "germplasmName=Name001" \
    --data-urlencode "germplasmDbId=1" \
    | python3 -m json.tool > germplasm2.json

curl -H "Content-Type: application/json" -X POST "$BASEURL"/brapi/v1/germplasm-search \
    -d '{"germplasmPUIs" : [ "http://pui.per/accession/A000001", "http://pui.per/accession/A000009" ],
        "germplasmDbIds" : [1,2,3,4,5,6,9],
        "germplasmSpecies": ["novus"]}' \
    | python3 -m json.tool > germplasm-search3.json


curl "$BASEURL"/brapi/v1/trials/102 | python3 -m json.tool > trials1.json


curl -G "$BASEURL"/brapi/v1/trials \
    --data-urlencode "programDbId=1" \
    --data-urlencode "sortBy=trialName" \
    --data-urlencode "sortOrder=desc" \
    | python3 -m json.tool > trials2.json


curl "$BASEURL"/brapi/v1/studies/1002 | python3 -m json.tool > studies1.json


curl -H "Content-Type: application/json" -X POST "$BASEURL"/brapi/v1/studies-search \
    -d '{"studyType" : "Yield study",
	 "studyNames" : ["Study 1", "Study 2", "Study 3"],
     "studyLocations" : ["Location X", "Location Y"]
  	}' \
    | python3 -m json.tool > studies2.json
