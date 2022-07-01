from Get_race_time import Get_race_time
from Buy_boat import Input_schedule
#自動売買のメイン関数
if __name__ == '__main__':
    #今日がどこのレースで何時からか行うかとってくる。
    race_time = Get_race_time()

    #日にちをもとに自動売買を行う
    Input_schedule(race_time)