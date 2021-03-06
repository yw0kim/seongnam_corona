import crawl
import serve_api
import sys
import platform
from http.server import HTTPServer

def main():
    crawlClass = crawl.CoronaCrawlClass()
    crawlClass.crawl_stats()
    crawlClass.crawl_track()
    crawlClass.align_track_str()
    crawlClass.manage_files()

    #Handler = serve_api.MyHandler(crawlClass.stat_dict,
    #                                  crawlClass.seongnam_track_list,
    #                                  crawlClass.around_track_list)
    if platform.system() == 'Windows':
        ip_str = 'localhost'
    else:
        ip_str = '0.0.0.0'

    httpd = HTTPServer((ip_str, 19158), serve_api.MyHandler)

    buffer = 1
    sys.stderr = open('logfile.txt', 'w', buffer)
    httpd.serve_forever()

if __name__ == "__main__":
    main()
