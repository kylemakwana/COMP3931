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

    #---------------------------------------------

    #EXPAND UPON THIS TRYING TO CHANGE TIME AND MOVE PATIENTS ABOUT

    #---------------------------------------------
    def isFree(self, Patient):
        patientHours, patientMinutes = Patient.getJobs()

        for i in range(len(self.machinePatients)):
            machineHours[i], machineMinutes[i] = self.machinePatients[i].getJobs()

            for j in range(0, 2):
                if(patientHours[j] == machineHours[j] and patientMinutes[j] == machineMinutes[j]):
                    return False

        return True

    def numPatients(self):
        return len(self.machinePatients)

    def addPatient(self, Patient):
        numberOfPatients = self.numPatients()
        self.machinePatients.append(Patient)

    def getPatients(self):
        return self.machinePatients

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

for i in range(numMachines):
    curMachine = dayMachines[i]

    if curMachine.isFree(dayPatients[i]):
        curMachine.addPatient(dayPatients[i]);

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
