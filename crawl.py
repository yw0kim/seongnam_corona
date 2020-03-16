import requests
import re
from bs4 import BeautifulSoup
# import datetime as pydatetime

class CoronaCrawlClass:
    # def __init__(self, url='http://www.seongnam.go.kr/coronaIndex.html'):
    def __init__(self, url='https://www.seongnam.go.kr/prgm/corona/coronaList2.do'):
        self.crawl_url = url
        self.response = requests.get(self.crawl_url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.stat_dict = {}

        # list of dict
        self.track_dict = {}

    def crawl_stats(self):
        # print(html)
        # table = soup.find_all("table")
        # corona_value = self.soup.select('#corona_page > div.corona_page_top > div > div.contents_all > ul')
        # corona_value = self.soup.select('#corona_page > div.corona_page_top > div > div.contents_all > div.pc_view > table')
        corona_value = self.soup.select('#board_group2 > table > tbody > tr.plus_view.open > td > div > table > tbody')
        print(corona_value)
        str_corona_value = corona_value[0].text + '\n'

        p = re.compile('\d+.\n')
        before_end = 1
        for line in p.finditer(str_corona_value):
            self.stat_dict[str_corona_value[before_end:line.start()]] = str_corona_value[line.start():line.end() - 1]
            before_end = line.end()

    #        print(self.stat_dict)

    def crawl_track(self):
        track_infos = self.soup.select('#board_group1 > table > tbody')
        str_track_infos = track_infos[0].text
        patient_track_infos = " ".join(str_track_infos.split())
        # print(patient_track_infos)

        p = re.compile(
            '((성남#\d+ \( \d\d년생 \/ (남|여) \/ \D+ \) 확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일))')

        before_contents_start = 0
        before_contents_end = 0
        before_patient_id = ""

        for i, patient in enumerate(p.finditer(patient_track_infos)):
            before_contents_end = patient.start() - 1
            if i != 0:
                self.track_dict[before_patient_id] = patient_track_infos[before_contents_start:before_contents_end]
            patient_id = patient_track_infos[patient.start():patient.end()]
            self.track_dict[patient_id] = ""
            before_patient_id = patient_id
            before_contents_start = patient.end() + 7

        self.track_dict[before_patient_id] = patient_track_infos[before_contents_start:]

    def align_track_str(self):
        p1 = re.compile('((\d+월 \d+일~\d+월 \d+일)|(\d+월 \d+일))')
        p2 = re.compile('((\d+:\d+~\d+:\d+)|(\d+:\d+))')

        # align with p1 pattern
        for patient, track_info in self.track_dict.items():
            new_str = ""
            before_found_end = 0
            for i, found in enumerate(p1.finditer(track_info)):
                if i != 0:
                    new_str += (track_info[before_found_end:found.start() - 1] + '\n')
                new_str += (track_info[found.start():found.end()] + '\n')
                before_found_end = found.end()
            new_str += (track_info[before_found_end:] + '\n')
            self.track_dict[patient] = new_str

        # align with p2 pattern
        for patient, track_info in self.track_dict.items():
            new_str = ""
            before_found_end = 0
            for i, found in enumerate(p2.finditer(track_info)):
                if i == 0:
                    new_str += track_info[:found.start()-1]
                else:
                    new_str += (track_info[before_found_end:found.start()-1])
                if not '일' in track_info[found.start()-7:found.start()-1]:
                    new_str += '\n'
                new_str += (track_info[found.start():found.end()])
                before_found_end = found.end()
            new_str += (track_info[before_found_end:])
            self.track_dict[patient] = new_str

    def manage_files(self):
        seongnam_track_dict = {}
        around_track_dict = {}

        for patient, track_info in self.track_dict.items():
            if "성남" in patient:
                seongnam_track_dict[patient] = track_info
            else:
                around_track_dict[patient] = track_info

        fw = open('data/sn_patients.txt', 'w')
        for sn_patient, track_info in seongnam_track_dict.items():
            fw.write(sn_patient+'\n')
            fw.write(track_info+'\n')
        fw.close()

        fw = open('data/ar_patients.txt', 'w')
        for ar_patient, track_info in around_track_dict.items():
            fw.write(ar_patient + '\n')
            fw.write(track_info + '\n')
        fw.close()

'''
((성남#\d+ \( \d\d년생 \/ (남|여) \/ \D+ \) 확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일))
'''
'''
# backup last record
fr  = open('data/sn_patients.txt', 'r')
fw = open('data/sn_patients-'
          +pydatetime.datetime.now().replace(microsecond=0).isoformat()+'.txt'
          , 'w')
data = fr.read()
print(data)
fw.write(data)
fw.close()
fr.close()
'''