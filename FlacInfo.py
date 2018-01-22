#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import os
import sys
import time
import json
import urllib
import taglib
import requests

def main():
    FlacPath = sys.argv[1]
    if not os.path.exists(FlacPath):
        sys.exit('PathError')
    if os.path.isdir(FlacPath):
        #print 'Is Dir'
        for dir_path, dir_names, file_names in os.walk(FlacPath):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                UpdateTagInfoForFile(file_path)
    else:
        #print 'Is File'
        UpdateTagInfoForFile(FlacPath)

def UpdateTagInfoForFile(flacpath,mandatoryupdating=False):
    fullname = os.path.basename(flacpath)
    if fullname.lower().endswith('.flac'):
        songname = os.path.basename(fullname)[:-5]
        #search_par = urllib.urlencode({"w": FileName.decode('gbk').encode('utf-8')}).replace('+', '%20')  # Windows
        search_par = urllib.urlencode({"w": songname}).replace('+', '%20')  # OSX
        QQMusicUrl = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid=53376023965311626&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&g_tk=1476104164&loginUin=463718346&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&" + search_par
        song = taglib.File(flacpath)
        print flacpath
        if mandatoryupdating:
            QQJson = RequestQQMusic(QQMusicUrl)
            QQJsonResult = json.loads(QQJson)
            song.tags["TITLE"] = QQJsonResult['data']['song']['list'][0]['title']  #TITLE
            song.tags["ARTIST"] = QQJsonResult['data']['song']['list'][0]['singer'][0]['title']  #ARTIST
            song.tags["ALBUM"] = QQJsonResult['data']['song']['list'][0]['album']['title']  #ALBUM
            song.save()
        else:
            if not song.tags:
                QQJson = RequestQQMusic(QQMusicUrl)
                QQJsonResult = json.loads(QQJson)
                song.tags["TITLE"] = QQJsonResult['data']['song']['list'][0]['title']  # TITLE
                song.tags["ARTIST"] = QQJsonResult['data']['song']['list'][0]['singer'][0]['title']  # ARTIST
                song.tags["ALBUM"] = QQJsonResult['data']['song']['list'][0]['album']['title']  # ALBUM
                song.save()
            if song.tags.get("ARTIST") is None and song.tags.get("TITLE") is None and song.tags.get("ALBUM") is None:
                QQJson = RequestQQMusic(QQMusicUrl)
                QQJsonResult = json.loads(QQJson)
                if not song.tags.get("ARTIST"):
                    song.tags["ARTIST"] = QQJsonResult['data']['song']['list'][0]['singer'][0]['title']  #ARTIST
                if not song.tags.get("TITLE"):
                    song.tags["TITLE"] = QQJsonResult['data']['song']['list'][0]['title']  #TITLE
                if not song.tags.get("ALBUM"):
                    song.tags["ALBUM"] = QQJsonResult['data']['song']['list'][0]['album']['title']
                song.save()
            print song.tags

def RequestQQMusic(QQUrl):
    try:
        QQResult = requests.get(QQUrl).text
        return QQResult
    except Exception,e:
        time.sleep(3)
        RequestQQMusic(QQUrl)

if __name__ == '__main__':
    main()