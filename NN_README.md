# In Chapter 1 of Michael Nielsen’s Neural Networks and Deep Learning.
## implement NN from scratch 
The intro of the ch1 discuss the complexity of human brain and how incredibly efficient at recognizing visual patters and it's hard for computers. Instead of manually coding rules, NN learn from training that allows network to improve accuracy.
perceptrons have ability to model different decision-making processes and compute logical functions by varying the weights and increasing biases 
  * Bias Term: The threshold is replaced with a bias term b, simplifying the activation rule to output = 1 if w · x + b > 0.
  * The weighted sum ∑j wj xj is expressed as a dot product.
### The Architecture of Neural Networks
 **Layers:**
  consists of layers, simple NN has 3 layers: input layer that recieve data , hidden layer allow network to learn and output layer that responsable for prediction. Each of layers is made up of neurons which connected with another one in another layer via weights
 **Feedforward:**
  informations flow from input tp output then computes a weighted sum through a ReLU function.
 **RNN:**
  which allows feedback loops, RNNs are better suited for tasks involving sequential data
 **Cost Function:** 
  measures how far the network's predictions are from the actual values and to improve the accuracy --> minimize the cost function 
### Handwritten Digit Classification
 consider the task of classifying handwritten digits. Suppose we segment an image of several handwritten digits into separate images, each containing one digit
 * Input Layer: Consists of 784 neurons (for 28x28)
 * Output Layer: Has 10 neurons, one for each digit from 0 to 9
