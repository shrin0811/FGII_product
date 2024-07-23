# FGII product

## How to install and make it work? 

`Unfortunately, as the front-end of this product has not been made, some basic coding knowledge is required to make the program run.`

Ensure that you have Python installed on your device. Any version beyond Python 3.12.0 will work. If not you can install the software [here](https://www.python.org/downloads/). 
Once you have installed Python, follow the instructions below:
- Go to `grade_policy.py` and download the file. **Do NOT RENAME THE FILE.**
- Open your Terminal/PowerShell/Command Prompt (for Windows users) and Bash (for MacOS users).
- Ensure that your terminal/bash directory is the same as the file in which `grade_policy.py` has been downloaded/saved in.
- Write the following command: `python grade_policy.py 'output_filename.csv'` -- in this case, replace 'output_filename' with the filename that you would want the Excel sheet to be saved as.
- Answer the prompts as asked. 

## What does the product do? 
As a part of my summer internship I was tasked to create a model that objectively grades 100+ insurance policies across the Indian insurance market, thus allowing the company to not only conduct a market survey of existing products but also understand the needs and concerns of the consumer base. 

## What are the steps to making the product work? 
- Step 1: Choose whether you want to check existing policies or add a new policy
   - 1.1: In case you want to check a new policy, it will see whether the file storing policy data is empty or not. If empty it will ask you to add at least one policy. If not, it will ask you which policies to show, as per requirement.
   - 1.2 If you want to add a new policy, it will give you a series of prompts to enter family and policy details.
- Step 2: Entering family details
- Step 3: Entering policy details
- Step 4: Ranking the marking criteria as per the family's needs
- Step 5: Processing and calculation
- Step 6: Display of final score and asking for final comments on the policy
- Step 7: Automatic addition of the policy name, score, letter grade and comment to a `.csv` file.

The `.csv` file can be checked in the working directory - i.e. the location where the program is being run from. 
