#include <string>
#include <iostream>

using namespace std;

class personName
{
    friend ostream& operator<<(ostream&, const personName&);
    friend istream& operator>>(istream&, personName&);
public:
    personName(string = "", string = "");
private:
    string fName;
    string lName;
};

//Class constructor
personName::personName(string firstName, string lastName)
{
    fName = firstName;
    lName = lastName;
}

//Stream Insertion Operator Overload Function
ostream& operator<<(ostream& osObj, const personName& pName)
{
    osObj << pName.fName << " " << pName.lName;

    return osObj;
}

//Stream Extraction Operator Overload Function
istream& operator>>(istream& isObj, personName& pName)
{
    isObj >> pName.fName >> pName.lName;

    return isObj;
}

int main()
{
    personName myName("Graeson", "Thomas");
    personName aName;

    cout << "My name is " << myName
         << endl << endl;

    cout << "What is your first and last name: ";
    cin >> aName;
    cout << endl;

    cout << "Nice to meet you, " << aName << "!" << endl;

    return 0;
}
