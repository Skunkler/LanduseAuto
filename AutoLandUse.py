
#Tool written by Warren Kunkler to help automate the landuse data. The input readFile
#is the result of running test.sql. This pulls most of the attributes that are found within
#the Water Plan Packet and adds them to the landuse feature class. 
import os, shutil, arcpy





class GetRecordedValues:
    MonthDict = {'Jan':'01', 'Feb':'02','Mar':'03', 'Apr':'04', 'May':'05', \
             'Jun':'06', 'Jul':'07', 'Aug':'08'\
             , 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    #our constructor that reads the result of the sql queries and initializes an empty list
    def __init__(self, inFile):
        self.__ListPL_IDs = []
        self.readFile = open(inFIle, "r")
        
    #Get vals takes each record, decodes it, and adds the value to that records within the landuse feature class    
    def _getVals(ListRecord):
        LANDUSE_ID = int(ListRecord[0])
        PROJECT_NO = int(ListRecord[1])
        REVDATE = ListRecord[2]
        #print type(REVDATE.split('-')[1]
        if len(REVDATE.split('-')) > 1 and REVDATE.split('-')[1] in MonthDict.keys():
            finalRevDate = GetRecordedValues.MonthDict[REVDATE.split('-')[1]] + '/' + REVDATE.split('-')[0] + '/' + REVDATE.split('-')[2]
        elif len(REVDATE.split('-')) == 1:
            finalRevDate = '01/01/1899'

        REVENG = ListRecord[3]

        if ListRecord[4].isdigit() == False:
            ONFF_GPM = 0
        else:
            ONFF_GPM = int(ListRecord[4])

        if ListRecord[5].isdigit() == False:
            OFFF_GPM = 0
        else:
            OFFF_GPM = int(ListRecord[5])
            

        PZONE = int(ListRecord[6])
        Name = ListRecord[7]
        print LANDUSE_ID, PROJECT_NO, finalRevDate, REVENG, ONFF_GPM, OFFF_GPM, PZONE, Name

        arcpy.SelectLayerByAttribute_management('lyr', 'NEW_SELECTION', "LANDUSE_ID = " + str(LANDUSE_ID))

        arcpy.CalculateField_management('lyr', 'LANDUSE_ID', LANDUSE_ID, 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'PROJID', PROJECT_NO, 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'REVDATE', '"' + finalRevDate +'"', 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'REVENG', REVENG, 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'ONFF_GPM', ONFF_GPM, 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'OFFFF_GPM', OFFF_GPM, 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'PZONE', PZONE, 'PYTHON_9.3')
        arcpy.CalculateField_management('lyr', 'PROJ_NAME', '"' + Name.strip() + '"', 'PYTHON_9.3')
        arcpy.SelectLayerByAttribute_management('lyr', 'CLEAR_SELECTION')

    #Call lines reads the result sql query file and calls the getVals function on each of them
    def _CallLines():
        lines = self.readFile()
        count = 0
        for line in lines:
            if count >= 3 and int(line.split(',')[0]) in self.__ListPL_IDs:
                self._getVals(line.split(',')[0])
            else:
                count += 1

    #This method is the only public method, the others are protected
    #This method loops through the feature class and appends the PL_ID within each feature
    #and calls the callLines method when complete
    def CollectPL_IDs(Fc):
        arcpy.MakeFeatureLayer_management(Fc, 'lyr')
        with arcpy.da.SearchCursor("lyr", "LANDUSE_ID") as cursor:
            for row in cursor:
                self.__ListPL_IDs.append(row[0])
        self._CallLines()


readFile = r"D:\LandUseEdit\testrun2.csv"

FC = r'D:\LandUseEdit\Test.gdb\testrun4'
        
GetLandRecordsObj = GetRecordedValues(readFile)
GetLandRecordsObj.CollectPL_IDs(FC)



