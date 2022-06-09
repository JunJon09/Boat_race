from scraping import scarpe
import pickle
if __name__ == '__main__':
    #スクレピング
    #scarpe()
    with open('boat-tsu.binaryfile', 'rb') as web:
        boat_tsu = pickle.load(web)
        print(boat_tsu)   

    
   
    
     