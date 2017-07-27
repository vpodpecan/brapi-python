

TODO:
what to do with tables from the schema which do not have primary key declared?
Django adds 'id' primary key but which is required on import but not present in the data!


FIXED
add function def __str__(self) to all models that require nice display name
add verbose_name_plural inside meta class to all models that require fix in plural name
