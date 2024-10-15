import os, json

dir_path = os.path.dirname(os.path.realpath(__file__))
DataFolderPath = os.path.join(dir_path, 'GameData')
DataStoreFile = os.path.join(DataFolderPath,'UserSaveData')

class Data:
    def __init__(self):
        self.DataSet = {"Bananas": 0,
                        "BananasPerClick": 1,
                        "BananasPerSecond": 0,
                        "MonkeyCost": 15,
                        "MonkeyAmount": 0,
                        "BananaFarmCost": 100,
                        "BananaFarmAmount": 0,
                        "BananaMineCost": 1000,
                        "BananaMineAmount": 0,
                        "MonkeyVillageCost": 3000,
                        "MonkeyVillageAmount": 0,
                        "BananaShipmentCost": 15000,
                        "BananaShipmentAmount": 0,
                        "MonkeyWizardCost": 50000,
                        "MonkeyWizardAmount": 0,
                        "BananaFactoryCost": 150000,
                        "BananaFactoryAmount": 0,
                        #add more here
                        "BananaGalaxyCost": 20000000,
                        "BananaGalaxyAmount": 0,
                        #add more here
                        "BananaBigBangCost": 75000000000,
                        "BananaBigBangAmount": 0,
                        #add more here
                        }

    def WriteData(self):
        DataStoreFileOpened = open(str(DataStoreFile)+'.txt','a')

        json.dump(self.DataSet,DataStoreFileOpened)

    def UpdateData(self, Data):
        DataStoreFileOpened = open(str(DataStoreFile)+'.txt','a')
        json.dump(Data, DataStoreFileOpened)

    def ReadData(self):
        path = str(DataStoreFile+".txt")
        f = open(path,)
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return self.WriteData()
    

def UnpackData():
    #while True:
    if not os.path.exists(DataFolderPath):
        os.makedirs(DataFolderPath)
    else:
        if not os.path.exists(str(DataStoreFile+".txt")):
            temp = open(str(DataStoreFile)+'.txt', 'w')
            temp.close()
            Data().WriteData()

        data = Data()
        DataSet = data.DataSet
        UserData = data.ReadData()

        if UserData == "":
            data.WriteData()

        try:
            if len(UserData) == len(DataSet):
                return UserData
            else:
                for item in DataSet:
                    if not item in UserData:
                        UserData[item] = DataSet[item]
                data.UpdateData(UserData)
                return UserData
        except TypeError:
            return(data.ReadData())

    
def WriteDataToFile(data):
    File = open(str(DataStoreFile)+'.txt','w')
    File.write(str(data).replace("'",'"'))
    File.close()

if __name__ == "__main__":
    print(UnpackData())