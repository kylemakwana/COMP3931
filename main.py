import random, sys

class Patient(object):
    def __init__(self):
        self.hour = []
        self.minute = []

    def setJobValues(self):
        self.hour.append(random.randint(9, 11))
        self.minute.append(random.randint(0, 3) * 15)

        self.hour.append(random.randint(12, 14))
        self.minute.append(random.randint(0, 3) * 15)

    def getJobs(self):
        return self.hour, self.minute

    def getDuration(self):
        totalHours = self.hour[-1] - self.hour[0]
        totalMinutes = self.minute[-1] - self.minute[0]

        if(totalMinutes < 0):
            totalHours -= 1
            totalMinutes = 60 + totalMinutes

        total = totalHours + (totalMinutes/60.0)
        return total

class Machine(object):
    def __init__(self):
        self.machinePatients = []

    def canShiftPatient(self, Patient, patientPos, jobPos):
        patientHours, patientMinutes = Patient.getJobs()
        machineHours, machineMinutes = [], []

        #Create lists of the machines patients for the day
        for i in range(len(self.machinePatients)):
            hours, minutes = self.machinePatients[i].getJobs()
            machineHours.append(hours)
            machineMinutes.append(minutes)

        clashHour, clashMinute = machineHours[patientPos][jobPos], machineMinutes[patientPos][jobPos] #hour and minute of clash
        clash = True

        if clashHour < 12:  #clash happens in the morning
            maxHour = 11
            minHour = 9
        else:               #clash happens in the afternoon
            maxHour = 2
            minHour = 12

        #Try going backwards to fix clash and fit into machine timetable
        while(clash):
            clashMinute -= 15
            if clashMinute < 0:
                clashMinute = 45
                clashHour -= 1

            if clashHour < minHour:
                break

            #Solution found
            if not any((hour == clashHour for hour in machineHours) and (minute == clashMinute for minute in machineMinutes)):
                print("Solution found going backwards:")
                clash = False

        if not clash:
            print("{}:{}".format(clashHour, clashMinute))
            return True, clashHour, clashMinute

        #Reset values back
        clashHour, clashMinute = machineHours[patientPos][jobPos], machineMinutes[patientPos][jobPos] #reset the values since we couldn't find a space in one direction

        #No solution found going backwards so try going forwards instead
        if clash:
            while(clash):
                clashHour += 15
                if clashMinute == 60:
                    clashMinute = 0
                    clashHour += 1

                if clashHour > maxHour:
                    break

                #Solution found
                if not any((hour == clashHour for hour in machineHours) and (minute == clashMinute for minute in machineMinutes)):
                    print("Solution found going forwards:")
                    clash = False

            #No solution found for this machine
            if clash:
                print("No solution found, try next machine")
                return False #Cannot find a space for the patient so try next machine

            print("{}:{}".format(clashHour, clashMinute))
            return True, clashHour, clashMinute

    def isFree(self, Patient):
        patientHours, patientMinutes = Patient.getJobs()
        i = 0

        for i in range(len(self.machinePatients)):
            machineHours, machineMinutes = self.machinePatients[i].getJobs()
            j = 0

            for j in range(len(patientHours)):
                if patientHours[j] == machineHours[j] and patientMinutes[j] == machineMinutes[j]:
                    print("CLASH ---- J{} ---- PH: {} PM: {} MH: {} MM: {}".format(j+1, patientHours[j], patientMinutes[j], machineHours[j], machineMinutes[j]))

                    if j == 0:
                        print("J{} ---- PH: {} PM: {} MH: {} MM: {}".format(j+1, patientHours[j+1], patientMinutes[j+1], machineHours[j+1], machineMinutes[j+1]))

                    else:
                        print("J{} ---- PH: {} PM: {} MH: {} MM: {}".format(j, patientHours[j-1], patientMinutes[j-1], machineHours[j-1], machineMinutes[j-1]))

                    print("\nTrying to fix clash...")
                    canShift, newHour, newMinute = self.canShiftPatient(Patient, i, j)

                    if canShift:
                        print("FIXED")
                        print("old time -- {}:{}".format(Patient.hour[j], Patient.minute[j]))
                        Patient.hour[j] = newHour
                        Patient.minute[j] = newMinute

                        print("new time -- {}:{}".format(Patient.hour[j], Patient.minute[j]))
                        return True

                    return False

        return True

    def numPatients(self):
        return len(self.machinePatients)

    def addPatient(self, Patient):
        numberOfPatients = self.numPatients()
        self.machinePatients.append(Patient)
        self.sortPatients(0)

    def getPatients(self):
        return self.machinePatients

    #----------------------------------------------------------------------------
    #Sort out patients trying to move them all to be from 9 - 12
    #Check to see if possible (afternoon job may be before 12, not allowed!)
    #----------------------------------------------------------------------------
    def sortPatients(self, job):
        machineHours, machineMinutes = [], []
        for i in range(len(self.machinePatients)):
            tempH, tempM = self.machinePatients[i].getJobs()
            machineHours.append(tempH)
            machineMinutes.append(tempM)

        for i in range(len(self.machinePatients)):
            print("J1 -- {}:{}, J2 -- {}:{}".format(machineHours[i][0], machineMinutes[i][0], machineHours[i][1], machineMinutes[i][1]))
            #while()



def partition(list, low, high):
    i = low - 1
    pivot = list[high]

    for j in range(low, high):
        if list[j].getDuration() >= pivot.getDuration(): #Change inequality sign to reverse the list
            i = i + 1
            list[i], list[j] = list[j], list[i]

    list[i+1], list[high] = list[high], list[i+1]
    return (i + 1)

#Sorts the patients out into descending order of length of time required
def quickSort(list, low, high):
    if low < high:
        pi = partition(list, low, high)

        quickSort(list, low, pi - 1)
        quickSort(list, pi + 1, high)

# --------------------------------------------------
#                    MAIN METHOD
# --------------------------------------------------
numPatients = 10
numMachines = 2
dayPatients = []
dayMachines = []

#Override the default values for the number of patients and the number of machines
if len(sys.argv) > 1:
    numPatients = int(sys.argv[1])

if len(sys.argv) > 2:
    numMachines = int(sys.argv[2])

i = 0

for i in range(numPatients):
    dayPatients.append(Patient()) #Add patient to the list of total patients for the day
    dayPatients[i].setJobValues() #Create the times for the patient

for i in range(numMachines):
    dayMachines.append(Machine()) #Add machine to the list of total machines for the day

quickSort(dayPatients, 0, numPatients - 1)

for i in range(numPatients):
    j = i % numMachines
    curMachine = dayMachines[j]

    if curMachine.isFree(dayPatients[i]):
        curMachine.addPatient(dayPatients[i]);

    else:
        #curMachine.canShiftPatient
        #j = i
        print("Cannot add there is a clash")

for i in range(numMachines):
    machine = dayMachines[i]
    print("----------------- Machine {} -----------------".format(i+1))
    j = 0

    for j in range(machine.numPatients()):
        print("----------------- Patient {} -----------------".format(j+1))
        k = 0

        for k in range(2):
            hours, minutes = machine.getPatients()[j].getJobs()
            print("J: {} H: {} M: {}".format(k+1, hours[k], minutes[k]))
        print("")
