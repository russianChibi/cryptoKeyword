from config import *

#!/usr/bin/python3
# -*- coding: utf-8 -*-
import scrapetube
from binance import Client
from numpy import *
import argparse
from binance.enums import *
from youtube_transcript_api import YouTubeTranscriptApi

class youtubeKeyword:
    def __init__(self):
        self.connect()

        self.listAllBinanceToken = self.getAllPair()
        print(self.listAllBinanceToken)
        self.listAllBinanceTokenCount = []
        for i in range(0,len(self.listAllBinanceToken)):
            self.listAllBinanceTokenCount.append(0)
        self.listYTVideoID = []

    def connect(self):
        self.client = Client(api_key, api_secret)

    def getAllPair(self):
        exchange_info = self.client.get_exchange_info()
        tmpSymbols = ""
        blackList = open("blackList.txt", "r").read()
        for s in exchange_info['symbols']:
            tmp = s['symbol']
            # if "USD" in tmp[-3:] or "SDT" in tmp[-3:]:
            if tmp not in blackList and "USDT" in tmp[-4:] and "BUSDT" not in tmp and "BULLUSDT" not in tmp and "BEARUSDT" not in tmp and "UPUSDT" not in tmp and "DOWNUSDT" not in tmp and "USDS" not in tmp:
                if tmp[:-4] not in tmpSymbols:
                    tmpSymbols += tmp[:-4]+"--"
            elif tmp not in blackList and "BUSD" in tmp[-4:] and "BUSDT" not in tmp and "BULLBUSD" not in tmp and "BEARBUSD" not in tmp and "UPBUSD" not in tmp and "DOWNBUSD" not in tmp and "USDS" not in tmp:
                if tmp[:-4] not in tmpSymbols:
                    tmpSymbols += tmp[:-4]+"--"
        tmpSymbols = tmpSymbols[:-2]
        self.symbols = tmpSymbols.split("--")
        return self.symbols

    def checkInt(self,str):
        try:
            int(str)
            return True
        except ValueError:
            return False


    def checkLiveDay(self,videoData,liveDay):
        publishedTime = videoData['publishedTimeText']['simpleText'].lower()

        if "trước" not in publishedTime and  "giờ" not in publishedTime and "phút" not in publishedTime and "giây" not in publishedTime and "giờ" not in publishedTime and "ngày" and "tuần" not in publishedTime not in publishedTime and "tháng" not in publishedTime and "năm" not in publishedTime:
            self.hotExit(["Sai ngon ngu nhan dien",videoData,publishedTime])


        publishedTime = publishedTime.split(" ")

        if len(publishedTime) <1:
            self.hotExit(["Sai ngon ngu nhan dien",videoData,publishedTime])
        
        count =-1
        for i in range(0,len(publishedTime)):
            if self.checkInt(publishedTime[i]):
                count = i


        if count ==-1:
            self.hotExit(["Sai ngon ngu nhan dien",videoData,publishedTime])

        if "giờ" not in publishedTime[count+1] and "phút" not in publishedTime[count+1] and "giây" not in publishedTime[count+1] and "giờ" not in publishedTime[count+1] and "ngày" not in publishedTime[count+1] and "tuần" not in publishedTime[count+1] and "tháng" not in publishedTime[count+1] and "năm" not in publishedTime[count+1]:
            self.hotExit(["Sai ngon ngu nhan dien",videoData,publishedTime])


        if "giây" in publishedTime[count+1] or "giờ" in publishedTime[count+1]:
            return 1
        elif "ngày" in publishedTime[count+1]:
            if int(publishedTime[count]) < liveDay:
                return 1
            else:
                # print(publishedTime)
                return 0
        elif "tuần" in publishedTime[count+1]:
            if int(publishedTime[count])*7 < liveDay:
                return 1
            else:
                # print(publishedTime)
                return 0
        elif "tháng" in publishedTime[count+1]:
            if int(publishedTime[count])*30 < liveDay:
                return 1
            else:
                # print(publishedTime)
                return 0
        # print(publishedTime)
        return 0

    def hotExit(self,mes):
        print(mes)
        exit(1)



    def getListVideo(self,ytchlID,liveDay):
        # ytchlID: youtube chal id
        # liveDay: so ngay video da duoc upload. 2 thang

        videos = scrapetube.get_channel(ytchlID)
        for video in videos:
            self.listYTVideoID.append(video['videoId'])
            if self.checkLiveDay(video,liveDay) == 0:
                break

    def getAllVideoIDInTimeRange(self,liveDay):
        for chal in listYtbChl:
            self.getListVideo(chal,liveDay)
        ...

    # def getSubTitle(self,ytVideoID):
    def getAndCheckKeyword(self,ytVideoID):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(ytVideoID)
        except:
            return
        retSub=""
        for transcript in transcript_list:
            try:
                texts = transcript.translate('en').fetch()
                for text in texts:
                    retSub += text['text']+" "
                
                for i in range(0,len(self.listAllBinanceToken)):
                    token = self.listAllBinanceToken[i]
                    self.listAllBinanceTokenCount[i] = self.listAllBinanceTokenCount[i]+retSub.count(token+" ")
                # 
            except:
                self.hotExit(["loi ham getAndCheckKeyword",ytVideoID])

    def gateWay(self,liveDay):
        self.getAllVideoIDInTimeRange(liveDay)
        lengListYTVideoID = len(self.listYTVideoID)
        print("Found "+ str(lengListYTVideoID)+" video\nStart search keyword...")

        for i in range (0,lengListYTVideoID):
            print(str(i+1)+"/"+str(lengListYTVideoID))
            self.getAndCheckKeyword(self.listYTVideoID[i])
            # print(self.listAllBinanceTokenCount)
        retFile = open("ret.txt","w")
        for i in range(0,len(self.listAllBinanceTokenCount)):
            if self.listAllBinanceTokenCount[i] > 0:
                retFile.write(self.listAllBinanceToken[i]+"    "+str(self.listAllBinanceTokenCount[i])+"\n")


# yk.getAndCheckKeyword("ZXHiJHPNcu8&t=3s")

def main():
    parser = argparse.ArgumentParser(description="Used: python3 a1.py -ld 30")
    parser.add_argument('-ld', '-liveDay', dest="liveDay",
                        help="So ngay can kiem tra", action="store", default="30", required=1)
    args = parser.parse_args()
    yk = youtubeKeyword()
    yk.gateWay(int(args.liveDay))
if __name__ == "__main__":
    main()