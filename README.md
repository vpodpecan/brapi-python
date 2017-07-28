

OPEN QUESTIONS

incompleteness and errors in current DB schema

inconsistencies between BRAPI API description and current schema
e.g. germplasm -> typeOfGermplasmStorageCode is text, API wants array of strings


TODO:



FIXED
what to do with tables from the schema which do not have primary key declared?
  Django adds 'id' primary key but which is required on import but not present in the data!
  fixed by declaring combinations of other keys in django-import-export
add function def __str__(self) to all models that require nice display name
add verbose_name_plural inside meta class to all models that require fix in plural name
