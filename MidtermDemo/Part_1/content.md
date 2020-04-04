# The first part
## Build Our Own Dataset
### 1. we downloaded all links that we need for our project

[Douban Link](https://movie.douban.com/)

> Here is the regular expression of our preprocessing procedure:

`res = re.search(r'href="https://movie.douban.com/subject/(\d+)/"', token)`


> Here is one example of links from the html results:

`<div data-v-3e982be2="" class="list-wp"><a data-v-2c455d87="" data-v-3e982be2="" target="_blank" href="https://movie.douban.com/subject/1291543/" class="item">`


> We could use regular expression to fetch the links that we need for the next step:

https://movie.douban.com/subject/1291543/

### 2. we used these links to fetch further

> We used the following API which was developped by others to fetch the information for the given subject id.

`https://douban.uieee.com/v2/movie/subject/id`

> Then we uploaded all the data and built our own dataset.
