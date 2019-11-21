# BodySlide-Group-Generator
This is a short Python Script to compare installed BS outfits and automatically generate SliderGroups for those that don't exist.

##  Abstract:



## Introduction:



## Task List

# Errors:
- Wrong Set folder location (Check for detection of Set format xml/osp files)
- Wrong Group folder location (Check for detection of Set format xml files)-
- Check for Presence of the above paths in config.xml, if not present, ask f-or them
- Check for Presence of Masterlist


# Planned Features:
- Select CBBE/UNP/Agnostic Mode to allow for checking of outfits that dont conform to the bodytype used in a game.
-A utomatic Grouping of Ungrouped Outfits with reasonable names
-Load and Consolodation of SliderGroups to one Group File
- Option to Comprise Masterlist of only nongrouped outfits

# Planned Modules/Tools    
- Automatically Copy specified preset across all existing outfits

#### Hardware Specs:

|     |Laptop| Desktop |
| --- | --- | --- |
|Model| 2018 Dell Latitude | Custom |
|CPU| 4x x Intel(R) Core(TM) i5-7300U @2.60GHz | 8x AMD Ryzen 7 1700X @3.40 GHz |
|RAM| 8 GB | 32 GB |
|Hard Disk| 256 GB HDD | 1 TB SSD |
|GPU| Intel HD Graphics 620 | ZOTAC 1080 TI |

#### Software Environment:

|     |Laptop| Desktop |
| --- | --- | --- |
|OS| Windows 10 Pro (16299.1087) x64 | Windows 10 Home () x64 |
|Python|3.8.0 x32  | 3.8.8 x64|
|lxml| - | - |
|requests| - | - |
|GPU| - | - |

Example Build Command (VSCODE)

C:\....\BodySlide-Group-Generator> C:\....\.venv35\Scripts\pyinstaller.exe --onefile cli.py --name BSGG