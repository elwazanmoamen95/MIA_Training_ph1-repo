#include <bits/stdc++.h>
using namespace std;

// func compare matrices and score the wins times 
void comp(int r, int c, int arr_1[][100], int arr_2[][100]) {
    int justice_score = 0, villains_score = 0;
    for (int i = 0; i < r; i++){
        for (int j = 0; j < c; j++){
            if(arr_1[i][j] > arr_2[i][j])
                ++justice_score;
            else if(arr_1[i][j] < arr_2[i][j])
                ++villains_score;
        }
    }
    if(justice_score > villains_score)
        cout << "Justice League"<< endl;
    else if (justice_score < villains_score)
        cout << "Villains" << endl;
    else
        cout << "Tie" << endl;
}

int main(){
    int r,c, justice[100][100], villains[100][100];
    cin >> r >> c;
    // input the matrix of justice_league 
    for (int i = 0; i < r; i++){
        for (int j = 0; j < c; j++){
            cin >> justice[i][j];
        }
    }

    // input the matrix of villains 
    for (int i = 0; i < r; i++){
        for (int j = 0; j < c; j++){
            cin >> villains[i][j];
        }
    }
    comp(r, c, justice, villains);
    return 0;
}