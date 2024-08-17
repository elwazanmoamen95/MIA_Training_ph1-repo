#include <bits/stdc++.h>
#include <cstdlib>  // For rand() and srand()
#include <ctime>    // For time()
using namespace std;

class Character {
    private:
        string name;
        double health;
        int energy;

public:
    Character(string name, double health, int energy) : name(name), health(health), energy(energy) {}

    virtual void attack(Character &opponent) = 0;
    virtual void defend(int damage) = 0;

    bool isDefeated() {
        return health <= 0;
    }
    void setHealth(int saved_damage){
            this->health -= saved_damage;
    }
    void setEnergy(int energy_consumed){
            this->energy -= energy_consumed;
    }
    double getHealth() {
        return health;
    }
    int getEnergy() {
        return energy;
    }
    string getName() {
        return name;
    }
};

// Batman Class
class Batman : public Character {
public:
    Batman() : Character("Batman", 100, 500) {}
    int use_0=0,use_1=0,use_2=0,use_sh=0,Bat=0;
    void attack(Character &opponent) override {
        cout << getName() << " attacks!" << endl;

        // Choose a random gadget for attack
        int gadget = rand() % 3;
        int damage = 0;
        int energy_consumed_B_A = 0;
        switch (gadget) {
            case 0:
                use_0++;
                if (use_0<=1) {
                    cout << "Uses Batclaw!" << endl;
                    damage = 20;
                    energy_consumed_B_A = 120;
                    break;
                }
            case 1:
                use_1++;
                if(use_0<=5){
                    cout << "Uses Grapple Gun!" << endl;
                    damage = 18;
                    energy_consumed_B_A = 88;
                    break;
                }
            case 2:
                use_2++;
                if(use_2<=3){
                    cout << "Uses Explosive Gel" << endl;
                    damage = 10;
                    energy_consumed_B_A = 92;
                    break;
                }
            case 3:
                
                cout << "Uses Batarang!" << endl;
                damage = 11;
                energy_consumed_B_A = 50;
                break;
        }
        setEnergy(energy_consumed_B_A);
        opponent.defend(damage);
    }

    void defend(int damage) override {
        cout << getName() << " defends!" << endl;

        // Choose a random shield for defense
        int shield = rand() % 2;
        int saved = 0;
        int energy_consumed_B_D = 0;

        switch (shield) {
            case 0:
                use_sh++;
                    if(use_sh<=2){
                        cout << "Uses  Smoke pellet!" << endl;
                        saved = 90; 
                        energy_consumed_B_D = 50;
                        break;
                    }
            case 1:
                cout << "Uses Cape Glide!" << endl;
                saved = 40; // 
                energy_consumed_B_D = 20;
                break;
        }

        int saved_damage = damage * (100 - saved) / 100;
        setHealth(saved_damage) ;
        setEnergy(energy_consumed_B_D);
        cout << getName() << "-->  Health: " << getHealth()<< endl;
    }
};

// Joker Class
class Joker : public Character {
public:
    Joker() : Character("Joker", 100, 500) {}
    int uses_0=0, uses_1=0,uses_sh=0;

    void attack(Character &opponent) override {
        cout << getName() << " attacks!" << endl;

        // Choose a random gadget for attack
        int gadget = rand() % 3;
        int damage = 0;
        int energy_consumed_J_A = 0;

        switch (gadget) {
            case 0:
                uses_0++;
                if(uses_0<=3){
                    cout << "Uses  Acid Flower!" << endl;
                    damage = 22;
                    break;
                }
            case 1:
                uses_1++;
                if(uses_1<=8){
                    cout << "Uses Laughing Gas!" <<endl;
                    damage = 13;
                    break;
                }
            case 2:
                
                cout << "Uses Joy Buzzer!" << endl;
                damage = 8;
                break;
        }
        setEnergy(energy_consumed_J_A);
        opponent.defend(damage);
    }

    void defend(int damage ) override {
        cout << getName() << " defends!" << endl;

        // Choose a random shield for defense
        int shield = rand() % 2;
        int save = 0;
        int energy_consumed_J_D = 0;
        if (damage != 20){ //damage 20 from Batclaw
            switch (shield) {
                case 0:
                    uses_sh++;
                    if(uses_sh<=3){
                        cout << "Uses Rubber Chicken!" << endl;
                        save = 80; 
                        energy_consumed_J_D = 40;
                        break;
                    }
                case 1:
                    cout << "Uses Trick Shield!" << endl;
                    save = 32; 
                    energy_consumed_J_D = 15;
                    break;
            }
        }
        else
            save = 0;

        int saved_damage = damage * (100 - save) / 100;
        setHealth( saved_damage);
        setEnergy(energy_consumed_J_D);
        cout << getName() << "-->  health: " << getHealth() <<endl;
    }
};

// Function to simulate the fight
void simulateFight(Batman &batman, Joker &joker) {
    while (!batman.isDefeated() && !joker.isDefeated()) {
        batman.attack(joker);
        if (joker.isDefeated()) break;
        joker.attack(batman);
    }

    if (batman.isDefeated()) {
        cout<<"Batman -->  Health: "<< batman.getHealth() <<"  Energy: "<< batman.getEnergy()<<endl;
        cout<<"Joker -->  Health: "<< joker.getHealth() <<"  Energy: "<< joker.getEnergy()<<endl;
        cout<< "Joker wins!" << endl;
    } else {
        cout<<"Batman -->  Health: "<< batman.getHealth() <<"  Energy: "<< batman.getEnergy()<<endl;
        cout<<"Joker -->  Health: "<< joker.getHealth() <<"  Energy: "<< joker.getEnergy()<<endl;
        cout << "Batman wins!" << endl;
    }
}

int main() {
    srand(static_cast<unsigned int>(time(0))); // Seed the random number generator

    Batman batman;
    Joker joker;
    simulateFight(batman, joker);
    return 0;
}
