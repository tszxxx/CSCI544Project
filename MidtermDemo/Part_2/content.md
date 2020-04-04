#Preprocessing
## In This Part, We Tried to Preprocess the Data from the First Part
### 1. Some Rules We Discussed Before

> We tried to split data in out dataset by its id, title, summary, director, and other types of information to get a csv file to store them.

`id | Title | Summary | Casts | Directors | Writers | Rating`

> We seperated all data by the above categories and stored them in a csv file.

`Movie_information.csv`

### 2. Problems that We Met

> We found that there are some records given by the API which could not satisfy our requirement, so we removed them from our dataset and then collected the others into different directories.

>> Especially, we got rid of the record with the length of summary equals to 0.
