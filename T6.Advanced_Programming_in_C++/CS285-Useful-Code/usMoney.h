#include <iostream>
#include <cmath>
#include <string>

using namespace std;

class usMoney
{
    friend ostream& operator<<(ostream&, const usMoney&);
    friend istream& operator>>(istream&, usMoney&);
public:
    //Other functions removed for this example.
    usMoney(double = 0);
private:
    int dollars;
    int cents;
    int sign;
    void setMoney(double value);
};

//Used by class constructor and instream overload function.
void usMoney::setMoney(double value)
{
    //Both dollars and cents will be stored as positive values to avoid math errors.
    sign = (value < 0) ? -1 : 1;
    value = abs(value);

    dollars = static_cast<int>(value);  //Store the positive integer portion of value in dollars.

    //Covert cents to an integer. Rounding used to address floating point issues (e.g. 0.20 becoming 0.199999999...).
    cents = static_cast<int>(round(100 * (value - dollars)));
}

//Class constructor
usMoney::usMoney(double value)
{
    sign = 1; //Initialize the value of sign.
    setMoney(value);
}

//Output to stream the money value in dollar and cent format. Example:  –$1,234,567.80
ostream& operator<<(ostream& ostreamObj, const usMoney& money)
{
    //Convert dollars to a string as it's easier to add commas using a string.
    string sDollars = to_string(abs(money.dollars));
    //Get the number of commas for the output for $10,000 and up.
    int numCommas = (sDollars.length() - 1) / 3;

    //If money value is negative, print an n-dash before the dollar sign
    if (money.sign == -1)
        ostreamObj << "–";

    ostreamObj << "$";

    //Output dollar numbers, starting from the first number and adding commas, as necessary.
    for (int i = 0; i <= numCommas; i++)
    {
        if (i == 0 && sDollars.length() % 3 != 0)
            //When the number of digits is not divisible by 3, the first comma comes after less than three digits.
            ostreamObj << sDollars.substr(i, sDollars.length() % 3);
        else
            ostreamObj <<  sDollars.substr(i, 3);

        if (i < numCommas)
            ostreamObj << ",";
    }

    ostreamObj << ".";  //Output a period between the dollars and cents.

    //Output cents as a two-digit decimal, adding a leading zero to single-digit integers (0 through 9).
    if (money.cents >= 10)
        ostreamObj << money. cents;
    else
        ostreamObj << "0" << money.cents;

    return ostreamObj;
}

istream& operator>>(istream& istreamObj, usMoney& money)
{
    double inMoney;

    istreamObj >> inMoney;  //Get input double (or integer value)

    money.setMoney(inMoney);  //Use class function to update class values

    return istreamObj;
}
