#include <iostream>
#include <string>
#include <iomanip>

using namespace std;

int main()
{
    string userEntry;
    char x = 'x', o = 'o', b = ' ';

    cout << "Welcome to Tic-Tac-Toe!" << endl << endl;

    for (int i = 0; i < 3; i++)
    {
        cout << '|';
        for (int j = 0; j < 3; j++)
        {
            cout << setw(2) << '|';
        }
        cout << endl;
    }

    return 0;
}
