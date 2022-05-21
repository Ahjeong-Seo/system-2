from ast import keyword
from difflib import restore
from gettext import find
from stat import FILE_ATTRIBUTE_NOT_CONTENT_INDEXED
import tweepy
import time
import random
from random import randint
import datetime
import os

API_KEY = os.environ.get('API_KEY')
API_KEY_SECRET = os.environ.get('API_KEY_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

USER_TOKEN = os.environ.get('USER_TOKEN')
USER_SECRET =os.environ.get('USER_SECRET')

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET, callback='oob')

auth.set_access_token(USER_TOKEN,USER_SECRET)

api = tweepy.API(auth)

bot = api.verify_credentials()
bot_id = bot.id
last_reply_id = 1
keywords = ['주사위', '행운뽑기', '불운뽑기', '가위바위보', '대결', '낚시대회', '수갑게임'] 
lucky_thing = ['[보통] 누군가의 안경','[보통] 도라지청','[보통] 뜨끈한 국밥 한 그릇','[보통] 비녀','[보통] 샌드백','[보통] 양은냄비','[보통] 장구채','[보통] 효자손','[보통] 후라이팬','[희귀] 8비트 선글라스','[희귀] 보약 한첩','[희귀] 뿅망치','[희귀] 연애소설 \'내가 이 궁의 유일한 보물이라구욧?!\'','[희귀] 장구','[희귀] 하트뿅뿅 머리띠','[전설] 공주님♡왕관(장난감)','[전설] 물풍선 5개','[전설] 홍삼맛 사탕 50개','[신화] 천종산삼 200년산','[신화] 포켓몬볼..?','꽝']
lck_normal = [0] * 9
lck_rare = [0] * 6
lck_legend = [0] * 3
lck_myth = [0] * 2
lck_none = 0
unlucky_thing = ['[보통] 곤장 1대 무료이용권(본인 한정 사용)','[보통] 궁례겨 등신대','[보통] 기왓장 10개','[보통] 기왓장 20개','[보통] 당신만을 따라다니는 원숭이(인형?)(3시간 지속)','[보통] 대군 등신대','[보통] \'대흉길\'이라고 적힌 종이','[보통] 바나나 껍질 (잘 미끄러지게 생김)','[보통] 쑥과 마늘 10일치','[보통] 행운의 편지','[재앙] 눈덩이(후두둑!)','[재앙] 먹물이 찍! 옷들이 엉망!','[재앙] 물풍선(촤악!)','[재앙] 밀가루 폭탄','[재앙] 뿅망치(뾱!)','[재앙] 어라 여기에 구덩이갘 (슉!)','[재앙] 쟁반 노래방(깡!)','[재앙] 태양이 널 쫓아다녀 (3시간 지속)','[재난] 물벼락','[재난] 자네 불꽃 놀이라고 들어봤는가. (펑퍼퍼러펑펑)','꽝']
uck_normal = [0] * 10
uck_dis = [0] * 8
uck_evil = [0] * 2
uck_none = 0
person = api.get_follower_ids
person_len = 18

def check_new_mention() :
    print("! 멘션 확인 함수 호출")
    global last_reply_id
    mention_return = api.mentions_timeline(since_id = last_reply_id)
    mention_return_length = len(mention_return)

    if mention_return_length > 0 :
        print("! 키워드 체크 함수 호출")
        check_keyword(mention_return_length,mention_return)
        return

