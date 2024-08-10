#include <bits/stdc++.h>
using namespace std;

int searchValue(int n ,int value,int arr[]){
    for (int i = 0; i < n; i++){
    if (value == arr[i])
        return i;
    }
        return -1;
};

int main(){
    int n, val;
    cin >> n;
    int Num[n];
    for (int i = 0 ; i < n ; i++){
        cin >> Num[i];
    }
    cin >> val;
    cout << searchValue(n, val, Num) << endl;
    return 0;
}