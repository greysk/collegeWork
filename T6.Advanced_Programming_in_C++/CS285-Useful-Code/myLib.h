namespace std
{
    void resetPointer(int* &p)
    {
        delete p;
        p = nullptr;
    }
}
