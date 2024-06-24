from .models import TRA, THSR, Metro, Image,THSR_Schedule,StopTime,Metro_sta,Metro_sta_to_sta,THSRODFare
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from django.shortcuts import render
from django import forms
from datetime import datetime

Client_id = 'b1043003-1164d050-a05c-4884'
Client_Secret = '8f5b9442-be4e-41f7-90b7-e4e863c36516'

auth_data = {
    'client_id':Client_id,
    'client_secret':Client_Secret,
    'grant_type':'client_credentials'
    }
    
auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TRA_url = "https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/DailyTimetable/Today?%24top=30&%24format=JSON"
THSR_url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/Today?%24top=100&%24format=JSON'
Metro_url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationTimeTable/TRTC?%24top=30&%24format=JSON'
image_url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/Shape?%24top=30&%24format=JSON'

Metro_all_station_url = 'https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/S2STravelTime/TRTC?%24top=30&%24format=JSON'

auth_response = requests.post(auth_url,data=auth_data)
auth_json = auth_response.json()
access_token = auth_json['access_token']

headers = {
    'Authorization':f'Bearer {access_token}'
}

def home(request):
    now = datetime.now()
    fetch_data()
    return render(request, 'main.html', locals())

def fetch_data():
    
    response = requests.get(TRA_url,headers=headers)
    data = response.json()
    fetch_TRA(data)
    response = requests.get(THSR_url,headers=headers)
    data = response.json()
    fetch_THSR(data)
    response = requests.get(Metro_url,headers=headers)
    data = response.json()
    fetch_Metro(data)
    response = requests.get(image_url,headers=headers)
    data = response.json()
    for item in data:
        image = Image(
            Geometry = item['Geometry']
        )
        image.save()

def fetch_TRA(data):
    for item in data:
        item = item['DailyTrainInfo']
        tra = TRA(
            TrainNo = item['TrainNo'],
            Direction = item['Direction'],
            StartingStationID = item['StartingStationID'],
            StartingStationName = item['StartingStationName']['Zh_tw'],
            EndingStationID = item['EndingStationID'],
            EndingStationName = item['EndingStationName']['Zh_tw'],
            TrainTypeName = item['TrainTypeName'],
            TripLine = item['TripLine'],
            PackageServiceFlag = item['PackageServiceFlag'],
            DailyFlag = item['DailyFlag']
        )
        tra.save()

def create_tra_schedule(data,s1,s2):
    r=""
    tmp=""
    tmp2=""
    s_id=""
    e_id=""
    f1=0
    f2=0
    t=0
    for i in data:
        for j in i['StopTimes']:
            
            arrival_time = j['ArrivalTime'] if 'ArrivalTime' in j else "N/A"
            departure_time = j['DepartureTime'] if 'DepartureTime' in j else "N/A"
            
            
            if s1 == f"{j['StationName']['Zh_tw']}":
                f1=1
                s_id = f"{j['StationID']}"
            if s2 == f"{j['StationName']['Zh_tw']}":
                f2=1
                e_id = f"{j['StationID']}"
            

            if ((f1==1) and (f2==1) and (t==0)):
                
                response = requests.get(f"https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/ODFare/1000/to/0980?%24top=30&%24format=JSON", headers=headers)
                tra_fare = response.json()
                for i in tra_fare:
                    for t in i['Fares']:
                        if (t['TicketType'] ==  "成自"):
                            tmp2+= str(t['Price'])+" 元整"
                
                tmp += f"{j['StopSequence']} {j['StationID']} {j['StationName']['Zh_tw']} {arrival_time} {departure_time}\n"
                r += tmp2+"\n"
                r += tmp
                t=1
            elif f1==1:
                tmp += f"{j['StopSequence']} {j['StationID']} {j['StationName']['Zh_tw']} {arrival_time} {departure_time}\n"
            elif f2==1:
                t=1
        
    
    return r
        
def TRA_OUTPUT(request):
    result = ""  # 初始化 result 變數為空字串
    if request.method == 'POST':
        from_station = request.POST.get('start_station')
        to_station = request.POST.get('end_station')
        TRAS = TRA.objects.all()[:100]
        for T in TRAS:
            TRA_Schedule_url = f"https://tdx.transportdata.tw/api/basic/v2/Rail/TRA/DailyTimetable/Today/TrainNo/{T.TrainNo}?%24top=30&%24format=JSON"  
            response = requests.get(TRA_Schedule_url, headers=headers)
            tra_schedule_data = response.json()
            if create_tra_schedule(tra_schedule_data, from_station, to_station) != "":
                train_type = T.TrainTypeName.split("'Zh_tw': '")[1].split("', 'En'")[0]
                result += f"{T.TrainNo} {T.StartingStationName} -> {T.EndingStationName} {train_type}\n"
                result += create_tra_schedule(tra_schedule_data, from_station, to_station)
                result += "\n"
    
    context = {'result': result}
    return render(request, 'TRA.html', context)
        
