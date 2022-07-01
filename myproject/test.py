from os import rename


def a():
    try:
        a = 1
        for i in range(20):
            if i==1 or i==3 or i==5 or i==10:
                print(i)
    except Exception as e:
        print(e)
        print('knrgk')
    else:
        print(a)
        
        
        
        

if __name__ == '__main__':
    a() 