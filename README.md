# Team Ripple's amazing edgar project
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project downloads 10-K filings from the SEC website, counts sentiment words and performs some initial analysis.
	
## Technologies
Project is purely created in Python. Its uses libraries such as:
* requests
* beautiful soup
* pandas
* matplotlib
	
## Setup
To run this project:

```
$ git clone https://gitlab.com/kubrick-group/training/teaching/assessments/de20/edgar-ripple/EdgarRipple.git
$ cd EdgarRipple
$ pip install -r requirements.txt
$ python Edgar/edgar_full.py
```
