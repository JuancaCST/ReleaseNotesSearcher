# Getting Started
This program searches for known bugs from the FortiSIEM releases notes using keywords. It will build a cache, if not present, when running for the first time which allows all subsequent searches to be faster and offline.

## Requirements
Python 3.6 and higher.

## Installation
Click on the green "Code" button under this repository to Download ZIP. 
* The cache.txt is not required but allows for fast offline searches from the start. 

## Usage
![image](https://user-images.githubusercontent.com/65786940/169099579-1168737c-72fc-43fa-b4a7-4f9743f772d7.png)

# Roadmap
Future FortiSIEM versions will be supported. Versions 6.1.0 up to 6.5.0 are currently supported.

# Known Issues
If the cache is not present, it has to scrape the data from the release notes for each version included in the current search. Depending on the availability and responsiveness of the docs.fortinet.com domain, this can cause:
* The program to have a significant slowdown in displaying the results for each version (only affects first time running without cache)
* The program to error out due to incomplete Bytes transferred. Expected x bytes / only received x bytes. This is a rare issue and is due to a packet loss. Re-running the script should fix this.
* The program can error out due to a server side HTTP error (example: 503 Service Unavailable).
