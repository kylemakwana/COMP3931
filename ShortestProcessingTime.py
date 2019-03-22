import random, sys

#--------------------------------------------------------------------------------
#
#                           PATIENT CLASS
#
#--------------------------------------------------------------------------------

class Patient(object):
    #--------------------------------------------------------------------------------
    # Initialises the patient with an empty hour list and an empty minute list
    #--------------------------------------------------------------------------------
    def __init__(self):
        self.hour = []
        self.minute = []

    #--------------------------------------------------------------------------------
    # Randomly chooses the times for the patients jobs
    # Chooses a job for the morning and a job for the afternoon
    #--------------------------------------------------------------------------------
    def setJobValues(self):
        self.hour.append(random.randint(9, 11))
        self.minute.append(random.randint(0, 3) * 15)

        self.hour.append(random.randint(12, 14))
        self.minute.append(random.randint(0, 3) * 15)

    #--------------------------------------------------------------------------------
    # Overwrites the patient job times with new ones that don't clash with a
    # different patient's job times in the machine's list
    #--------------------------------------------------------------------------------
    def overrideJobValues(self, firstJobHour, firstJobMin, secJobHour, secJobMin):
        self.hour[0], self.minute[0] = firstJobHour, firstJobMin
        self.hour[1], self.minute[1] = secJobHour, secJobMin

    #--------------------------------------------------------------------------------
    # Returns the jobs for the patient
    #--------------------------------------------------------------------------------
    def getJobs(self):
        return self.hour, self.minute

    #--------------------------------------------------------------------------------
    # Returns the duration of time required for the jobs of the patient
    #--------------------------------------------------------------------------------
    def getDuration(self):
        totalHours = self.hour[-1] - self.hour[0]
        totalMinutes = self.minute[-1] - self.minute[0]

        if(totalMinutes < 0):
            totalHours -= 1
            totalMinutes = 60 + totalMinutes

        total = totalHours + (totalMinutes/60.0)
        return total

#--------------------------------------------------------------------------------
#
#                           MACHINE CLASS
#
#--------------------------------------------------------------------------------

