import random
import sys
import time

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

        #for i in range(len(self.operations)):
            #print("O{} - Time: {}".format(i+1, self.operations[i]))

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

        #print("\n{}".format(self.timeLag))
        self.setOperationValues()

    #--------------------------------------------------------------------------------
    # Overwrites the patient operation times with new ones that don't clash with a
    # different patient's operation times in the nurse's list
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
#                           NURSE CLASS
#
#--------------------------------------------------------------------------------

class Nurse(object):
    #--------------------------------------------------------------------------------
    # Initialises the nurse with an empty list of assigned patients
    #--------------------------------------------------------------------------------
    def __init__(self):
        self.nursePatients = []

    #--------------------------------------------------------------------------------
    # Tries to shift the patient to see if the current nurse can take on the operations.
    # If possible, returns true with values of new times otherwise returns false
    #--------------------------------------------------------------------------------
    def canShiftPatient(self, Patient, patientPos, operationPos):
        patientOperations = Patient.getOperations()
        nurseOperations = []
        lastOperation = 14.75

        #Create lists of the nurses patients for the day
        for i in range(len(self.nursePatients)):
            operations = self.nursePatients[i].getOperations()
            nurseOperations.append(operations)

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

            for i in range(len(nurseOperations)):
                for j in range(len(nurseOperations[i])):
                    #print("Checking times {} and {} to nurse time {}".format(clashOperation, otherOperation, nurseOperations[i][j]))
                    if (clashOperation == nurseOperations[i][j]) or (otherOperation == nurseOperations[i][j]):
                        #print("Clash at {}\n".format(nurseOperations[i][j]))
                        clash = True
                        break #clash still found so try again

        #No solution found for this nurse
        if clash:
            #print("No solution found, try next nurse\n")
            return False, None, None #Cannot find a space for the patient so try next nurse

        #print("Free times found at {} and {}\n".format(clashOperation, otherOperation))

        return True, clashOperation, otherOperation

    #--------------------------------------------------------------------------------
    # Checks to see if the nurse has a free slot at the given patient time
    # Returns true if it does, false otherwise
    #--------------------------------------------------------------------------------
    def isFree(self, patient):
            patientOperations = patient.getOperations()

            for i in range(len(self.nursePatients)):
                nurseOperations = self.nursePatients[i].getOperations()

                for j in range(len(patientOperations)):
                    if any(op == patientOperations[j] for op in nurseOperations): #Either the morning or afternoon job clashes
                        return False, i, j

            return True, None, None

    #--------------------------------------------------------------------------------
    # Returns the number of patients assigned to the nurse
    #--------------------------------------------------------------------------------
    def numPatients(self):
        return len(self.nursePatients)

    #--------------------------------------------------------------------------------
    # Adds the patient to the end of the nurse's list
    #--------------------------------------------------------------------------------
    def addPatient(self, Patient):
        numberOfPatients = self.numPatients()
        self.nursePatients.append(Patient)

    #--------------------------------------------------------------------------------
    # Returns the list of patients assigned to the nurse
    #--------------------------------------------------------------------------------
    def getPatients(self):
        return self.nursePatients

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
# Tries to assign the patient to a nurse, if possible it returns true
# otherwise it returns false
#--------------------------------------------------------------------------------
def assignPatientToNurse(nurse, patient):
    free, scheduledPatientPos, operationPos = nurse.isFree(patient)

    if free:
        nurse.addPatient(patient)

    else:
        free, fixedOperation, otherOperation = nurse.canShiftPatient(patient, scheduledPatientPos, operationPos)

        if free:
            patient.overrideOperationValues(fixedOperation, otherOperation)
            nurse.addPatient(patient)
            #print("Added patient\n")

    return free

#----------------------------------------------------------------------------
#                           MAIN METHOD
#----------------------------------------------------------------------------
def main():
    startTime = time.time()
    numPatients = 10
    numNurses = 1
    dayPatients = []
    dayNurses = []

    #Override the default values for the number of patients and the number of nurses
    #Also can read the first argument as a text file and parse it for testing
    if len(sys.argv) > 1:
        try:
            int(sys.argv[1])
            numPatients = int(sys.argv[1])

        except ValueError:
            with open(sys.argv[1], 'r') as f:
                contents = f.read().split(',')

                for i in range(len(contents)):
                    p = Patient()
                    l = float(contents[i])

                    if l > 5.5:
                        l = 5.5

                    p.timeLag = (l)
                    dayPatients.append(p)

                numPatients = len(dayPatients)

    if len(sys.argv) > 2:
        numNurses = int(sys.argv[2])

    for i in range(numPatients):
        if len(dayPatients) < numPatients:
            dayPatients.append(Patient()) #Add patient to the list of total patients for the day

        dayPatients[i].chooseTimeLag()

    for i in range(numNurses):
        dayNurses.append(Nurse()) #Add nurse to the list of total nurses for the day

    quickSort(dayPatients, 0, len(dayPatients) - 1) #Sort patients by the time lag decreasing

    #for i in range(len(dayPatients)):
        #hours, minutes = dayPatients[i].getJobs()
        #print("----------------- Patient {} -----------------".format(i+1))
        #for j in range(len(hours)):
            #print("J{} H: {} M: {}".format(j+1, hours[j], minutes[j]))

    #----------------------------------------------------------------------------
    # Works but need to see if possible to balance nurse workload
    #
    # Currently if one nurse cant take job but next can it is given to the next
    # nurse but, we then see if the next nurse can take the new job it was
    # originally suppose to have.
    #
    # First check to see if previous nurse can take the new job to try and
    # help balance the workload.
    #----------------------------------------------------------------------------
    for i in range(len(dayPatients)):
        j = i % numNurses
        curNurse = dayNurses[j]

        success = assignPatientToNurse(curNurse, dayPatients[i])
        k = j

        while not success:
            k += 1
            k = k % numNurses

            if j == k:
                break

            success = assignPatientToNurse(dayNurses[k], dayPatients[i])

        if not success:
            #Cannot be scheduled with any nurse so try contract nurses (if there are any)
            if len(dayNurses) > numNurses:
                k = numNurses #First contract nurse

                success = assignPatientToNurse(dayNurses[k], dayPatients[i])

                while not success:
                    k += 1

                    if k == len(dayNurses):
                        break

                    success = assignPatientToNurse(dayNurses[k], dayPatients[i])

                if not success:
                    dayNurses.append(Nurse())
                    assignPatientToNurse(dayNurses[-1], dayPatients[i])
                    #print("Created new nurse and added patient")

            else:
                dayNurses.append(Nurse())
                assignPatientToNurse(dayNurses[-1], dayPatients[i])

    endTime = time.time()
    duration = endTime - startTime

    for i in range(len(dayNurses)):
        nurse = dayNurses[i]
        if i+1 > numNurses:
            print("----------------- Contract Nurse {} -----------------".format(i+1 - numNurses))

        else:
            print("----------------- Nurse {} -----------------".format(i+1))

        j = 0

        for j in range(nurse.numPatients()):
            print("----------------- Patient {} -----------------".format(j+1))
            k = 0

            for k in range(2):
                operations = nurse.getPatients()[j].getOperations()
                print("O{} T: {}".format(k+1, operations[k]))
            print("")

    print("Duration of heuristic: {} seconds".format(duration))

if __name__ == '__main__':
    main()