def check_keyword(mention_length, mention_return) :
    global last_reply_id
    for i in range(mention_length-1, -1, -1):
        mention = mention_return[i]
        mention_txt = mention.text
        keyword_type = -1
        keyword_ac_return = ''
        n = 0
        # 멘션 구분
        try:
            if mention.author.id != bot_id: #내가 내게 보낸 멘션 아님 확인
                print('내가 보낸 멘션 아님')
                start = mention_txt.find('[')
                end = mention_txt.find(']')
                if(start != -1 and end != -1) and start<end : 
                    that_keyword = mention_txt[start+1:end].strip()
                    keyword = that_keyword[0].strip()
                    keyword_find = that_keyword[1].strip()
                    print('키워드 있음')
                    if keyword == '주사위':
                        print('주사위 실행')
                        keyword_type = 1
                        keyword_ac_return = randint(1,100)
                    elif keyword == '행운뽑기' :
                        print('행운뽑기 실행')
                        keyword_type = 2
                        keyword_ac_return = roll_lucky()
                    elif keyword == '불운뽑기' :
                        print('불운뽑기 실행')
                        keyword_type = 3
                        keyword_ac_return = roll_unlucky()
                    elif keyword == '가위바위보' :
                        print('가위바위보 실행')
                        keyword_type = 4
                        n = randint(1,3)
                        keyword_ac_return = rock_k(n)
                    elif keyword == '대결' :
                        print('대결 실행')
                        keyword_type = 5
                        keyword_ac_return = rap_b(mention_length)
                    elif keyword == '낚시대회' :
                        print('낚시대회 실행')
                        keyword_type = 6
                        n = randint(1,100)
                        keyword_ac_return = fishtrap(n)
                    elif keyword == '수갑게임' :
                        keyword_type = 7
                        reply_content = find_key(keyword_find.replace(" ",""))
                
                    if keyword_type != -1 :
                        print('키워드 타입 확인')
                        if keyword_type == 1:
                            reply_content = "주사위 결과: " + str(keyword_ac_return)
                            reply_funtion(mention, reply_content)
                        elif keyword_type == 2 or keyword_type == 3 :
                            mk_reply_content(keyword_type, mention, keyword_ac_return)
                        elif keyword_type == 4 :
                            reply_content = "안내면 진 거 가위바위보!\n" + keyword_ac_return
                            reply_funtion(mention, reply_content)
                        elif keyword_type == 5 :
                            reply_content = "당신의 점수 : " + str(keyword_ac_return)
                            reply_funtion(mention, reply_content)
                        elif keyword_type == 6 :
                            reply_content = keyword_ac_return + " 을/를 낚았다!\n득점: " + str(n)
                            reply_funtion(mention, reply_content)
                        elif keyword_type == 7 :
                            reply_content(mention, reply_content)
            print('마지막으로 답변한 아이디: '+ last_reply_id)
        except:
            print('! 키워드 체크 도중 오류 발생')
            last_reply_id = mention.id_str
            

def fishtrap(n) :
    print('물고기 낚아유')
    if n == 100 :
        result = '[용왕이라 불리는 전설의 물고기가 아니라 상어?!?!?!]'
    elif n >= 90 :
        result = '[가물치]'
    elif n >= 80 :
        result = '[산천어]'
    elif n >= 70 :
        result = '[뱀장어]'
    elif n >= 60 :
        result = '[메기]'
    elif n >= 50 :
        result = '[잉어]'
    elif n >= 40 :
        result = '[송어]'
    elif n >= 30 :
        result = '[붕어]'
    elif n >= 20 :
        result = '[가물치]'
    elif n >= 10 :
        result = '[송사리]'
    else :
        result = '[쓰레기]'
    return result

def roll_lucky() :
    print('행뽑 굴러가유')
    n = randint(1,100)
    if lck_none < 6 or 0 in lck_myth or 0 in lck_legend or 1 in lck_legend or 0 in lck_rare or 1 in lck_rare or 2 in lck_rare or 0 in lck_normal or 1 in lck_normal or 2 in lck_normal or 3 in lck_normal :
        if n == 100 : 
            if lck_none < 6 : #5번까지만 돌아감
                lck_none += 1
                return lucky_thing[20]
            else :
                return roll_lucky()                
        elif n == 99 :
            if 0 in lck_myth : #0이 있어야만 돌아감
                i = randint(0,1)
                while lck_myth[i] == 1 : #1번 뽑힌 상태면 돌아감
                    i = randint(0,1) #신화급 2개
                lck_myth[i] += 1
                return lucky_thing[i+9+6+3]
            else :
                return roll_lucky()
        elif n > 89 :
            if 0 in lck_legend or 1 in lck_legend : #0이나 1상태가 있으면 돌아감
                i = randint(0,2)
                while lck_legend[i] == 2 : #2번 뽑힌 상태면 돌아감
                    i = randint(0,2) #전설급 3개
                lck_legend[i] += 1
                return lucky_thing[i+9+6]
            else :
                return roll_lucky()
        elif n > 68 :
            if 0 in lck_rare or 1 in lck_rare or 2 in lck_rare : #0이나 1상태가 있으면 돌아감
                i = randint(0,5)
                while lck_rare[i] == 3 : #3번 뽑힌 상태면 돌아감
                    i = randint(0,5) #희귀급 6개
                lck_rare[i] += 1
                return lucky_thing[i+9]
            else :
                return roll_lucky()
        elif n > 0 :
            if 0 in lck_normal or 1 in lck_normal or 2 in lck_normal or 3 in lck_normal :
                i = randint(0,8)
                while lck_normal[i] == 4 : #4번 뽑힌 상태면 돌아감
                    i = randint(0,8) #보통급 9개 
                lck_normal[i] += 1
                return lucky_thing[i]
            else :
                return roll_lucky()
    else :
        return ' '

