import fullbot as F
import time as t

string = """1
t star = 2.262
t star = 2.861
From table: t star = 1.671 using calculator: t star = 1.665

3
Not satisfied.
We cannot assume the population follows a Normal distribution.
The sample size is small (n = 28 is less than 30), and there are outliers in the data.

5
Part A:
	•	Random: No, students were not chosen randomly.
	•	10 percent condition: 32 is less than 10 percent of all students in the school (if there are at least 320 students).
	•	Normal/Large sample: Yes, because the sample size is large enough (32 is greater than 30).

Part B:
	•	Random: The sample consists of 100 home sales randomly chosen from the past 6 months in the city.
	•	10 percent condition: Assume 100 is less than 10 percent of all home sales in the last 6 months.
	•	Normal/Large sample: Yes, even though the box plot shows a strong right skew with outliers, the condition is still met because the sample size is large enough (100 is greater than 30).

7
Standard error of x = standard deviation divided by square root of n = 9.327 divided by square root of 23 = 1.7898.
In many random samples of size 23, the sample mean blood pressure will typically vary by about 1.7898 from the population mean.

11
Part A:
	•	State: Construct a 90 percent confidence interval for the true mean weight of an Oreo cookie in grams.
	•	Plan: Use a one-sample t-interval.
	•	Random sample of 36 cookies.
	•	36 is less than 10 percent of all Oreo cookies.
	•	Sample size is 36, which is greater than 30, so we assume normality.
	•	Do: Degrees of freedom = 30
	•	Interval: (11.369, 11.4152)
	•	Conclude: We are 90 percent confident that the true mean weight of an Oreo cookie is between 11.369 and 11.4152 grams.

Part B:
If we repeatedly took random samples of 36 Oreo cookies and calculated a 90 percent confidence interval each time, about 90 percent of those intervals would contain the true mean weight of an Oreo cookie.

13
	•	State: Construct a 95 percent confidence interval for the true mean number of pepperonis on a large pizza at the restaurant.
	•	Plan: Use a one-sample t-interval.
	•	Random sample of 10 pizzas.
	•	10 is less than 10 percent of all large pepperoni pizzas made at this restaurant in a week.
	•	The distribution does not show strong skewness or outliers, so normality is assumed.
	•	Do:
	•	Sample mean = 37.4, sample standard deviation = 7.662
	•	Degrees of freedom = 9
	•	Interval: (31.919, 42.881)
	•	Conclude: We are 95 percent confident that the true mean number of pepperonis on a large pizza at this restaurant is between 31.919 and 42.881.

15
Part A:
Checking normality was necessary because the sample size was too small (10 is less than 30).

Part B:
The number 40 is within the confidence interval, so there is no strong evidence that the mean number of pepperonis is less than 40.

Part C:
Melissa and Madeline could either increase the sample size or lower the confidence level. Increasing the sample size would require more resources. Lowering the confidence level is not ideal because a higher confidence level provides greater assurance that the interval contains the population mean.

17
n = 373.26
Select a simple random sample of 374 women.

19
Part A:
19.03 = sample standard deviation divided by square root of 23
Sample standard deviation = 91.26

Part B:
	•	t star = 1, degrees of freedom = 22
	•	The probability of being between -1 and 1: tcdf(-1, 1, 22) = 0.67
	•	The confidence level is 67 percent.

Multiple Choice Answers
21: B
22: E
23: B
24: A
"""

t.sleep(5)
F.auto_type(string)
