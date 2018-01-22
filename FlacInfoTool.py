#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:Tea

import os
import sys
import time
import json
import urllib
import taglib
import logging
import requests
import argparse

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def main():
    args = getArg()
    qqMusicUrlStr = qqMusicUrl()
    if args.file and os.path.isfile(args.file):
        updateTagInfoForFile(args.file, qqMusicUrlStr, args.force)
    elif args.dir and os.path.isdir(args.dir):
        for dirPath, dirNames, fileNames in os.walk(args.dir):
            for fileName in fileNames:
                filePath = os.path.join(dirPath, fileName)
                updateTagInfoForFile(filePath, qqMusicUrlStr, args.force)
    else:
        logging.warning('Parameter not match...')
        sys.exit()


def updateTagInfoForFile(flacPath, qqMusicUrlStr, mandatoryUpdating=False):
    fullName = os.path.basename(flacPath)
    print fullName
    if fullName.lower().endswith('.flac'):
        songName = os.path.basename(fullName)[:-5]
        print songName
        # search_par = urllib.urlencode({"w": FileName.decode('gbk').encode('utf-8')}).replace('+', '%20')  # Windows
        searchPar = urllib.urlencode({"w": songName}).replace('+', '%20')  # OSX
        qqMusicUrl = qqMusicUrlStr + searchPar
        song = taglib.File(flacPath)
        print flacPath
        if mandatoryUpdating:
            qqJson = requestQQMusic(qqMusicUrl)
            qqJsonResult = json.loads(qqJson)
            song.tags["TITLE"] = qqJsonResult['data']['song']['list'][0]['title']  # TITLE
            song.tags["ARTIST"] = qqJsonResult['data']['song']['list'][0]['singer'][0]['title']  # ARTIST
            song.tags["ALBUM"] = qqJsonResult['data']['song']['list'][0]['album']['title']  # ALBUM
            song.save()
        else:
            if not song.tags:
                qqJson = requestQQMusic(qqMusicUrl)
                qqJsonResult = json.loads(qqJson)
                song.tags["TITLE"] = qqJsonResult['data']['song']['list'][0]['title']  # TITLE
                song.tags["ARTIST"] = qqJsonResult['data']['song']['list'][0]['singer'][0]['title']  # ARTIST
                song.tags["ALBUM"] = qqJsonResult['data']['song']['list'][0]['album']['title']  # ALBUM
                song.save()
            if song.tags.get("ARTIST") is None and song.tags.get("TITLE") is None and song.tags.get("ALBUM") is None:
                qqJson = requestQQMusic(qqMusicUrl)
                qqJsonResult = json.loads(qqJson)
                if not song.tags.get("ARTIST"):
                    song.tags["ARTIST"] = qqJsonResult['data']['song']['list'][0]['singer'][0]['title']  # ARTIST
                if not song.tags.get("TITLE"):
                    song.tags["TITLE"] = qqJsonResult['data']['song']['list'][0]['title']  # TITLE
                if not song.tags.get("ALBUM"):
                    song.tags["ALBUM"] = qqJsonResult['data']['song']['list'][0]['album']['title']
                song.save()
            print song.tags


def qqMusicUrl():
    return 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid=53376023965311626&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&g_tk=1476104164&loginUin=463718346&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&'


def requestQQMusic(QQUrl):
    try:
        QQResult = requests.get(QQUrl).text
        return QQResult
    except Exception:
        time.sleep(3)
        requestQQMusic(QQUrl)


def getArg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', type=str, help='path name. e.g:FlacInfoTool.py -d /music/')
    parser.add_argument('-f', '--file', type=str, help='file name. e.g:FlacInfoTool.py -f python.flac')
    parser.add_argument('-force', '--force', help='force update flac file all info', action='store_true')
    args = parser.parse_args()
    if (args.file and args.dir) or (not args.dir and not args.file):
        parser.print_help()
        sys.exit()
    existsTag = args.dir if args.dir else args.file
    if not os.path.exists(existsTag):
        logging.warning('Path or File is not exists')
        sys.exit()
    return args


if __name__ == '__main__':
    main()
