# About

Data available with use of [Google Ngram Viewer](https://books.google
.com/ngrams)  is optimized for quick **on-line** inquiries into the usage of 
 small sets of phrases. But what if you want to get the data analyzed  
 **locally**? 

This script retrieves data from Google Ngram Viewer and allow for local data 
analysis.
 
### Dependencies

* Python 3
* requests
* pandas
* matplotlib

# Running

The usage of the `google_ngram.py` script accept the following parameters.
* **list_of_words** comma separated list of words to be searched
* **corpus** (default: eng_2012) - The corporas that are available at Google 
 Ngram Viewer are [here](https://books.google.com/ngrams/info) (scroll to  
 Corpora section). It only support `eng` corpora.
* **startYear** (default: 1900) in range `[1800..2008]`
* **endYear** (default: 2008) in range `[1800..2008]`
* **smoothing** (default: 3) Smoothing parameter (integer) in range `[0..50]`
* **noprint** do not display results to console
* **caseInsensitive** (default: False)return case-insensitive results

*Note:* flags require single dash `-`, while parameters require double dash `--`

```
python3 google_ngram.py television,computer,internet,ai
--corpus=eng_2012 
--startYear=1900  
--endYear=2008
-noprint
```
The results are going to be stored in a CSV file generated with name adequate
 to used runtime options. The file is going to be stored in directory where 
 the script is to be placed.
 
###Explaining Code

```
import sys           # for script paramethers and file handling
import requests      # for geting the data with url request
import re            # parsing the data out of http response of a `request`
from ast import literal_eval # evaluateexpression node or string containing a Python literal or container display to dict
from pandas import DataFrame # pandas 2D dataframe 
import subprocess            #

```
The data is retrieved using the 
[requests](http://docs.python-requests.org/en/master/) package. As the 
response is a pure HTML it is searched with `re` package to get the clean and
raw data:
 
`res = re.findall('var data = (.*?);\\n', req.text)`

### Criticism on Google Ngrams

A paper published in [PLoS ONE](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0137041) outlines some of the major problems with 
the  corpus of scanned books that powers Google Ngram. 
>“It’s so beguiling, so powerful,”

says Peter Sheridan Dodds, an applied mathematician at the University of 
Vermont who co-authored the paper. 
>“But I think there’s a misrepresentation of what people should expect from 
this corpus right now.” 

**Credits:** Source code inspired by 
[this](https://github.com/econpy/google-ngrams/) very nice script 