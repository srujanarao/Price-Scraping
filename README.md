# README.md


:rocket: Installation Steps
---
1. Save the input sku files in ```UTF-8 enabled``` csv format. Skipping this step will lead to errors during script execution. 
<br> ```File -> Save As -> CSV UTF-8(.csv)```</br>

<p align="center"><img width="450" src="./assets/utf8_csv.png"></p>

2. Clone the Github repository to a desired location on your computer. You will need [git](https://git-scm.com/) to be preinstalled on your machine. Once the repository is cloned, you will then ```cd``` into the local repository.
```
git clone https://github.com/srujanarao/Price-Scraping.git
cd price_scrape
```
3. This project uses Python 3, so make sure that [Python](https://www.python.org/downloads/) and [Pip](https://pip.pypa.io/en/stable/installation/) are preinstalled. All requirements of the project are listed in the ```requirements.txt``` file. Use pip to install all of those.
```
pip3 install -r requirements.txt
```
4. Once all the requirements are installed, you will have to ```cd``` into the ```src``` folder. Once in the ```src``` folder, use the python command to run the ```.py``` files.
```
cd src

For Mac
python3 sku_US.py 

For Windows
python sku_US.py
```

:page_facing_up: Sample Output
---
 1. results_US.csv

 <p align="center"><img width="800" src="https://github.com/srujanarao/Price-Scraping/blob/main/assets/Results_US.png?raw=true"></p>
 
 2. results_CA.csv
 
 <p align="center"><img width="800" src="https://github.com/srujanarao/Price-Scraping/blob/main/assets/Results_CA.png?raw=true"></p>

 3. results_CA_9PXM.csv
 4. results_IT.csv

<p align="center"><img width="300" src="https://github.com/srujanarao/Price-Scraping/blob/main/assets/Results_IT.png?raw=true"></p>

:golf: Next Steps
---
1. Fix scraping issues in ```sku_CA_9PXM.py``` due to dynamic urls and unstable search results
2. Reduce run time of the scripts

:thought_balloon: Future Scope
---
1.
2.
3.

:sparkles: Contributors
---
- Rakesh Ravi
- [Srujana Marne Shiva Rao](https://github.com/srujanarao)
- Landon Smith

:email: Support
---

For any queries and help, please reach out to us at: rravi@ncsu.edu, smarnes@ncsu.edu, gsmith9@ncsu.edu

