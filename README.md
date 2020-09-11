`````                     
                           |`-:_
  ,----....____            |    `+.
 (             ````----....|___   |
  \     _                      ````----....____
   \    _)                                     ```---.._
    \                                                   \
  )`.\  )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.   )`.   )
-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `-'   `

------------------------------------------------
`````
# The Sub: Expeditionary VLSM Calculator
This application can calculate IPv4 subnets for complex networks in resource constrained runtimes.

Because U.S. Government computers have restrictions on the applications that administrators can install. 
This software does not require any compiling and does not write to the system allowing for usage on any government computer.
###### Features
- Only requires python interpreter 
- Made with security in mind.
- Does not require external modules. Tabulate module is optional.
- Outputs in CSV format for easy import to Excel.
- Can calculate up to 40 subnets.

###### FAQ
- **Why are the IP addresses outputted with commas and brackets?** _The IP addresses are stored and operated upon in a list format. The format is preserved for output into other applications if needed._
- **Why python and not java or C?** _Most government computers have python installed and can run simple scripts, but cannot support additional moduals. The Sub does not have any external dependencies other than the "Tabulate" module._
- **What happens if I don't copy or want to use Tabulate?** _The Sub will still work without tabulate. But you will need to import the output into Excel to view the output in a human readable format._
-** What is CSV? **_Comma Seperated Values (CSV) is a file format for storing spreadsheet data. CSV files are saved in a text file and opend in spreadsheet software._

## How to Install
0) Create a directory to save the calculator and required modules. If possible, you can fork or clone this repo. But this instruction set assumes that git is not available on your machine.
1) Copy and paste the the **main.py** file into a text document on your local machine. Save the file as a ```.py``` extension.
2) Optional: Copy and paste the **tabulate.py** file in the same directory. If you do not copy the tabulate module, The Sub will only output a CSV format.
3) In powershell or CMD Prompt, navigate to the directory with the file.
4) Enter the following command:
```py main.py```
5) Follow the prompts. 

## Usage
1) Enter your network IPv4. The Sub will not subnet IPv6.
2) Enter your subnet mask in dotted decimal or CIDR in slash notation.
3) Enter the desired amount of subnets. The Sub is tested up to 40 subnets, but can probably go higher.
4) Enter the common name for your network. Any easy to remember Alpha Numeric string is acceptable.
5) Enter the number of hosts required for the network. Include network devices (switches, firewalls). DO NOT Include broadcast or network address, the calculator will account for those addresses.
![Screencap of CLI for The Sub](https://github.com/TheMagicNacho/subnet/blob/master/archive/img/screencap.PNG)

## Excel Integration
1) Highlight and copy the CSV output.
2) Paste the text into a notepad.
3) Save the text file with a ```.csv``` extension.
4) Open Excel.
5) Navigate to the Data tab.
6) Click, "From Text/CSV"
7) Select your file, click import on the bottom right of the window.
8) On the top drop down "delimiter", choose colon.
9) Click import. 
![Import Tabs on Excel](https://github.com/TheMagicNacho/subnet/blob/master/archive/img/excel_screencap.PNG)
_Location of Data tab and CSV import button._
![Excel Import settings](https://github.com/TheMagicNacho/subnet/blob/master/archive/img/import.PNG)
_Required import settings for CSV in Excel._