def fetch_Metro(data):
    for item in data:
        for i in item['Timetables']:
            i = i
        metro = Metro(
            RouteID = item['RouteID'],
            StationID = item['StationID'],
            StationName = item['StationName']['Zh_tw'],
            Direction = item['Direction'],
            DestinationStaionID = item['DestinationStaionID'],
            DestinationStationName = item['DestinationStationName']['Zh_tw'],
            Sequence = i['Sequence'],
            ArrivalTime = i['ArrivalTime'],
            DepartureTime = i['DepartureTime'],
            TrainType = '0'
        )
        metro.save()     
        
def Metro_OUTPUT(request):
    
    Metro_Schedule_url = f"https://tdx.transportdata.tw/api/basic/v2/Rail/Metro/StationTimeTable/TRTC?%24top=30&%24format=JSON"  
    response = requests.get(Metro_Schedule_url, headers=headers)
    result = response.json()
    
#     Metros = Metro.objects.all()[:60]
#     result = ""
#     for t in Metros:
#         
#         result += f"{t.RouteID} {t.StationName} {t.DestinationStationName} {t.Sequence} {t.ArrivalTime} {t.DepartureTime} \n"

    return HttpResponse(result, content_type="text/plain; charset=utf-8")

def fetch_THSR(data):
    for item in data:
        for i in item['StopTimes']:
            i = i
        thsrs = THSR(
            TrainDate = item['TrainDate'],
            TrainNo = item['DailyTrainInfo']['TrainNo'],
            Direction = item['DailyTrainInfo']['Direction'],
            StartingStationID = item['DailyTrainInfo']['StartingStationID'],
            StartingStationName = item['DailyTrainInfo']['StartingStationName']['Zh_tw'],
            EndingStationID = item['DailyTrainInfo']['EndingStationID'],
            EndingStationName = item['DailyTrainInfo']['EndingStationName']['Zh_tw'],
            StopSequence = i['StopSequence'],
            ArrivalTime = i['ArrivalTime'],
            DepartureTime = i['DepartureTime']
        )
        thsrs.save()
       
def create_thsr_schedule(data,s1,s2):
    r=""
    tmp=""
    f1=0
    f2=0
    t=0
    for i in data:
        s_id=""
        e_id=""
        tmp2=""
        for j in i['StopTimes']:
            
            arrival_time = j['ArrivalTime'] if 'ArrivalTime' in j else "N/A"
            departure_time = j['DepartureTime'] if 'DepartureTime' in j else "N/A"
            
            
            if s1 == f"{j['StationName']['Zh_tw']}":
                f1=1
                s_id= f"{j['StationID']}"
            if s2 == f"{j['StationName']['Zh_tw']}":
                f2=1
                e_id= f"{j['StationID']}"

            if ((f1==1) and (f2==1) and (t==0)):
                response = requests.get(f"https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/ODFare/{s_id}/to/{e_id}?%24top=30&%24format=JSON", headers=headers)
                thsr_fare = response.json()
                for i in thsr_fare:
                    for t in i['Fares']:
                        if (t['TicketType'] == 1) and (t['FareClass'] == 1) and (t['CabinClass'] == 1):
                            tmp2+= str(t['Price'])+" 元整"
                
                            tmp += f"{j['StopSequence']} {j['StationID']} {j['StationName']['Zh_tw']} {arrival_time} {departure_time}\n"
                
                r += tmp2+"\n"
                r += tmp
                t=1
            elif f1==1:
                tmp += f"{j['StopSequence']} {j['StationID']} {j['StationName']['Zh_tw']} {arrival_time} {departure_time}\n"
            elif f2==1:
                t=1
    return r

