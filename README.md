## FlacInfoTool - 更新Flac信息工具
很多时候下载回来的flac音乐文件里面的信息不全,放在音乐播放器里面看着不爽  
所以有了这个脚本,从QQ音乐搜索歌曲名称、音乐家，再将信息插入到flac文件中   
使用版本:  
**Python 2.7.x**  
**OSX**  
需要 requests 以及 taglib  

    usage: FlacInfoTool.py [-h] [-d DIR] [-f FILE] [-force]
    
    optional arguments:
      -h, --help        show  this help message and exit
      -d DIR, --dir     DIR   path name. e.g:FlacInfoTool.py -d /music/
      -f FILE, --file   FILE  file name. e.g:FlacInfoTool.py -f python.flac
      -force, --force         force update flac file all info
    
**使用方法:**  
更新目录下面的所有flac文件

    python FlacInfoTool.py -d /music/

更新单个flac文件
 
    python FlacInfoTool.py -f python.flac

强制更新就是覆盖原文件已经存在的信息

    python FlacInfoTool.py -d /music/ -force