def roll_unlucky(n) :
    print('불뽑 굴러가유')
    n = randint(1,100)
    if uck_none < 6 or 0 in uck_evil or 0 in uck_dis or 1 in uck_dis or 2 in uck_dis or 0 in uck_normal or 1 in uck_normal or 2 in uck_normal or 3 in uck_normal :
        if n == 100 : 
            if uck_none < 6 : #5번까지만 돌아감
                uck_none += 1
                return unlucky_thing[20]
            else :
                return roll_unlucky()
        elif n > 94 :
            if 0 in uck_evil : #0 있으면 돌아감
                i = randint(0,1)
                while uck_evil[i] == 1 :
                    i = randint(0,1) #재난급 2개
                uck_evil[i] += 1
                return unlucky_thing[i+8+10]
            else :
                return roll_unlucky()
        elif n > 68 :
            if 0 in uck_dis or 1 in uck_dis or 2 in uck_dis : #0, 1, 2상태가 있으면 돌아감
                i = randint(0,7)
                while uck_dis[i] == 3 : #3번 뽑힌 상태면 돌아감
                    i = randint(0,7) #재앙급 8개
                uck_dis[i] += 1
                return unlucky_thing[i+10]
            else :
                return roll_unlucky()
        elif n > 0 :
            if 0 in uck_normal or 1 in uck_normal or 2 in uck_normal or 3 in uck_normal : #0, 1, 2, 3 상태 있으면 돌아감
                i = randint(0,9)
                while lck_normal[i] == 4 : #4번 뽑힌 상태면 돌아감
                    i = randint(0,9) #보통급 10개 
                lck_normal[i] += 1
                return unlucky_thing[i]
            else :
                return roll_unlucky()
    else :
        return ' '

def rock_k(n) :
    result = ' '
    if n == 1 :
        result = '[가위]'
    elif n == 2 :
        result = '[주먹]'
    elif n == 3 :
        result = '[보자기]'
    return result

def rap_b(len) :
    result = 0
    if len >= 120 :
        result = 40 + randint(1,100)
    elif len >= 100 :
        result = 30 + randint(1,100)
    elif len >= 80 :
        result = 20 + randint(1,100)
    elif len >= 60 :
        result = 10 + randint(1,100)
    else :
        result = randint(1,100)
    if result > 100 :
        result = 100
    return result

