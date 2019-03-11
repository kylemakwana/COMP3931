#include<iostream>
#include<random>

using namespace std;

// ----------------------- CLASSES -----------------------

class Patient
{
    int hour[2], minute[2];
    void SetFirstJobValues();
    void SetSecondJobValues();
    public:
      void SetJobValues();
      int* GetJobHours() {return hour;}
      int* GetJobMinutes() {return minute;}
      double GetDuration();
};

void Patient::SetFirstJobValues()
{
    const int minHour = 9;
    const int maxHour = 11;
    int minutes[4] = {0, 15, 30, 45};

    random_device randDev;
    mt19937 generator(randDev());
    uniform_int_distribution<int> hourDistr(minHour, maxHour);

    hour[0] = hourDistr(generator);

    random_device minRandDev;
    mt19937 minGenerator(randDev());
    uniform_int_distribution<int> minDistr(0, sizeof(minutes)/sizeof(*minutes));

    int i = minDistr(minGenerator);
    minute[0] = minutes[i];
}

void Patient::SetSecondJobValues()
{
    const int minHour = 12;
    const int maxHour = 14;
    int minutes[4] = {0, 15, 30, 45};

    std::random_device randDev;
    std::mt19937 generator(randDev());
    std::uniform_int_distribution<int> hourDistr(minHour, maxHour);

    hour[1] = hourDistr(generator);

    random_device minRandDev;
    mt19937 minGenerator(randDev());
    uniform_int_distribution<int> minDistr(0, sizeof(minutes)/sizeof(*minutes));

    int i = minDistr(minGenerator);
    minute[1] = minutes[i];
}

void Patient::SetJobValues()
{
    SetFirstJobValues();
    SetSecondJobValues();
}

double Patient::GetDuration()
{
    int totalHours = hour[1] - hour[0];
    double totalMinutes = minute[1] - minute[0];

    if(totalMinutes < 0)
    {
      totalHours -= 1;
      totalMinutes = 60 + totalMinutes;
    }

    double total = totalHours + (totalMinutes / 60);
    return total;
}

class Machine
{
    Patient* machinePatients;
    public:
      bool IsFree(Patient);
      void AddPatient(Patient);
      Patient* GetPatients(){return machinePatients;}
      int NumPatients(){return (sizeof(machinePatients) / sizeof(*machinePatients));}
};

void Machine::AddPatient(Patient patient)
{
    int numPatients = NumPatients();
    machinePatients[numPatients] = patient;
}

bool Machine::IsFree(Patient patient)
{
    int *patientHours = new int[2];
    int *patientMins = new int[2];

    int *machineHours = new int[2];
    int *machineMins = new int[2];

    for(int i = 0; i < 2; i++)
    {
      patientHours[i] = patient.GetJobHours()[i];
      patientMins[i] = patient.GetJobMinutes()[i];
    }

    for(int i = 0; i < (sizeof(machinePatients) / sizeof(*machinePatients)); i++)
    {
        for(int j = 0; j < 2; i++)
        {
          machineHours[i] = machinePatients[i].GetJobHours()[j];
          machineMins[i] = machinePatients[i].GetJobMinutes()[j];

          if(patientHours[j] == machineHours[j] && patientMins[j] == machineMins[j]) //patient clash
          {
              return false;
          }
        }
    }

    return true;
}

// ----------------------- METHODS -----------------------

void Swap(Patient* a, Patient* b)
{
    Patient c = *a;
    *a = *b;
    *b = c;
}

int Partition(Patient array[], int low, int high)
{
    Patient pivot = array[high];
    int i = low - 1;

    for(int j = low; j <= high - 1; j++)
    {
        if(array[j].GetDuration() >= pivot.GetDuration()) //Sign changed in order to make it descending instead of ascending
        {
            i++;
            Swap(&array[i], &array[j]);
        }
    }
    Swap(&array[i+1], &array[high]);
    return i+1;
}

//Quicksort for the jobs to order based on length of total stay
void QuickSort(Patient array[], int low, int high)
{
    if(low < high)
    {
        //pi is the partitioning index. array[pi] is now at the right place
        int pi = Partition(array, low, high);

        QuickSort(array, low, pi - 1);
        QuickSort(array, pi + 1, high);
    }
}

void PrintArray(Patient arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << arr[i].GetDuration() << endl;
    }
}

int main(int argc, char const *argv[])
{
    int numPatients = 10;
    int numMachines = 2;

    //Override the number of default patients by entering the number as the first parameter in the command line
    if(argc > 1)
    {
        numPatients = atoi(argv[1]);
    }

    if(argc > 2)
    {
        numMachines = atoi(argv[2]);
    }

    Patient dayPatients[numPatients];
    Machine dayMachines[numMachines];

    for(int i = 0; i < numPatients; i++)
    {
        Patient patient;
        patient.SetJobValues();

        dayPatients[i] = patient;
    }

    for(int i = 0; i < numMachines; i++)
    {
        Machine machine;
        dayMachines[i] = machine;
    }

    QuickSort(dayPatients, 0, (sizeof(dayPatients)/sizeof(*dayPatients))-1);

    for(int i = 0; i < numMachines; i++)
    {
        Machine curMachine = dayMachines[i];

        if(curMachine.IsFree(dayPatients[i]))
        {
            curMachine.AddPatient(dayPatients[i]);
        }
    }

    for(int i = 0; i < numMachines; i++)
    {
        Machine machine = dayMachines[i];

        cout << "----------------- Machine " << i+1 << "-----------------" << endl;

        for(int j = 0; j < machine.NumPatients(); j++)
        {
            for(int k = 0; k < 2; k++)
            {
                cout << "J" << k+1 << " H: "<< machine.GetPatients()[k].GetJobHours()[k] << endl;
                cout << "J" << k+1 << " M: "<< machine.GetPatients()[k].GetJobMinutes()[k] << endl;
            }
        }
    }
    //test

    // for(int i = 0; i < (sizeof(dayPatients)/sizeof(*dayPatients)); i++)
    // {
    //     Patient patient = dayPatients[i];
    //     cout<< "----------------- Patient " << i+1 << "-----------------" << endl;
    //
    //     for(int j = 0; j < (sizeof(patient.GetJobHours()) / sizeof(*patient.GetJobHours())); j++)
    //     {
    //         cout<< "---------- Job " << j+1 << " ----------" << std::endl;
    //         cout<< "Hour: " << patient.GetJobHours()[j] << " Minute: " <<patient.GetJobMinutes()[j] << endl;
    //
    //         if(j > 0)
    //         {
    //           cout<<"Total duration: " << patient.GetDuration() << endl;
    //         }
    //
    //         cout<< endl;
    //     }
    // }
    // PrintArray(dayPatients, (sizeof(dayPatients)/sizeof(*dayPatients))-1);
    // cout << "Longest patient time: " << dayPatients[0].GetDuration() << endl;
    // cout << "Shortest patient time: " << dayPatients[(sizeof(dayPatients)/sizeof(*dayPatients))-1].GetDuration() << endl;

    return 0;
}
