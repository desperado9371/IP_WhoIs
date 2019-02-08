# -*- coding: utf-8 -*-

import requests
import json

#########################################################################################################
def findWhoIs(ip):
    ip_address = ip
    
    # key값 오류 발생시 https://xn--c79as89aj0e29b77z.xn--3e0b707e/kor/whois/openAPI_KeyCre.jsp  서 새로 받으실수 있습니다.
    key = "2019020711065118499589"
    url = "http://whois.kisa.or.kr/openapi/whois.jsp?query="+ip_address+"&key="+key+"&answer=json"

    req = requests.get(url)
    
    country_code=""
    isp_name=""
    user_name=""
    
    #error 
    if req.text.find("error_code") !=-1:
        index= req.text.find("error_code")
        print("ERROR  ",end="")
        err= req.text[index+13:index+16]
        if err=="000":
            print("시스템오류")
        elif err=="012":
            print("잘못된 쿼리")
        elif err=="021":
            print("등록되지 않은 키")
        elif err=="022":
            print("사용할 수 없는 키")
        elif err=="031":
            print("잘못된 주소형식")
        elif err=="9NNNN":
            print("서버오류")
        return "error",
    
    json_response = json.loads(req.content)
    country_code = json_response["whois"]["countryCode"]
    
    #IF the Countrycode is not KR(korea) return just country_code
    if country_code!="KR":
        print(country_code)
        return country_code,
     
    #ELSE return country code + ISP name + user name
    else:
        print(json_response["whois"]["countryCode"], end=", ")
        if 'PI' in json_response["whois"]["korean"]:
            isp_name="PI : "+json_response["whois"]["korean"]["PI"]["netinfo"]["orgName"]
    
        elif 'ISP' in json_response["whois"]["korean"]:
            isp_name="ISP : "+json_response["whois"]["korean"]["ISP"]["netinfo"]["orgName"]
        if 'user' in json_response["whois"]["korean"]:
            user_name="User : "+ json_response["whois"]["korean"]["user"]["netinfo"]["orgName"]
        print(isp_name+" "+user_name)
        return country_code, isp_name,user_name
############################################################################################################
        
    
with open('ip.csv') as file:
    result = open('result.txt','w')
    korea = open('korea.txt','w')
    koscom = open('koscom.txt','w')
    
    kr_cnt=0        # 한국 ip 카운터
    koscom_cnt=0    # 코스콤 ip 카운터
    csv_data=[]
    
    for line in file.readlines():
        csv_data.append(line.split(','))
    for ip in csv_data[0]:
        ip=ip.replace(" ","")
        
        print('%-14s - '%(ip),end="")
        
        list = findWhoIs(ip)
        
        result.write(ip+" - ")
        
        if list[0]=="KR":
            kr_cnt+=1
            korea.write(ip+"  -  "+list[1]+" , "+list[2]+"\n")
            if list[1].find("코스콤")!=-1:
                koscom_cnt+=1
                koscom.write(ip+"  -  "+list[1]+" , "+list[2]+"\n")
        for a in list:
            result.write(a+",")
        result.write("\n")
        
    print("\n한국소재 IP주소는 {}개 이며,".format(kr_cnt))
    print("코스콤과 연관된 주소는 {}개 입니다.".format(koscom_cnt))
    
    print("전체결과는 result.txt에 한국IP는 korea.txt에 코스콤IP는 koscom.txt에서 보실수 있습니다.")
    
    result.close();
    korea.close();
    koscom.close();
    
    print("\n종료하시려면 ENTER입력")
    a=input()