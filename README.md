# Facebook Messenger Data Grapher

****Use 64 bit Python or it will not work!!!!!!   <----- Important read this!****

## Dependencies
* Python 3 ****64 bit****
* Pandas
* Matplotlib
* BeautifulSoup4

## How To
1. Install all the dependencies
2. Download/clone this repository
3. On Facebook, go to Settings then select "Download a copy of your Facebook data" (you can select either HTML or JSON formats)
4. Once you have that, find the `messages` folder inside the archive and copy that folder into your clone of this repository
    - This folder should keep the same name (`messages`) and be placed at the top level of the repo
5. Edit `userinfo.py` and add your information
6. If you selected HTML format in step 3, run `python html_parser.py`; otherwise, run `python json_parser.py` for the JSON format 
7. Run `python grapher.py`
8. Graphs will be generated and saved in the `graphs` folder

## Results
Here are a few examples of the type of graphs generated:

![graph one](https://s3.amazonaws.com/rohanp/cumulative3.png)
![graph two](https://s3.amazonaws.com/rohanp/number_messaged_by_day3.png)
![graph three](https://s3.amazonaws.com/rohanp/messaging_by_sex3.png)
![graph four](https://s3.amazonaws.com/rohanp/total_sent_received3.png)

## Want to contribute? Here's some features to consider
* Additional parameters: who messaged first, average reply time.
* More permutations of existing parameters (sent/received, sex, date, number of messages, and number of people)
