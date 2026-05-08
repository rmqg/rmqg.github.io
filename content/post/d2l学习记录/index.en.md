---
title: D2L Study Notes
description: D2L Study Notes

date: 2026-04-20T14:23:30+08:00
lastmod: 2026-05-06T12:00:00+08:00

categories:
  - d2l
tags:
  - d2l
  - PyTorch
  - Neural Networks
  - Deep Learning

math: true
---

## Environment Setup Memo
Remember to mount the `WORK` disk
```shell
cd /run/media/rmqg/WORK/learnDeepLearning/d2l-zh/d2l-zh/pytorch/
conda activate d2l
jupyter lab
```

## 2. Preliminaries, 3. Linear Neural Networks
The tutorial starts from `linear regression` and `softmax regression`, introducing the fundamental methods for training models, including the following basic concepts:

- `Training set`: Data used for the model to learn from
- `Test set`: Data used to evaluate the model's generalization ability
- `Feature`: Information fed to the model, such as pixel values, numerical attributes, etc.
- `Label`: The ground-truth answer corresponding to a sample
- `Sample`: A single data instance in the dataset
- `Model`: A function or computation process that maps inputs to outputs
- `Parameter`: Quantities in the model that need to be learned through training, such as weights and biases
- `Batch size`: The number of samples fed into the model for training at each step
- `Epoch`: The process of going through the entire training set once
- `Forward propagation`: The process of passing input data through the model to obtain predictions
- `Loss function`: A function that measures the discrepancy between the model's predictions and the ground-truth labels
- `Accuracy`: The proportion of correctly predicted samples in a classification task
- `Gradient`: The sensitivity of the loss function to changes in parameters
- `Backpropagation`: The process of computing gradients for each parameter based on the loss
- `Optimizer`: A method for updating model parameters based on gradients
- `Gradient descent`: The most common idea for parameter updates — adjusting parameters in the direction of decreasing loss
- `Learning rate`: A hyperparameter that controls the step size of each parameter update
- `Generalization`: The model's ability to perform on unseen data

Combined with practical code, the basic method for training a model is given:

- Iterate over the entire training set
- Forward propagation
- Compute the loss
- Backpropagation
- Update parameters
- Record the training loss and training accuracy for this epoch

### Difference Between "Concise Implementation" and "Implementation from Scratch"

Compared to the previous section's implementation of softmax regression from scratch, the "concise implementation" in this section does not change the model in essence — it still flattens the input image, passes it through a fully connected layer to output scores for 10 classes, and trains with cross-entropy loss. The main difference between the two lies in the implementation approach:

When implementing from scratch, you need to manually define the model parameters `W` and `b`, write the `softmax` function, cross-entropy loss function, and the parameter update process yourself. The benefit is a clearer understanding of the mathematical principles and training pipeline behind softmax regression — for example, what forward propagation, loss computation, backpropagation, and gradient descent each do.

In the concise implementation, most of these low-level details are handled by PyTorch's high-level APIs. For example, `nn.Flatten()` automatically flattens the input image, `nn.Linear(784, 10)` automatically defines the linear layer and its parameters, `nn.CrossEntropyLoss()` directly computes the loss for multi-class tasks, and `torch.optim.SGD` handles parameter updates. This results in shorter, more standardized code that better aligns with common practices in real-world engineering.

Additionally, the concise implementation has an important advantage over the handwritten version: better numerical stability. When implementing from scratch, computing softmax and cross-entropy directly according to their mathematical definitions may encounter issues like exponential overflow or underflow; frameworks typically have internal optimizations for these cases, making them safer and more reliable in practice.

> [!NOTE]
> The concise implementation hides the implementation details of `d2l.train_ch3` and its called functions. It is speculated that they are consistent with the functions of the same name in the implementation from scratch.

> [!WARNING]
> Exercise 3.7.6 is suspected to have the following issue: increasing the number of epochs does not cause test accuracy to decrease after a certain period, but rather to plateau near an upper bound.

![The author ran 1k epochs for an hour](d2l学习记录-01.png)

The speculated reason is that `softmax` regression is essentially a linear model with an inherent upper bound on its expressiveness. The model has only about `7850` parameters (784×10 + 10), and with `60000` training samples, the parameter count is far from sufficient to "memorize" the training data. Therefore, no matter how many epochs are trained, the model cannot truly overfit — it suffers from `underfitting` rather than `overfitting`. Both training accuracy and test accuracy eventually converge and stabilize near an upper bound (around 85%), with the gap between them remaining small throughout.

The emergence of overfitting requires the model to have sufficient capacity to fit the noise in the training set, and a linear classifier simply lacks this capability for nonlinear tasks like image classification. The premise of this textbook exercise ("test accuracy will decrease after a certain period") is more suitable for describing models with more parameters and greater expressiveness, such as multilayer perceptrons or convolutional neural networks on small datasets.

