#!/bin/bash

# program
BASEURL="http://127.0.0.1:8000"

# list all programs
curl -G "$BASEURL"/brapi/v1/programs \
    | python3 -m json.tool > programs.json

# GET programs
curl -G "$BASEURL"/brapi/v1/programs \
    --data-urlencode "programName=Program 5" \
    --data-urlencode "abbreviation=P5" \
    | python3 -m json.tool > programs1.json

# GET germplasm details by id
curl "$BASEURL"/brapi/v1/germplasm/1 | python3 -m json.tool > germplasm1.json

# GET germplasm search
curl -G "$BASEURL"/brapi/v1/germplasm-search \
    --data-urlencode "germplasmName=Name001" \
    --data-urlencode "germplasmDbId=1" \
    | python3 -m json.tool > germplasm2.json

# POST germplasm search
curl -H "Content-Type: application/json" -X POST "$BASEURL"/brapi/v1/germplasm-search \
    -d '{"germplasmPUIs" : [ "http://pui.per/accession/A000001", "http://pui.per/accession/A000009" ],
        "germplasmDbIds" : [1,2,3,4,5,6,9],
        "germplasmSpecies": ["novus"]}' \
    | python3 -m json.tool > germplasm-search3.json

# GET trial by id
curl "$BASEURL"/brapi/v1/trials/102 | python3 -m json.tool > trials1.json

# GET list trial summaries
curl -G "$BASEURL"/brapi/v1/trials \
    --data-urlencode "programDbId=1" \
    --data-urlencode "sortBy=trialName" \
    --data-urlencode "sortOrder=desc" \
    | python3 -m json.tool > trials2.json

# GET study details
curl "$BASEURL"/brapi/v1/studies/1002 | python3 -m json.tool > studies1.json

# GET list study summaries
curl -G "$BASEURL"/brapi/v1/studies-search \
--data-urlencode "studyType=Yield study" \
--data-urlencode "locationDbId=1" \
--data-urlencode "germplasmDbIds=['1', '2']" \
--data-urlencode "observationVariableDbIds=['MO_123:100002','MO_123:100004']" \
--data-urlencode "active=false" \
--data-urlencode "sortOrder=desc" \
--data-urlencode "sortBy=startDate" \
| python3 -m json.tool > studies2.json


# POST study search
curl -H "Content-Type: application/json" -X POST "$BASEURL"/brapi/v1/studies-search \
    -d '{"studyType" : "Yield study",
	 "studyNames" : ["Study 1", "Study 2", "Study 3"],
     "studyLocations" : ["Location 1", "Location 1"],
     "programNames": ["Program 1", "Program 2"],
     "germplasmDbIds" : ["1","2"],
     "observationVariableDbIds" : ["MO_123:100002","MO_123:100004"],
     "active" : "false",
     "sortBy" : "startDate",
     "sortOrder": "desc"
  	}' \
    | python3 -m json.tool > studies3.json

# GET Study Observation Variables
curl "$BASEURL"/brapi/v1/studies/1002/observationVariables \
    | python3 -m json.tool > observationVariable1.json


# GET Study Germplasms
curl "$BASEURL"/brapi/v1/studies/1002/germplasm \
    | python3 -m json.tool > observationVariable3.json


# GET List Locations
curl -G "$BASEURL"/brapi/v1/locations \
    --data-urlencode "locationType=Farmer field location" \
    | python3 -m json.tool > locations1.json


# GET Location details
curl "$BASEURL"/brapi/v1/locations/10 \
    | python3 -m json.tool > locations2.json


# GET Call search
curl "$BASEURL"/brapi/v1/calls?datatype=json \
    | python3 -m json.tool > calls1.json