def THSR_OUPUT(request):
    now = datetime.now()
    class StationForm(forms.Form):
        start_station = forms.CharField(label='起點站')
        end_station = forms.CharField(label='終點站')

    context = {} 
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            from_station = form.cleaned_data['start_station']
            to_station = form.cleaned_data['end_station']

            thsr = THSR.objects.all()[:30]

            if thsr.exists():
                result = []
                for thsr_obj in thsr:
                    THSR_Schedule_url = f"https://tdx.transportdata.tw/api/basic/v2/Rail/THSR/DailyTimetable/Today/TrainNo/{thsr_obj.TrainNo}?%24top=30&%24format=JSON"  
                    response = requests.get(THSR_Schedule_url, headers=headers)
                    thsr_schedule_data = response.json()
                    
                    if(create_thsr_schedule(thsr_schedule_data,from_station,to_station)!=""):
                        #result += f"車次:{thsr_obj.TrainNo} "
                        #result += create_thsr_schedule(thsr_schedule_data,from_station,to_station)
                        result.append((thsr_obj.TrainNo, create_thsr_schedule(thsr_schedule_data, from_station, to_station)))

                        #result += f"{thsr_obj.TrainNo} \n"
                        #result += create_thsr_schedule(thsr_schedule_data, from_station, to_station)
                context = {'result': result}
        else:
            form = StationForm()
    else:
        form = StationForm()  # 初始化表單

    context['form'] = form  # 將表單加入上下文
    return render(request, 'THSR.html', context)
                
def METRO(request):
    result=""
    context={}
    if request.method == 'POST':
        from_station = request.POST.get('start_station')
        to_station = request.POST.get('end_station')
        result += "起點站: "+from_station
        result += "\t終點站: "+to_station+"\n\n"
        
        from_station_id = Metro_sta.objects.filter(StationName_Zh_tw = from_station)
        to_station_id = Metro_sta.objects.filter(StationName_Zh_tw = to_station)
        tmps_id=[]
        tmps_name=[]
        tmpe_id=[]
        tmpe_name=[]
        s_id=""
        e_id=""
        f=0 #0轉車
        
        for i in from_station_id:
            tmps_id.append(str(i.StationID))
            tmps_name.append(str(i.StationName_Zh_tw))
            
        for i in to_station_id:
            tmpe_id.append(str(i.StationID))
            tmpe_name.append(str(i.StationName_Zh_tw))
            
        for i in tmps_id:
            for j in tmpe_id:
                if ((len(i)==4) and (len(j)==4)):
                    if i[:2] == j[:2]:
                        s_id = i
                        e_id = j
                        
                        f=1
                else:
                    if i[0] == j[0]:
                        s_id = i
                        e_id = j
                        f=1
        
                        
        if f==1:
            x=0
            t_id=s_id
            sum_time=0
        
            if int(s_id[-2:])<int(e_id[-2:]):
                id_ = Metro_sta.objects.filter(StationID__range=(s_id, e_id))
                
                for i in id_:
                    if int(int(i.StationID[-2])*10+int(i.StationID[-1])+1) <= int(e_id[-2:]):
                        next_id = str(e_id[:-2])+str(int(int(i.StationID[-2])*10+int(i.StationID[-1])+1))
                        tmp = Metro_sta_to_sta.objects.filter(FromStationID = next_id )[:1]    
                        #result += str(i.StationID[:-2]+str(0)*((int(i.StationID[-2])*10+int(i.StationID[-1]))<10)+str(int(i.StationID[-2])*10+int(i.StationID[-1])))
                        #result += str(tmp)
                        #result += "  "+next_id+"\n"
                        x=1
                    for j in tmp[:1]:
                        if x==1:
                            run = j.RunTime
                            stop = j.StopTime
                            sum_time += run+stop
                            result += "{:5}".format(j.ToStationID)+"{:10}".format(j.ToStationName_Zh_tw)+"\t{} ".format(j.FromStationID)+"{:10}".format(j.FromStationName_Zh_tw)+f"\t行駛時長: {(run+stop)//60}分{(run+stop)%60}秒\n"
                            x=0
                    
            elif int(s_id[-2:])>int(e_id[-2:]):
                id_ = Metro_sta.objects.filter(StationID__range=(e_id, s_id))[::-1]
                for i in id_[:-1]:
                    tmp = Metro_sta_to_sta.objects.filter(FromStationID = i.StationID ,ToStationID = str(i.StationID[:-2]+str(0)*((int(i.StationID[-2])*10+int(i.StationID[-1])-1)<10)+str(int(i.StationID[-2])*10+int(i.StationID[-1])-1)))      
                    #result += +"\n"
                    for j in tmp:
                        run = j.RunTime
                        stop = j.StopTime
                        sum_time += run+stop
                        
                        result += "{:5}".format(j.FromStationID)+"{:10}".format(j.FromStationName_Zh_tw)+"\t{} ".format(j.ToStationID)+"{:10}".format(j.ToStationName_Zh_tw)+f"\t行駛時長: {(run+stop)//60}分{(run+stop)%60}秒\n"
            
            result += "\n總共行駛:"+str(sum_time//60)+"分"+str((sum_time%60)//10)+str((sum_time%60)%10)+"秒"
    
        
    
    context = {'result': result}
    return render(request, 'Metro.html', context)