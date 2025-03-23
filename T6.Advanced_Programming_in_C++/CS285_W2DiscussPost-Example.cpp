#include <iostream>
#include <climits>

using namespace std;

/**
 * @brief A value no less than minValue and no more than maxValue.
 *
 */
class validateInt
{
public:
    int getValue() const {
        return validatedInt;
    };
    void setValue(int newValue);
    validateInt(int = 0, int = INT_MIN, int = INT_MAX);
private:
    int validatedInt;
    int minValue;
    int maxValue;
};

/**
 * @brief Represent seconds on a clock.
 *
 */
class seconds : public validateInt
{
public:
    /**
     * @brief Construct a new seconds object.
     *
     * @param value The number of seconds. Must be from 0
     *              through 59 (less than 1 minute).
     */
    seconds(int value = 0) : validateInt(value, 0, 59) {};
    /**
     * @brief Print the number of seconds as # seconds.
     *
     */
    void print() const {
        cout << getValue() << " seconds";
    };
};

/**
 * @brief Represent minutes on a clock
 *
 */
class minutes : public validateInt
{
public:
    /**
     * @brief Construct a new minutes object
     *
     * @param value The number of minutes. Must be from 0
     *              through 59 (less than 1 hour).
     */
    minutes(int value = 0) : validateInt(value, 0, 59) {};
    /**
     * @brief Print the number of minutes as # minutes.
     *
     */
    void print() const {
        cout << getValue() << " minutes";
    };
};

/**
 * @brief Represent hours on a 24-hour clock.
 *
 */
class hours : public validateInt
{
public:
    /**
     * @brief Construct a new hours object
     *
     * @param value The number of hours. Must be from 0
     *              through 23 (less than 1 day).
     */
    hours(int value = 0) : validateInt(value, 0, 23) {};
    /**
     * @brief Print the number of hours as # hours.
     *
     */
    void print() const {
        cout << getValue() << " hours";
    };
};

/**
 * @brief Represent the time as show on a 24-hour clock.
 *
 */
class clockType
{
public:
    /**
     * @brief Get the integer hour value.
     *
     * @return int The hour value
     */
    int hour() const
    {
        return hr.getValue();
    };
    /**
     * @brief Get the integer minute value.
     *
     * @return int The minute value
     */
    int minute() const
    {
        return min.getValue();
    };
    /**
     * @brief Get the integer second value.
     *
     * @return int The second value
     */
    int second() const
    {
        return sec.getValue();
    };
    /**
     * @brief Print the clocktype in the form hh:mm:ss
     *
     */
    void print() const {
       cout << hr.getValue() << ":"
            << min.getValue() << ":"
            << sec.getValue();
    };

    void setTime(int = 0, int = 0, int = 0);
    clockType(int = 0, int = 0, int = 0);
    clockType(hours, minutes, seconds);
private:
    hours hr;
    minutes min;
    seconds sec;
};

int main()
{
    cout << endl;

    //Setting acceptable values.
    hours myHour;
    minutes myMinute(50);
    seconds mySecond(33);

    myHour.setValue(20);

    clockType myClock(myHour, myMinute, mySecond);

    // Trying to set unacceptable values
    myHour.setValue(30);

    clockType mySecondClock(10, 20, 80);

    // Testing printing
    myHour.print();
    cout << endl;
    myMinute.print();
    cout << endl;
    mySecond.print();
    cout << endl;
    cout << endl;

    myClock.print();
    cout << endl;
    mySecondClock.print();
    cout << endl;

    return 0;
}

/**
 * @brief Ensure the set value is in the accepted range of values.
 *
 * @param newValue The attempted new value. If this value is no
 *      less than the object's minValue and no greater than the
 *      object's maxValue, then the object's value will be changed
 *      to newValue.
 */
void validateInt::setValue(int newValue)
{
    if (newValue >= minValue && newValue <= maxValue)
        validatedInt = newValue;
    else
        cout << "Error: Value (" << newValue
             << ") not set. Value must be less than "
             << maxValue + 1 << " and greater than " << minValue + 1
             << "." << endl;
}

/**
 * @brief Construct a new validateInt::validateInt object
 *
 * @param numberToValidate Should be no less than minimumValue
 *      and no more than maximumValue.
 * @param minimumValue The minimum acceptable value.
 * @param maximumValue The maximum acceptable value.
 */
validateInt::validateInt(int numberToValidate, int minimumValue,
                         int maximumValue)
{
    minValue = minimumValue;
    maxValue = maximumValue;

    validatedInt = minValue; // Initialize variable.

    setValue(numberToValidate);
}

/**
 * @brief Set the Time object's hours, minutes, and seconds.
 *
 * @param hour The hour on the clock from 0 through 23.
 * @param minute The minutes on the clock from 0 through 59.
 * @param second The seconds on the clock from 0 through 59.
 */
void clockType::setTime(int hour, int minute, int second)
{
    if (second >= 60)
    {
        minute += second / 60;
        second = (second % 60);
    }
    if (minute >= 60)
    {
        hour += minute / 60;
        second = (minute % 6);
    }
    if (hour >= 24)
    {
        cout << "Removed " << hour / 24 << " days from time.";
        hour = hour % 24;
    }
    hr = hours(hour);
    min = minutes(minute);
    sec = seconds(second);
}

/**
 * @brief Construct a new clockType::clockType object
 *
 * @param hour The hour on the clock from 0 through 23.
 * @param minute The minutes on the clock from 0 through 59.
 * @param second The seconds on the clock from 0 through 59.
 */
clockType::clockType(int hour, int minute, int second)
{
    hr = hours(0);
    min = minutes(0);
    sec = seconds(0);
    setTime(hour, minute, second);
}
/**
 * @brief Construct a new clockType::clockType object
 *
 * @param hour The hours on the clock using an hours class object.
 * @param minute The minutes on the clock using an minutes class object.
 * @param second The seconds on the clock using an seconds class object.
 */
clockType::clockType(hours hour, minutes minute, seconds second)
{
    hr = hour;
    min = minute;
    sec = second;
}
