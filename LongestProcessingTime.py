import random, sys, math, time

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
        #self.hour = []
        #self.minute = []
        self.timeLag = None
        self.operations = []

    #--------------------------------------------------------------------------------
    # Sets the times for the patient's operations
    # Chooses first operation to be as early as possible in the morning and the
    # second operation to be after the time lag
    #--------------------------------------------------------------------------------
    def setOperationValues(self):
        #Set first operation to be as early as possible
        self.operations.append(9.0)

        #Second operation is the first operation + 15 minutes for processing of first operation + time lag between operations
        secondOperation = self.operations[0] + 0.25 + self.timeLag

        self.operations.append(secondOperation)

        for i in range(len(self.operations)):
            print("O{} - Time: {}".format(i+1, self.operations[i]))

    #--------------------------------------------------------------------------------
    # Randomly chooses a time lag which will then be used to determine the time
    # of the patient's operations
    #--------------------------------------------------------------------------------
    def chooseTimeLag(self):
        if self.timeLag is None:
            hours = random.randint(0, 5)

            if hours == 5:
                minutes = random.randint(0, 2) * 0.25

            else:
                minutes = random.randint(0, 3) * 0.25

            self.timeLag = hours + minutes

        print("\n{}".format(self.timeLag))
        self.setOperationValues()

    #--------------------------------------------------------------------------------
    # Overwrites the patient operation times with new ones that don't clash with a
    # different patient's operation times in the machine's list
    #--------------------------------------------------------------------------------
    def overrideOperationValues(self, fixedOperation, otherOperation):
        self.operations.clear()

        if fixedOperation > otherOperation:
            self.operations.append(otherOperation)
            self.operations.append(fixedOperation)

        else:
            self.operations.append(fixedOperation)
            self.operations.append(otherOperation)

    #--------------------------------------------------------------------------------
    # Returns the operation times for the patient
    #--------------------------------------------------------------------------------
    def getOperations(self):
        return self.operations

    #--------------------------------------------------------------------------------
    # Returns the time lag required between the operations for the patient
    #--------------------------------------------------------------------------------
    def getDuration(self):
        return self.timeLag

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
    # Tries to shift the patient to see if the current machine can take on the operations.
    # If possible, returns true with values of new times otherwise returns false
    #--------------------------------------------------------------------------------
    def canShiftPatient(self, Patient, patientPos, operationPos):
        patientOperations = Patient.getOperations()
        machineOperations = []
        lastOperation = 14.75

        #Create lists of the machines patients for the day
        for i in range(len(self.machinePatients)):
            operations = self.machinePatients[i].getOperations()
            machineOperations.append(operations)

        clashOperation = patientOperations[operationPos] #time of the clash
        otherOperation = patientOperations[(operationPos + 1) % 2]
        clash = True

        while(clash):
            clashOperation += 0.25
            otherOperation += 0.25

            if clashOperation > lastOperation or otherOperation > lastOperation:
                break

            #Assume we have found a solution and check to see if so
            clash = False

            for i in range(len(machineOperations)):
                for j in range(len(machineOperations[i])):
                    #print("Checking times {} and {} to machine time {}".format(clashOperation, otherOperation, machineOperations[i][j]))
                    if (clashOperation == machineOperations[i][j]) or (otherOperation == machineOperations[i][j]):
                        #print("Clash at {}\n".format(machineOperations[i][j]))
                        clash = True
                        break #clash still found so try again

        #No solution found for this machine
        if clash:
            #print("No solution found, try next machine\n")
            return False, None, None #Cannot find a space for the patient so try next machine

        #print("Free times found at {} and {}\n".format(clashOperation, otherOperation))

        return True, clashOperation, otherOperation

    #--------------------------------------------------------------------------------
    # Checks to see if the machine has a free slot at the given patient time
    # Returns true if it does, false otherwise
    #--------------------------------------------------------------------------------
    def isFree(self, patient):
            patientOperations = patient.getOperations()

            for i in range(len(self.machinePatients)):
                machineOperations = self.machinePatients[i].getOperations()

                for j in range(len(patientOperations)):
                    if any(op == patientOperations[j] for op in machineOperations): #Either the morning or afternoon job clashes
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
        if list[j].getDuration() >= pivot.getDuration(): #Change inequality sign to reverse the list
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
# Tries to assign the patient to a machine, if possible it returns true
# otherwise it returns false
#--------------------------------------------------------------------------------
def assignPatientToMachine(machine, patient):
    free, scheduledPatientPos, operationPos = machine.isFree(patient)

    if free:
        machine.addPatient(patient)

    else:
        free, fixedOperation, otherOperation = machine.canShiftPatient(patient, scheduledPatientPos, operationPos)

        if free:
            patient.overrideOperationValues(fixedOperation, otherOperation)
            machine.addPatient(patient)
            #print("Added patient\n")

    return free

#----------------------------------------------------------------------------
#                           MAIN METHOD
#----------------------------------------------------------------------------
def main():
    startTime = time.time()
    numPatients = 10
    numMachines = 1
    dayPatients = []
    dayMachines = []

    #Override the default values for the number of patients and the number of machines
    #Also can read the first argument as a text file and parse it for testing
    if len(sys.argv) > 1:
        if isinstance(sys.argv[1], int):
            numPatients = int(sys.argv[1])

        elif isinstance(sys.argv[1], str):
            with open(sys.argv[1], 'r') as f:
                contents = f.read().split(',')

                for i in range(len(contents)):
                        p = Patient()
                        p.timeLag = (float(contents[i]))
                        dayPatients.append(p)

    if len(sys.argv) > 2:
        numMachines = int(sys.argv[2])

    for i in range(numPatients):
        if len(dayPatients) < numPatients:
            dayPatients.append(Patient()) #Add patient to the list of total patients for the day

        dayPatients[i].chooseTimeLag()

    for i in range(numMachines):
        dayMachines.append(Machine()) #Add machine to the list of total machines for the day

    quickSort(dayPatients, 0, len(dayPatients) - 1) #Sort patients by the time lag decreasing

    #for i in range(len(dayPatients)):
        #hours, minutes = dayPatients[i].getJobs()
        #print("----------------- Patient {} -----------------".format(i+1))
        #for j in range(len(hours)):
            #print("J{} H: {} M: {}".format(j+1, hours[j], minutes[j]))

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
        j = i % numMachines
        curMachine = dayMachines[j]

        success = assignPatientToMachine(curMachine, dayPatients[i])
        k = j

        while not success:
            k += 1
            k = k % numMachines

            if j == k:
                break

            success = assignPatientToMachine(dayMachines[k], dayPatients[i])

        if not success:
            #Cannot be scheduled with any nurse so try contract nurses (if there are any)
            if len(dayMachines) > numMachines:
                k = numMachines #First contract nurse

                success = assignPatientToMachine(dayMachines[k], dayPatients[i])

                while not success:
                    k += 1

                    if k == len(dayMachines):
                        break

                    success = assignPatientToMachine(dayMachines[k], dayPatients[i])

                if not success:
                    dayMachines.append(Machine())
                    assignPatientToMachine(dayMachines[-1], dayPatients[i])
                    #print("Created new machine and added patient")

            else:
                dayMachines.append(Machine())
                assignPatientToMachine(dayMachines[-1], dayPatients[i])

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
                operations = machine.getPatients()[j].getOperations()
                print("O{} T: {}".format(k+1, operations[k]))
            print("")

    endTime = time.time()
    duration = endTime - startTime
    print("Duration of heuristic: {} seconds".format(duration))

if __name__ == '__main__':
    main()
