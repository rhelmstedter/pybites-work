import numpy as np
import random

np.random.seed(1)
n = 1
p_sped = (1/6)
p_lowin = (7/20)

runs = 10000
pop = 600

PR_exact = 0
PR_twoper = 0
for i in range(runs):
    sped = 0
    lowin = 0
    both = 0
    sample_school = []
    for s in range(pop):
        student = str(np.random.binomial(n,p_sped)) + str(np.random.binomial(n,p_lowin))
        if int(student) == 10:
            sped += 1
        elif int(student) == 1:
            lowin += 1
        elif int(student) == 11:
            both += 1
        sample_school.append(student)
    per_lowsped = both/(sped + both)
    per_lowpop = (lowin+both)/(pop)
    if 0<(per_lowsped-per_lowpop)<= 0.02:
        PR_twoper += 1
    elif per_lowsped==per_lowpop:
        PR_exact +=1

prob_PR_exact = (PR_exact/runs)*100
prob_PR_twoper = (PR_twoper/runs)*100
print('The probability of having exact proportional representation in ' +str(runs) + ' trials is: '
      + str(prob_PR_exact) + '%')
print('The probability of having proportional representation within 2% in ' +str(runs) + ' trials is: '
      + str(prob_PR_twoper) + '%')