class Machine(object):
    #--------------------------------------------------------------------------------
    # Initialises the machine with an empty list of assigned patients
    #--------------------------------------------------------------------------------
    def __init__(self):
        self.machinePatients = []

    #--------------------------------------------------------------------------------
    # Tries to shift the patient to see if the current machine can take on the job.
    # If possible, returns true with values of new times otherwise returns false
    #--------------------------------------------------------------------------------
    def canShiftPatient(self, Patient, patientPos, jobPos):
        patientHours, patientMinutes = Patient.getJobs()
        machineHours, machineMinutes = [], []

        #Create lists of the machines patients for the day
        for i in range(len(self.machinePatients)):
            hours, minutes = self.machinePatients[i].getJobs()
            machineHours.append(hours)
            machineMinutes.append(minutes)

        clashHour, clashMinute = machineHours[patientPos][jobPos], machineMinutes[patientPos][jobPos] #hour and minute of clash
        otherHour, otherMinute = machineHours[patientPos][(jobPos + 1) % 2], machineMinutes[patientPos][(jobPos + 1) % 2]
        clash = True

        if clashHour < 12:  #clash happens in the morning
            maxHour = 11
            otherMaxHour = 14
        else:               #clash happens in the afternoon
            maxHour = 14
            otherMaxHour = 11

        while(clash):
            clashMinute += 15
            otherMinute += 15

            if clashMinute == 60:
                clashMinute = 0
                clashHour += 1

            if otherMinute == 60:
                otherMinute = 0
                otherHour += 1

            if clashHour > maxHour or otherHour > otherMaxHour:
                break

            #Assume we have found a solution and check to see if so
            clash = False

            for i in range(len(machineHours)):
                for j in range(len(machineHours[i])):
                    #print("Checking time {}:{} to machine time {}:{}".format(clashHour, clashMinute, machineHours[i][j], machineMinutes[i][j]))
                    if clashHour == machineHours[i][j] and clashMinute == machineMinutes[i][j]:
                        #print("Clash at {}:{}".format(machineHours[i][j], machineMinutes[i][j]))
                        clash = True
                        break #clash still found so try again

        #No solution found for this machine
        if clash:
            #print("No solution found, try next machine")
            return False, None, None, None, None #Cannot find a space for the patient so try next machine

        #print("Free time found at {}:{}".format(clashHour, clashMinute))

        if clashHour < 12:
            return True, clashHour, clashMinute, otherHour, otherMinute

        #Afternoon clash so return values in other order
        return True, otherHour, otherMinute, clashHour, clashMinute

    #--------------------------------------------------------------------------------
    # Checks to see if the machine has a free slot at the given patient time
    # Returns true if it does, false otherwise
    #--------------------------------------------------------------------------------
    def isFree(self, patient):
            patientHours, patientMinutes = patient.getJobs()

            for i in range(len(self.machinePatients)):
                machineHours, machineMinutes = self.machinePatients[i].getJobs()

                for j in range(len(patientHours)):
                    if patientHours[j] == machineHours[j] and patientMinutes[j] == machineMinutes[j]: #Either the morning or afternoon job clashes
                        #print("CLASH ---- J{} ---- PH: {} PM: {} MH: {} MM: {}".format(j+1, patientHours[j], patientMinutes[j], machineHours[j], machineMinutes[j]))

                        #if j == 0:
                            #print("J{} ---- PH: {} PM: {} MH: {} MM: {}".format(j+1, patientHours[j+1], patientMinutes[j+1], machineHours[j+1], machineMinutes[j+1]))

                        #else:
                            #print("J{} ---- PH: {} PM: {} MH: {} MM: {}".format(j, patientHours[j-1], patientMinutes[j-1], machineHours[j-1], machineMinutes[j-1]))

                        return False, i, j

            return True, None, None

    #--------------------------------------------------------------------------------
    # Returns the number of patients assigned to the machine
    #--------------------------------------------------------------------------------
    def numPatients(self):
        return len(self.machinePatients)

    #--------------------------------------------------------------------------------
    # Adds the patient to the end of the machine's list
    #--------------------------------------------------------------------------------
    def addPatient(self, Patient):
        numberOfPatients = self.numPatients()
        self.machinePatients.append(Patient)

    #--------------------------------------------------------------------------------
    # Returns the list of patients assigned to the machine
    #--------------------------------------------------------------------------------
    def getPatients(self):
        return self.machinePatients

#--------------------------------------------------------------------------------
#
#                           MAIN FUNCTIONS
#
#--------------------------------------------------------------------------------
def partition(list, low, high):
    i = low - 1
    pivot = list[high]

    for j in range(low, high):
        if list[j].getDuration() <= pivot.getDuration(): #Change inequality sign to reverse the list
            i = i + 1
            list[i], list[j] = list[j], list[i]

    list[i+1], list[high] = list[high], list[i+1]
    return (i + 1)

#--------------------------------------------------------------------------------
# Sorts the patients out into descending order of length of time required
#--------------------------------------------------------------------------------
def quickSort(list, low, high):
    if low < high:
        pi = partition(list, low, high)

        quickSort(list, low, pi - 1)
        quickSort(list, pi + 1, high)

#--------------------------------------------------------------------------------
# Sort out patients trying to move them all to be from 9 - 12 or as early as
# possible if restricted by afternoon time
#--------------------------------------------------------------------------------
def sortPatientTimes(patients):
    for i in range(len(patients)):
        curPatient = patients[i]
        tempHours, tempMinutes = curPatient.getJobs()

        while not((tempHours[0] == 9 and tempMinutes[0] == 0) or (tempHours[1] == 12 and tempMinutes[1] == 0)): #Jobs can be moved, not at the minimum
            tempMinutes[0] -= 15
            tempMinutes[1] -= 15

            if tempMinutes[0] < 0:
                tempMinutes[0] = 45
                tempHours[0] -= 1

            if tempMinutes[1] < 0:
                tempMinutes[1] = 45
                tempHours[1] -= 1

        curPatient.overrideJobValues(tempHours[0], tempMinutes[0], tempHours[1], tempMinutes[1])

