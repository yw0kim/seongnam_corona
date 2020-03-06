import requests
import re
from bs4 import BeautifulSoup

class CoronaCrawlClass:
    def __init__(self, url='http://www.seongnam.go.kr/coronaIndex.html'):
        self.crawl_url = url
        self.response = requests.get(self.crawl_url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.stat_dict = {}

        # list of dict
        self.track_list = []
        self.seongnam_track_list = []
        self.around_track_list = []

    def crawl_stats(self):
        # print(html)
        # table = soup.find_all("table")
        corona_value = self.soup.select('#corona_page > div.corona_page_top > div > div.contents_all > ul')
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

        s_p = re.compile('성남#\d+ \( \d\d년생 \/ (남|여) \/ (분당구|중원구|수정구) ..동 거주 \) 확진일 \d+월 \d+일')
        e_p = re.compile('타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일')
        p = re.compile('((성남#\d+ \( \d\d년생 \/ (남|여) \/ (분당구|중원구|수정구) ..동 거주 \) 확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일))')

        before_contents_start = 0
        before_contents_end = 0
        before_patient_id = ""

        for i, patient in enumerate(p.finditer(patient_track_infos)):
            before_contents_end = patient.start()-1
            if i != 0 :
                self.track_list[i - 1][before_patient_id] = patient_track_infos[before_contents_start:before_contents_end]

            patient_id = patient_track_infos[patient.start():patient.end()]
            self.track_list.append({patient_id: ""})
            before_patient_id = patient_id

            before_contents_start = patient.end() + 7

        self.track_list[-1][before_patient_id] = patient_track_infos[before_contents_start:]

#        for patient_info in self.track_list:
#            print(patient_info)
'''            
            if "성남" in patient_id:
                self.seongnam_track_dict[i] = ""
            else :
                self.around_track_dict[patient_id] = ""
'''


'''
((성남#\d+ \( \d\d년생 \/ (남|여) \/ (분당구|중원구|수정구) ..동 거주 \) 확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일))
'''
