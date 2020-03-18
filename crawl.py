import requests
import re
from bs4 import BeautifulSoup
import datetime
# import datetime as pydatetime

class CoronaCrawlClass:
    def __init__(self, url='http://www.seongnam.go.kr/coronaIndex.html'):
    # def __init__(self, url='https://www.seongnam.go.kr/prgm/corona/coronaList2.do'):
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
        stat_title = self.soup.select('#corona_page > div.corona_page_top > div > div.contents_all > div.pc_view > table > thead')
        stat_value = self.soup.select('#corona_page > div.corona_page_top > div > div.contents_all > div.pc_view > table > tbody')
        stat_title_list = [v for v in stat_title[0].text.split('\n') if v and v != '확진환자']
        stat_value_list = [v for v in stat_value[0].text.split('\n') if v]

        for i in range(0, len(stat_value_list)):
            self.stat_dict[stat_title_list[(i+4)%8]] = stat_value_list[i]

        # print(self.stat_dict)

    def crawl_track(self):
        track_infos = self.soup.select('#board_group1 > table > tbody')
        str_track_infos = track_infos[0].text
        patient_track_infos = " ".join(str_track_infos.split())
        # print(patient_track_infos)

        # ((성남#\d+ \( (\d\d년생|(남|여)) \/ (\d\d년생|(남|여)) \/ \D+((\d{1,20}(동|단지))|) 거주(( \/ \D+)|) \) (|- 확인중 )확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일)|(성남#18 \( 남 \/ 55년생 \/ 분당구 이매동 거주 \/ 성남#4 접촉자 \) 확진일 3월 9일)|(서울#138 \( 87년생 \/ 남 \/ 중원구 은행동 거주 \/ 은혜의 강 교회 \) 확진일 3월 9일))
        # ((성남#\d+ \( (\d\d년생|(남|여)) \/ (\d\d년생|(남|여)) \/ \D+((\d{1,20}(동|단지))|) 거주(( \/ \D+)|) \) (|- 확인중 )확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일))
        # ((성남#\d+ \( \d\d년생 \/ (남|여) \/ \D+\) 확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일))
        p = re.compile(
            '((성남#\d+ \( (\d\d년생|(남|여)) \/ (\d\d년생|(남|여)) \/ \D+((\d{1,20}(동|단지))|) 거주(( \/ \D+)|) \) (|- 확인중 )확진일 \d+월 \d+일)|(타지역 확진자 \( \D+\d+번 \d+년생 \/ (남|여) \/ \D+거주 \) 확진일 \d+월 \d+일)|(성남#18 \( 남 \/ 55년생 \/ 분당구 이매동 거주 \/ 성남#4 접촉자 \) 확진일 3월 9일)|(서울#138 \( 87년생 \/ 남 \/ 중원구 은행동 거주 \/ 은혜의 강 교회 \) 확진일 3월 9일))')

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
        self.filter_by_week(1)

    def filter_by_week(self, weeks):
        p = re.compile('\d+월 \d+일')
        today = datetime.datetime.today()

        temp_dict = {}
        for patient, info in self.track_dict.items():
            confirm_date = p.findall(patient)
            confirm_date = datetime.datetime.strptime('2020년' + confirm_date[0], '%Y년%m월 %d일')
            delta = (today - confirm_date).days
            if delta <= weeks*7 :
                temp_dict[patient] = info

        self.track_dict.clear()
        self.track_dict = temp_dict


    def align_track_str(self):
        p1 = re.compile('((\d+월 \d+일~\d+월 \d+일)|(\d+월 \d+일~\d+일)|(\d+월 \d+일))')
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
        # seongnam_track_dict = {}
        # 제생병원
        hospital1_dict = {}
        # 은혜의 강 교회
        church1_dict = {}
        around_track_dict = {}

        for patient, track_info in self.track_dict.items():
            if "은혜의 강" in patient:
                church1_dict[patient] = track_info
            elif "제생병원" in patient:
                hospital1_dict[patient] = track_info
            else:
                around_track_dict[patient] = track_info

        fw = open('data/sn_stats.txt', 'w')
        for key, value in self.stat_dict.items():
            fw.write(key + ' : ' +  value + '\n')
        fw.close()

        fw = open('data/all_patients.txt', 'w')
        for patient, track_info in self.track_dict.items():
            fw.write(patient + '\n')
            fw.write(track_info + '\n')
        fw.close()

        fw = open('data/hp1_patients.txt', 'w')
        for hp_patient, track_info in hospital1_dict.items():
            fw.write(hp_patient+'\n')
            fw.write(track_info+'\n')
        fw.close()

        fw = open('data/ch1_patients.txt', 'w')
        for ch_patient, track_info in church1_dict.items():
            fw.write(ch_patient + '\n')
            fw.write(track_info + '\n')
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