#--------------------------------------------------------------------------------
# Tries to assign the patient to a machine, if possible it returns true
# otherwise it returns false
#--------------------------------------------------------------------------------
def assignPatientToMachine(machine, patient):
    free, scheduledPatientPos, jobPos = machine.isFree(patient)

    if free:
        machine.addPatient(patient)
        #print("Added patient")

    else:
        free, fixedJobHour, fixedJobMin, otherJobHour, otherJobMin = machine.canShiftPatient(patient, scheduledPatientPos, jobPos)

        if free:
            #print("Shift possible, updating times")
            patient.overrideJobValues(fixedJobHour, fixedJobMin, otherJobHour, otherJobMin)
            #print("Times updated")
            machine.addPatient(patient)
            #print("Added patient")

    return free

#----------------------------------------------------------------------------
#                           MAIN METHOD
#----------------------------------------------------------------------------
numPatients = 10
numMachines = 2
dayPatients = []
dayMachines = []
text = ""

#Override the default values for the number of patients and the number of machines
#Also can read the first argument as a text file and parse it for testing
if len(sys.argv) > 1:
    if isinstance(sys.argv[1], int):
        numPatients = int(sys.argv[1])

    elif isinstance(sys.argv[1], str):
        text = sys.argv[1]
        numPatients = 0

        with open(text, 'r') as f:
            contents = f.read().split(',')
            #print(contents)
            i = 0
            while i < len(contents):
                if i % 4 == 0:
                    p = Patient()
                    p.hour.append(int(contents[i]))

                elif i % 4 == 1:
                    p.minute.append(int(contents[i]))

                elif i % 4 == 2:
                    p.hour.append(int(contents[i]))

                else:
                    p.minute.append(int(contents[i]))
                    #print(p.hour)
                    #print(p.minute)
                    dayPatients.append(p)
                i += 1

if len(sys.argv) > 2:
    numMachines = int(sys.argv[2])

for i in range(numPatients):
    dayPatients.append(Patient()) #Add patient to the list of total patients for the day
    dayPatients[i].setJobValues() #Create the times for the patient

for i in range(numMachines):
    dayMachines.append(Machine()) #Add machine to the list of total machines for the day

quickSort(dayPatients, 0, numPatients - 1) #Sort patients by the total length of jobs decreasing

#for i in range(len(dayPatients)):
    #hours, minutes = dayPatients[i].getJobs()
    #print("----------------- Patient {} -----------------".format(i+1))
    #for j in range(len(hours)):
        #print("J{} H: {} M: {}".format(j+1, hours[j], minutes[j]))

sortPatientTimes(dayPatients)

#----------------------------------------------------------------------------
# Works but need to see if possible to balance machine workload
#
# Currently if one machine cant take job but next can it is given to the next
# machine but, we then see if the next machine can take the new job it was
# originally suppose to have.
#
# First check to see if previous machine can take the new job to try and
# help balance the workload.
#----------------------------------------------------------------------------
for i in range(len(dayPatients)):
    j = i % len(dayMachines)
    curMachine = dayMachines[j]

    success = assignPatientToMachine(curMachine, dayPatients[i])
    k = j

    while not success:
        k += 1
        k = k % len(dayMachines)

        if j == k:
            break

        success = assignPatientToMachine(dayMachines[k], dayPatients[i])

    if not success:
        #print("Could not find a free machine, create a new one")
        dayMachines.append(Machine())
        assignPatientToMachine(dayMachines[-1], dayPatients[i])
        #print("Created new machine and added patient")

for i in range(len(dayMachines)):
    machine = dayMachines[i]
    if i+1 > numMachines:
        print("----------------- Contract Nurse {} -----------------".format(i+1 - numMachines))

    else:
        print("----------------- Nurse {} -----------------".format(i+1))

    j = 0

    for j in range(machine.numPatients()):
        print("----------------- Patient {} -----------------".format(j+1))
        k = 0

        for k in range(2):
            hours, minutes = machine.getPatients()[j].getJobs()
            print("J{} H: {} M: {}".format(k+1, hours[k], minutes[k]))
        print("")
