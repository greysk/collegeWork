#include <iostream>
#include <cctype>
#include <string>

using namespace std;

int convertStringNum(string strNum);

int main()
{
    string number = "-12.5"; // "-12.5"
    int num = convertStringNum(number); // -12.5

    cout << number << " as an integer " << num;
    return 0;
}

int convertStringNum(string strNum)
{
    int intNum = 0, numSign = 1, placeValue = 1;

    for (int i = (strNum.length() - 1); i >= 0; i--)
    {
        char strNumPart = strNum[i];

        if (isdigit(strNumPart))
        {
            intNum += (static_cast<int>(strNumPart) - 48) * placeValue;
            placeValue *= 10;
        }
        else if (strNumPart == '.')
        {
            placeValue = 1;
            intNum = 0;
        }
        else if (i == 0 && strNumPart == '-')
            numSign = -1;
    }
    return intNum * numSign;
}

int raise(int n, int exp)
{
    return static_cast<int>(pow(n, exp));
}

int getDigit(int num, int place)
{
    if (place == len(num) - 1)
        return num / raise(10, place);
    if (place == 0)
        return num % raise(10, place + 1);

    return num % raise(10, place + 1) / raise(10, place);
}

int len(int num)
{
    int numDigits = 0;

    while (num / 10 != 0 || num % 10 != 0)
    {
        num /= 10;
        numDigits++;
    }

    return numDigits;
}

string numToStr(int number)
{
    string strNum;
    char digit;

    for (int i = len(number) - 1; i >= 0; i--)
    {
        digit = static_cast<char>(getDigit(number, i) + 48);
        strNum.append(1, digit);
    }
    return strNum;
}
