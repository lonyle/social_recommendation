# We will open source all the code in this folder when this paper is published

# The technical report is in the fild technical_report.pdf

# Before you run
1. install joblib (to load our regression model)
2. compile the Influence Maximization algorithm by:
$ cd OPIM1.1
$ make

# How to run the demo (we use python3)
$ bash manifest.sh

# If you want to get the samples from the scratch (it may take more than one day)
For the simulation section, we pre-store 2000*1.3M samples
If you want to do it yourself, you can 
	1. delete those files with pattern data/uniform_informed_prob*
	2. download the social network data "user.json" from Yelp's website: https://www.yelp.com/dataset/challenge, and put it under the /data folder
	3. run $ simulation/sampling_size.py
	4. run the experiments in Section 6 again, e.g. $ python simulation/exp2.2_impact_initial_info_prob.py

Since the full experiments take some time (maybe more than one day, depending on your machine). The default demo in manifest.sh shows one experiment in Section 6 and one experiment in Section 7 respectively. You can uncomment all the lines to get full experiment results.

If you want to know the details of each folder, please read the following.

# Introduction to each folder (corresponding to each step)
## data: the raw data and derived data
## 1. preprocess: collect some data, and convert the raw data to the standard format, refill the entries needed
- input: raw data
- output: prepocessed data for inference

## 2. inference: infer the parameters of the model. (1) how the reward, price and other factors affect the probability of recommendation (2) how the probability of recommendation
- input: the pre-processed data
- output: the inferred parameters
### evaluation: evaluate the predictive accuracy of the inference (may use simulation)

## 3. simulation: simulate the diffusion of recommendations
- input: the recommendation probability for different types of users, the probability to be initially informed from other information sources
- output: the expected number of users who are informed from recommendations and from other information sources

## 4. analysis: analyze the impact of different factors, directly from data (or inferred parameters), or from simulations
- input: preprocessed data, inferred data, and the simulation algorithm
- output: the impact of various factors of our interests

## 5. optimization: find the optimal strategies of a firm when the firm can use dynamic strategies
- input: social network graph, parameter settings
- output: the dynamic strategies of a firm