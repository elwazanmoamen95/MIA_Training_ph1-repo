#include <iostream>
#include <stack>
using namespace std;

class QueueUsingStacks {
private:
    stack<string> stack1, stack2;

public:
    // add an item to the queue
    void add(const string& item) {
        stack1.push(item);
    }

    bool isEmpty() const {
        return stack1.empty() && stack2.empty();
    }

    void displayQueue() {
        cout << "Queue: ";
        // Reverse stack1 to display its elements in queue order
        while (!stack1.empty()) {
            stack2.push(stack1.top());
            stack1.pop();
        }
        // Display elements from stack1 (back of the queue)
        while (!stack2.empty()) {
            cout << stack2.top() << " ";
            stack2.pop();
        }
        cout << endl;
    }
};

int main() {
    QueueUsingStacks batmanQueue;

    // add Batman's gadgets and shields
    batmanQueue.add("Batarang ");
    batmanQueue.add("Grapple Gun ");
    batmanQueue.add("Explosive Gel ");
    batmanQueue.add("Batclaw ");
    batmanQueue.add("Cape Glide ");
    batmanQueue.add("Smoke Pellet ");
    // Display the queue
    batmanQueue.displayQueue();


    return 0;
}