## 4. Multilayer Perceptrons
### Basic Concepts
- `Deep Neural Network (DNN)`: A neural network with many hidden layers
- `Anti-monotonicity`: Causes the limitations of linear model fitting
- `Starting point for designing nonlinear models`: When representing data, we consider the correlated interactions between features; building a linear model on top of this representation may be appropriate
- `Hidden layer`: Adding one or more hidden layers to the network to overcome the limitations of linear models, enabling it to handle more general types of functional relationships
- `Multilayer Perceptron (MLP)`: Stacking many fully connected layers together. Each layer outputs to the layer above, until the final output is generated. The first L-1 layers are treated as the representation, and the last layer as a linear predictor
- `Nonlinear activation function`: Applied to each hidden unit after the affine transformation, preventing the `multilayer perceptron` from degenerating into a `linear model`
- `Universal approximation theorem`: Theoretically, a `single hidden layer network` can learn any function, but by using `deeper` (rather than `wider`) networks, we can more easily approximate many functions
- `Activation function`: Determines whether a neuron should be activated by computing the weighted sum and adding a bias; they are differentiable operations that transform input signals into outputs
  - `ReLU function`: $\text{ReLU}(x) = \max(x,\, 0)$
  - `Sigmoid function (squashing function)`: $\sigma(x) = \dfrac{1}{1 + e^{-x}}$
  - `Tanh (hyperbolic tangent) function`: $\tanh(x) = \dfrac{e^x - e^{-x}}{e^x + e^{-x}}$
- `Overfitting`: A phenomenon where the model fits the training data more closely than it does the underlying distribution
- `Regularization`: Techniques used to combat overfitting
- `Training error`: The error computed by the model on the training dataset
- `Generalization error`: The expected model error when applied to an infinite number of data samples drawn from the same distribution as the original samples
- `Independent and identically distributed (i.i.d.) assumption`: The assumption that `training data` and `test data` are independently drawn from the same distribution. In practice, almost all real-world applications involve some violation of the i.i.d. assumption

> Several factors that tend to affect model generalization
> The number of tunable parameters. When the number of tunable parameters (sometimes called degrees of freedom) is large, the model tends to overfit more easily.
> The values adopted by the parameters. When the weight values have a large range, the model may be more prone to overfitting.
> The number of training samples. Even a simple model can easily overfit a dataset containing only one or two samples. Overfitting a dataset with millions of samples requires an extremely flexible model.

- `Model selection`: Selecting the final model after evaluating several candidate models, such as:
  - Fundamentally different models, e.g., decision trees vs. linear models
  - The same class of model with different hyperparameter settings, possibly using a `validation set`
- `Validation set`: In principle, we do not want to use the `test set` before determining all `hyperparameters`, to avoid overfitting the `test data`; nor can we rely solely on `training data` for model selection, as we cannot estimate the `generalization error` of the `training data`. Therefore, a common practice is to split the data into three parts: in addition to the `training and test datasets`, a `validation dataset` (also called `validation set`) is added
- `K-fold cross-validation`: The original training data is split into $K$ non-overlapping subsets. Then $K$ rounds of model training and validation are performed, each time training on $K-1$ subsets and validating on the remaining subset (the one not used for training in that round). Finally, the training and validation errors are estimated by averaging the results of the $K$ experiments

#### Overfitting and Underfitting
- `Underfitting`: The generalization error between our `training` and `validation` errors is small, but both are severe; there is reason to believe that a more complex model can `reduce the training error`
- `Overfitting`: The `training error` is significantly lower than the `validation error`

Whether overfitting or underfitting occurs may depend on the model complexity and the size of the available training dataset.

`Model complexity`:

![Figure 4](image-2.png)

`Dataset size`: The fewer samples in the training dataset, the more likely (and more severely) we are to overfit. Given more data, we may attempt to fit a more complex model (which gave rise to `deep learning`)



### Difficulties
Joint optimization of hyperparameters such as

- Learning rate
- Number of training epochs
- Number of hidden layers
- Number of hidden units per layer

to find the optimal or near-optimal solution. Moreover, hyperparameters are not independent of each other but interact; `hyperparameter optimization` is a high-dimensional search problem, and brute-force training is very costly.

Strategies:

- `Staged search`:
  - First fix a relatively simple model structure and tune `batch size`
  - Search for `learning rate`
  - Then, around a good learning rate, search for `number of hidden units`
  - Then compare `number of hidden layers`
  - Finally, fine-tune `number of training epochs`
- `Coarse-to-fine search`:
  - First do a coarse search with sparser candidate values
  - Find a roughly good region, then do a fine search nearby
- `Random search`: Try your luck
- `Early stopping`: If the results look unreasonable, stop early and switch to different hyperparameters
- Check the validation set first, do not use the test set directly, to avoid overfitting the test set as well (d2l only has training and test sets at this point, so this does not need to be considered for now)

When doing the `Exercise 4.3 Concise Implementation of Multilayer Perceptron`, the author chose `batch size` 256, `lr` 0.03, `number of hidden units` 1024, `number of hidden layers` 1, and `number of training epochs` 20. The training results are as follows:

![Figure 2](image-1.png)

## Random Musings
Why does the `test acc` curve have a mysterious dip at this point?

![Figure 3](image.png)

> [!CAUTION]
> To become an excellent machine learning scientist, one needs critical thinking skills.

Why does the overfitting in the textbook look different from what I got?

![Figure 5](image-3.png)

![Figure 6](image-4.png)

---

*Translation provided by `mimo-v2.5-pro`*
