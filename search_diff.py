__author__ = 'wenshi.chen'
# encoding=utf-8



import sys
import time
import re
import codecs
import simplejson as json
import urllib2
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#input file
topQueryFile = open("TG_Search_TopQuery.txt", "r")

#output file
searchDealGroupFile = open("SearchDealGroup.txt", "w")

keywordDict = {}
#define url pattern
#newUrlPattern = "http://10.1.11.21:4123/search/tuangou?query=term(cityid,_CITYID_,-1),keyword(searchkeyword,_KEYWORD_)&sort=desc(intell)&limit=0,96&fl=dealgroupid,dealgroupshorttitleindexed&info=referguid:c0a8d59f-145b1adc1e2-71,geotype:shopgooglepos,app:tuangou,platform:WWW,referrequestid:d849fe39-c0fa-4ab5-936a-67deefac0486,mapitype:0,locatecity:_CITYID_,userIP:210.22.122.2,queryid:98f19d67-8bd5-4c04-9f92-92a7dfee5988,clientip:192.168.213.226,functiontype:1,shoplocatecity:_CITYID_,searchcity:_CITYID_,cookieId:356534050199593,lng:121.42001563424382,locateaccuracy:0,nettype:1,userId:0,requestid:24dd4ea2-6797-4ac4-bf60-5d174e0adfd0,channel:0,lat:31.215635033935374,requesttype:0,recordscoredetail:true"
newUrlPattern = "http://10.1.11.21:4123/search/tuangou?query=term(cityid,_CITYID_,-1),keyword(searchkeyword,_KEYWORD_)&filter=range(enddate,_NOWTIME_,null,true,false),range(begindate,null,_NOWTIME_,true,false)&sort=asc(defaultsort)&limit=0,96&fl=dealgroupid,dealgroupshorttitleindexed&info=referguid:0a010470-146a2498226-10bec0,geotype:shopgooglepos,app:AppName.TG,platform:WWW,userIP:180.166.152.90,queryid:e6c55228-20ca-406d-96cd-8253cc2fbbec,clientip:10.1.111.178,functiontype:0,shoplocatecity:_CITYID_,searchcity:_CITYID_,cookieId:2f99265f-2292-4884-b7be-0e837625a400,lng:0.0,retrytimes:1,locateaccuracy:0,rankcity:_CITYID_,userId:0,requesttype:0,lat:0.0,recordscoredetail:true"
oldUrlPattern = "http://10.1.11.21:4123/search/tuangou?query=term(cityid,_CITYID_,-1),keyword(searchkeyword,_KEYWORD_)&filter=range(enddate,_NOWTIME_,null,true,false),range(begindate,null,_NOWTIME_,true,false)&sort=asc(defaultsort)&limit=0,96&fl=dealgroupid,dealgroupshorttitleindexed&info=geotype:shopgooglepos,app:AppName.TG,platform:WWW,userIP:180.166.152.90,queryid:bb832b03-2a17-4df2-a2dd-c749c497ed85,clientip:10.1.108.187,functiontype:0,shoplocatecity:_CITYID_,searchcity:_CITYID_,cookieId:2f99265f-2292-4884-b7be-0e83763265,lng:0.0,retrytimes:1,locateaccuracy:0,rankcity:_CITYID_,userId:0,requesttype:0,lat:0.0"

nowtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
newUrlPattern=re.sub("_NOWTIME_",nowtime,newUrlPattern)
oldUrlPattern=re.sub("_NOWTIME_",nowtime,oldUrlPattern)


for line in topQueryFile:
        lineArray = line.strip("\n").split("\t")
        newUrlTemp = re.sub("_KEYWORD_", urllib2.quote(lineArray[1]), newUrlPattern)
        newUrl = re.sub("_CITYID_", lineArray[0], newUrlTemp)
        oldUrlTemp = re.sub("_KEYWORD_", urllib2.quote(lineArray[1] + "  "), oldUrlPattern)
        oldUrl = re.sub("_CITYID_", lineArray[0], oldUrlTemp)
        if(lineArray[0] == "0"):
            continue
        keyword = lineArray[0] + "\t" + lineArray[1] + "\t" + lineArray[2]
        newSearchDealListJson = urllib2.urlopen(newUrl).read()
        oldSearchDealListJson = urllib2.urlopen(oldUrl).read()
        newSearchDealList = json.loads(newSearchDealListJson)
        oldSearchDealList = json.loads(oldSearchDealListJson)
        searchIndex = 0
        newHitsNum = int(newSearchDealList['totalhits'])
        oldHitsNum = int(oldSearchDealList['totalhits'])
	oldshortTitle=""
	count=0#计数器
	for obj in oldSearchDealList['records']:
		if(count==0):
			oldshortTitle = obj['dealgroupshorttitleindexed']
		else:
			oldshortTitle = oldshortTitle+";"+obj['dealgroupshorttitleindexed']
		count=count+1;
		if(count>2):
			break
        #print  oldSearchDealListJson
       # print keyword
       # print keyword + "," + str(newHitsNum) + "," + str(newHitsNum - oldHitsNum)
	
        if oldHitsNum == 0 and newHitsNum==0:
            searchDealGroupFile.write(keyword + "\t0"+"\t"+oldshortTitle + "\n")
	    print keyword
	if oldHitsNum == 0 and newHitsNum<>0:
	    searchDealGroupFile.write(keyword + "\t1" +"\t"+oldshortTitle +  "\n")
	if oldHitsNum <> 0 and newHitsNum==0:
            searchDealGroupFile.write(keyword + "\t2" +"\t"+oldshortTitle +  "\n")
	if oldHitsNum <> 0 and newHitsNum>oldHitsNum:
            searchDealGroupFile.write(keyword + "\t3" + "\t"+oldshortTitle + "\n")
	if oldHitsNum > newHitsNum and newHitsNum<>0:
            searchDealGroupFile.write(keyword + "\t4" +"\t"+oldshortTitle +  "\n")
	    print keyword
	if oldHitsNum == newHitsNum and newHitsNum<>0:
            searchDealGroupFile.write(keyword + "\t5" + "\t"+oldshortTitle + "\n")

searchDealGroupFile.close()

