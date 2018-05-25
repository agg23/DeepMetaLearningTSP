# TSP Meta-Learning using Deep Neural Networks

This repo contains the resources used in the development of my undergraduate thesis in Computer Science and Mathematics. The work began as a recreation of the work by Kanda et al., culminating in the exploration of several domains relating to the encoding and learning of TSP instances from a deep learning standpoint.

[Read the thesis here](docs/TSPMetaLearningUsingDeepNeuralNetworks.pdf)

## Data Pipeline

* Instances are generated using [Random Instance Generation.ipynb](Random%20Instance%20Generation.ipynb)
* The features developed for the Kanda Reproduction are run some number of times and timed using [Feature Generation.ipynb](Feature%20Generation.ipynb)
* The generated features were cleaned using [Feature Cleaning.ipynb](Feature%20Cleaning.ipynb)
* The final dataset used in the results was produced by filtering using [Feature Cleaning - Selecting 200.ipynb](Feature%20Cleaning%20-%20Selecting%20200.ipynb) (incomplete)
* The dataset is now suitable for the Kanda Reproductions. The Reproduction was originally approached using a very traditional TensorFlow deep dense network ([Kanda Reproduction.ipynb](Kanda%20Reproduction.ipynb)), but the results in the paper were produced using [Kanda Deep Reproduction.ipynb](Kanda%20Deep%20Reproduction.ipynb) for the classification network, and [Kanda Deep Ranking Reproduction.ipynb](Kanda%20Deep%20Ranking%20Reproduction.ipynb) for ranking.
* DeepWalk was run on the dataset using [DeepWalk Instance Generation.ipynb](DeepWalk%20Instance%20Generation.ipynb)
* The DeepWalk data was merged into the primary dataset using the first several cells of [DeepWalk LSTM.ipynb](DeepWalk%20LSTM.ipynb)
* The ranking LSTM network is trained in [DeepWalk LSTM.ipynb](DeepWalk%20LSTM.ipynb)
* The ranking ConvLSTM network is trained in [DeepWalk ConvLSTM.ipynb](DeepWalk%20ConvLSTM.ipynb)

## Resources

Papers:
* Kanda et al., 2016: http://linkinghub.elsevier.com/retrieve/pii/S0925231216302867

Collection of Python implementations of TSP heuristics:
* Tabu search and GRASP based off of https://github.com/samuelpordeus/algorithms-lib
* Simulated annealing based off of https://github.com/perrygeo/simanneal
* Genetic algorithm based off of https://github.com/Wafflenaut/Travelling-Salesman-Genetic-Algorithm
* Ant Colony based off of https://github.com/trevlovett/Python-Ant-Colony-TSP-Solver

Other
* Held-Karp lower bound based off of https://github.com/mslusky/heldkarp
* DeepWalk implementation/modifications based off of https://github.com/phanein/deepwalk, https://github.com/shun1024/weighted-deepwalk
* ConvLSTM implementation provided by https://github.com/carlthome/tensorflow-convlstm-cell