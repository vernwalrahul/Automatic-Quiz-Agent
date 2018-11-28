# Automatic-Quiz-Agent
Knwoledge Modelling and Semantic Technologies (Term Project)

# Goal of our Project
To create a automated quiz agent for the Knowledge Graph by extracting s,p,o tuples from it, and generating well formed questions 
from them.
We used M.Heilman's work from CMU-LTI [1],to generate the questions from URI's,full documentation of our work-flow is attached as 
[2]//Add the link to our complete slides
# Knowledge graph Schema
Dictionary of {"s":["LABEL","TYPE",list[(("o",type_of_o),list["p"])]]} object and list of predicates hashed with respect to 
the corresponding subject.

[1] http://www.cs.cmu.edu/~ark/mheilman/questions/

[2]
Link to our compressed file of codes and all dependicies https://www.dropbox.com/s/rjq10n2mibfiqxz/KMST_Automatic_Quiz_Agent.tar.xz?dl=0

# Hosting the application locally  
- Install Apache server
- Change the default path to the location of "Quiz" folder
- Test on browser at localhost