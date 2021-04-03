# the crawler of the gaming website 巴哈姆特

## Introduction
This is a simple web crawler which gets the popularity(including the number of views and thread), and all the data can be stored in json/ mongodb

## Changes
2028-8 version 1.0: web crawling based on html  
2021-4 version 2.0: get by data by http request

## How to use
running the following code everyday after 12pm
```sh
python main.py
```

## todo
- [x] add functions to store data in both json and mongodb
- [ ] allow user to check certain game data through command line
- [ ] add simple web frontend, probably using chart.js and react.js
- [ ] add prediction, e.g., see low long the time a certain game is 'popular', how each game affected each other