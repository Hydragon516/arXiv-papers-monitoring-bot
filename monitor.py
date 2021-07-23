from bs4 import BeautifulSoup
import requests
import datetime as dt
import time
from slack import *

buffer = []
t = dt.datetime.now()

while True:
    target_list = open('target.txt', 'r').read().split('\n')
    target_list = [ix.lower() for ix in target_list]

    time.sleep(60)
    delta = dt.datetime.now() - t
    if delta.seconds >= 3600:
        try:
            html = requests.get('https://arxiv.org/list/cs.CV/pastweek?skip=0&show=1000')
            soup = BeautifulSoup(html.text, 'html.parser')

            title = []
            pdf = []

            content = soup.find_all('div', {'class':'meta'})
            link = soup.find_all('span', {'class':'list-identifier'})

            for i in range(len(content)):
                content_line = str(content[i]).split("\n")
                for ele in content_line:
                    if "Title:</span>" in ele:
                        title.append(ele.split("Title:</span> ")[1])

                link_line = str(link[i]).split("\n")
                for ele in link_line:
                    if "Download PDF" in ele:
                        pdf.append("https://arxiv.org/abs/" + (ele.split('[<a href="/pdf/')[1]).split('"')[0])

            new_buffer = []
            print_buffer = []

            for x in range(len(title)):
                for target in target_list:
                    if target in title[x].lower():
                        new = (title[x], pdf[x])
                        new_buffer.append(new)

                        if new not in buffer:
                            print_buffer.append(new)
                        break

            buffer = new_buffer

            if len(print_buffer) > 0:
                send_mdg_to_slack("Update new arXiv papers!")
                for i in range(len(print_buffer)):
                    send_mdg_to_slack(print_buffer[i][0] + " --- " + print_buffer[i][1])
        
        except:
            print("Connection ERROR!")
            pass
