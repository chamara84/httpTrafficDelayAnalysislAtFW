# httpTrafficDelayAnalysislAtFW
This contains python scripts to analyse and simulate traffic arriving at a firewalls and measure delay encountered.

In this project the data log of arrival time of each file with different MIME types and the size of those files we given to me as the data. The capture file was in csv format and had a size of around 5-10 GB.  This was the arrival process. Then another log file having the processing times at the deep packet inspection engine and the anti-spam engine for different MIME data types of different sizes was given. This file contained the information on the service process.
My task was to implement the following using MATLAB and Python

•	Replay capture data for the arrival process, altering replay speed, extracting different components, replicating certain components etc. and record latency induced by device for each flow.

•	Fit a model using regression on measured parameters and fit probability distributions for the error around this regression line for the processing times provided by the client. This is our server model.

•	Construct discrete event simulation for the operation of the devices, using server model and real arrival traces from experiments. Tweak if necessary until some performance measure (property of distribution of latency) matches measured from experiment sufficiently well.

•	Create abstract models of arrival processes and run simulations with these instead of arrival traces. Tweak models as necessary so that, statistical properties of latency measure over a number of arrival traces match those from trace simulations.

•	Analyze statistical properties of long term (month) log in terms of marginal distributions, correlations, autocorrelations over long term of parameters of micro model.

•	Create simulation model for macro model 

