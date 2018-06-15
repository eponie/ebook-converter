# ebook-converter

## 簡介

在Mac上把中文epub轉成直排mobi

## 如何安裝

0. 要裝 python 2.7
1. git clone 本專案
2. 下載 KindleGen for mac: https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211
3. 下載 KindleUnpack https://github.com/kevinhendricks/KindleUnpack
4. 解壓縮放在專案資料夾下
```
KindleGen_Mac_i386_v2_9 epub2vmobi.py
KindleUnpack-master     ebc.conf
```
5. 在ebc.conf設定執行檔位置
```
[ebc]
kindleunpack = ./KindleUnpack-master/lib/kindleunpack.py
kindlegen = ./KindleGen_Mac_i386_v2_9/kindlegen
```
6. 可以用啦

## 如何執行

```
python epub2vmobi.py epub檔案路徑 書名(中文可)

```

```
python checknew.py epub檔案路徑(wildcard可)
# e.g. python checknew.py /Users/miew_user/Calibre\ Library/*/*/*.epub 
# 找出今天修改過的epub檔案
```

## 備註

- 目前成功率九成
- 圖多or圖大的書不適合，拿來轉純文字最好


-----------

## Introduction

This is to convert (DRM-free) traditional Chinese epub to vertically aligned .mobi for Amazon Kindle on Mac.

## How to Install

0. Install python 2.7 (sorry!)
1. Clone this project 
2. Get KindleGen for mac here https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211
3. Get KindleUnpack https://github.com/kevinhendricks/KindleUnpack
4. Now your folder look like this:
```
KindleGen_Mac_i386_v2_9 epub2vmobi.py
KindleUnpack-master     ebc.conf
```
5. Set up path in ebc.conf like this:
```
[ebc]
kindleunpack = ./KindleUnpack-master/lib/kindleunpack.py
kindlegen = ./KindleGen_Mac_i386_v2_9/kindlegen
```
6. Good to go!

## How to Use

```
python epub2vmobi.py path2epub booktitle
```

```
python checknew.py path2epub(wildcard)
# e.g. python checknew.py /Users/miew_user/Calibre\ Library/*/*/*.epub 
# find the files modified today
```

## Note

- 90% successful
- No good for book with huge/mass image