def find_key(keyword) :
    find_f = "- 전각으로 간다\n- 앞마당으로 간다\n- 정자로 간다\n- 연못으로 간다\n- 조사를 그만둔다" #초반
    find_j = "- 전각 1층을 본다\n- 전각 2층을 본다\n- 계단을 본다\n- 기둥을 본다\n- 수상한 함을 본다\n- 돌아간다" #전각
    find_y = "- 수상한 흙더미를 본다\n- 커다란 나무를 본다\n- 해태상을 본다\n- 돌담을 본다\n- 땅따먹기 표를 본다\n- 돌아간다" #앞마당
    find_z = "- 정자 내부를 본다\n- 다과상을 본다\n- 두루마리를 본다\n- 굴러다니는 술병을 본다\n- 수상한 도포차람의 오리를 본다\n- 돌아간다" #정자
    find_w = "- 물가를 본다\n- 다리를 본다\n- 낚시터를 본다\n- 나룻배를 본다\n- 작은 섬을 본다\n- 돌아간다" #연못
    try:  
        if keyword == "조사시작" :
            first_line = "수갑 열쇠를 찾아보자! 엽전도 좋고!\n\n"
            find_content = find_f
        elif keyword == "돌아간다" :
            first_line = "처음으로 다시 돌아왔다. 어디로 갈까?\n\n"
            find_content = find_f
        elif keyword == '조사를그만둔다' :
            first_line = "조사를 그만두었다.\n\n"
            find_content = "<시스템계 포함 답멘 금지>"
        #전각
        elif keyword == '전각으로간다' :
            first_line = "전각에 도착했다. 어디부터 볼까?\n\n"
            find_content = find_j
        elif keyword == '전각1층을본다' :
            first_line = "스산한 분위기가 감돈다... \n설마... 유령?!\n\n"
            find_content = "- 전각 입구로 돌아간다\n- 1층을 더 찾아본다"
        elif keyword =='전각입구로돌아간다' :
            first_line = "자, 다시 어디를 볼까?\n\n"
            find_content = find_j
        elif keyword == '1층을더찾아본다' :
            i = randint(1,100)
            if i > 98 :
                first_line = '분명하다, 이 온도, 이 촉감... 열쇠다!\n\n'
                find_content = '<수갑 열쇠 발견>\n\n- 전각 입구로 돌아간다'
            elif i > 67 :
                first_line = '이건... 돈의 서늘함이었다!\n\n'
                find_content = '<엽전 1냥 발견>\n\n- 전각 입구로 돌아간다'               
            else :
                first_line = '...인가 싶었지만, 아무것도 없다.\n\n'
                find_content = '- 전각 입구로 돌아간다'
        elif keyword == '전각2층을본다' :
            first_line = '연못과 앞마당이 훤히 보인다.\n'
            i = randint(1,100)
            if i > 60 :
                first_line += '난간 위에 뭔가 반짝인다.\n\n'
                find_content = '- 반짝이는 것을 본다\n- 전각 입구로 돌아간다'
            else :
                first_line += '탁 트인 풍경이 보기 좋다...\n\n'
                find_content = '-풍경을 바라본다\n- 전각 입구로 돌아간다'
        elif keyword == '반짝이는것을본다' :
            i = randint(1,3)
            first_line = '앗 이건..?\n엽전이다! 어쩐지 반짝거리더라!\n\n'
            find_content = '<엽전 '+str(i)+'냥 발견>\n\n- 전각 입구로 돌아간다'
        elif keyword == '풍경을 바라본다' :
            first_line = '음... 마음이 편해졌다.\n\n'
            find_content = '- 전각 입구로 돌아간다'
        elif keyword == '계단을본다' :
            first_line = '전각 2층으로 올라가는 계단이다.\n\n'
            find_content = '- 올라가본다\n- 전각 입구로 돌아간다'
        elif keyword == '올라가본다' :
            i = randint(1,100)
            if i > 98 :
                first_line = '올라가다 성대하게 굴렀다!\n쿠당탕... 쿵탕...\n여기는 태초 마을? 이 아니라 불행 중 다행으로 열쇠다!\n\n'
                find_content = '<수갑 열쇠 발견>\n\n- 전각 입구로 돌아간다'
            elif i > 67 :
                j = randint(1,3)
                first_line = '앗, 계단 틈새에 엽전이 껴있다!'
                find_content = '<엽전 '+j+'냥 발견>\n\n- 전각 입구로 돌아간다'
            else :
                first_line = '휴! 2층까지 무사히 올라왔다!\n\n'
                find_content ='-전각 2층을 본다\n- 전각 입구로 돌아간다'

        #앞마당
        elif keyword == '앞마당으로간다' :
            first_line = "앞마당에 도착했다. 어디부터 볼까?\n\n"
            find_content = find_y
        elif keyword == '앞마당입구로돌아간다' :
            first_line = '자, 다시 어디를 볼까?\n\n'
            find_content = find_y
        
        #정자
        elif keyword == '정자로간다' :
            first_line = "정자에 도착했다. 어디부터 볼까?\n\n"
            find_content = find_z
        elif keyword == '정자입구로돌아간다' :
            first_line = "자, 다시 어디를 볼까?\n\n"
            find_content = find_z
        
        #연못
        elif keyword == '연못으로간다' :
            first_line = "연못에 도착했다. 어디부터 볼까?\n\n"
            find_content = find_w
        elif keyword == '연못입구로돌아간다' :
            first_line = "자, 다시 어디를 볼까?\n\n"
            find_content = find_w
            

        return first_line + find_content
    except:
        return '조사 장소를 잘못 입력한 듯 하오.'


def mk_reply_content(keyword_type, mention, keyword_ac_return) :
    global last_reply_id
    reply_to = "@" + mention.author.screen_name+" "
    now = datetime.datetime.now()
    print('행뽑, 불뽑 답멘 시행')
    nowdatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    lucky_reply = '행운뽑기 완료되었소.\n승정원을 확인하길 바라오.\n\n'
    unlucky_reply = '불운뽑기 완료되었소.\n승정원을 확인하길 바라오.\n\n'

    try:
        last_reply_id = mention.id_str
        if keyword_type == 2:
            keyword = '행운뽑기'
            reply_content = reply_to + lucky_reply + nowdatetime
        elif keyword_type == 3:
            keyword = '불운뽑기'
            reply_content = reply_to + unlucky_reply + nowdatetime
        print('만드는건 완료')
        api.update_status(reply_content, in_reply_to_status_id = mention.id_str)
        p = randint(0,person_len)
        print('행뽑, 불뽑 퍼블트 진행')
        public_reply = "누군가 " + keyword + "를 진행했습니다.\n"+person[p]+"가 "+keyword_ac_return+"에 당첨되었습니다.\n\n"+nowdatetime
        api.update_status(public_reply)
    except:
        print('행뽑/불뽑 답멘 오류')
        pass

    return

def reply_funtion(now_mention, make_return) :
    print('뽑기 외 답멘 실행')
    global last_reply_id
    reply_to = "@" + now_mention.author.screen_name+" "
    now = datetime.datetime.now()
    nowdatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    total_reply_content = reply_to + make_return +'\n\n' + nowdatetime
    print(total_reply_content)
    try:
        last_reply_id = now_mention.id_str
        api.update_status(total_reply_content, in_reply_to_status_id = now_mention.id_str)
    except:
        print("뽑기 외 답멘 에러")
        pass
    return

while True:
    check_new_mention()
    time.sleep(10)