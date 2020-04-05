#Preprocessing
## The 2nd Part: Preprocess the Data from the fetched html
### 1. Some Rules We Discussed Before

> We seperated each entry in our dataset into categories of id, title, summary, director, and other types of information. 

`id | Title | Summary | Casts | Directors | Writers | Rating`

> Stored them as `Movie_information.csv`.

### 2. Problems that We Met

> We found that there are some records given by the API which could not satisfy our requirement, so we removed them from our dataset.

>> Especially, we got rid of the record with the length of summary equals to 0.
