# El Mordiscos Insurance

![logo_enterprise](./ElMordiscos_insurance.webp)

For our project, we have based it on a travel insurance company that needs to analyze shark attacks by country, examining whether there is a correlation with gender, month of the year, and location.

The program uses the dataset [shark attacks](./GSAF.csv), which is uncleaned.

In [main.py](./main.py), the focus is on data cleaning. For dates, it uses regex patterns (see [regex documentation](https://docs.python.org/3/library/re.html)). During this process, some rows do not match these patterns and their values will be changed to NaN, resulting in the entire column having two formats: datetime and NaN.
In [main.py](./main.py), we also use a new technology called Ollama, specifically the 'mistral' model. Ollama is an NLP ('Natural Language Processing') tool from Meta, which allows us to interpret categorical variables and classify them as we see fit. In this case, all values in the 'Injury' column are classified as 'Fatal', 'Non-Fatal', and NaN.
For the 'Age' column, all numeric values are transformed into age ranges such as 'Child', 'Teen', 'Adult', and 'Senior'.

[final.ipynb](./final.ipynb) is a Jupyter notebook that makes it much easier to work with and create visualizations.

# Conclusions:

These graphs are created using the matplotlib library.
![graphic_1](./graphic_1.jpg)
This graph shows the countries with the most shark attacks, which are the USA, Australia, and South Africa.

Hypothesis: Do attacks vary depending on the month?
![graphic_2](./graphic_2.jpg)
This graph shows the difference in shark attacks in the USA, Australia, and South Africa. The USA, being in the northern hemisphere, shows a bell curve, indicating that the warmer months have more attacks. Meanwhile, South Africa and Australia, being in the southern hemisphere, show an inverted bell curve, as the warmer months are during the northern hemisphere's winter.

Hypothesis: Does gender and age have an impact?
![graphic_3](./graphic_3.jpg)
The graph shows a significant peak in adult males, which could be due to more men engaging in high-risk sports such as surfing and diving. These sports are also predominantly practiced by adults.

Hypothesis: Which country has the highest mortality rate percentage?
![graphic_4](./graphic_4.jpg)
This graph includes countries with more than 25 cases, as there are many countries in the dataset with only one attack, which doesn't make sense to include in the graph.
To make the comparison fairer, the mortality rate percentage calculation takes the total number of fatalities, divides it by the total number of cases, and multiplies by 100, rounding to two decimal places.
