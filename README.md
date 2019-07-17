# Geo utils
A collection of python command-line scripts for operations on 2D coordinates, specifically using CAD-related files.

## Getting Started
Simply clone this repo in your system, then create and activate a python virtual environment for it.

### Prerequisites
- python 3
- everything specified in `requirements.txt`.

(if you have problems installing package wxPython see [here](https://wiki.wxpython.org/How%20to%20install%20wxPython))

## Down To Business
Each script has a very specific funcionality and also a strict I/O file handling.
Inside the folder `data_samples` are stored files to test the scripts. (so you can have a clue of what this scripts are for)

### Script #1: Match Distance

>  Return a list of same-distance points couples from a file of 2D points.

Usage:

```
python match_distance.py -i  <inputfile> -o <outputfile>
```

Example:
```
python match_distance.py -i data_samples/point_coordinates.txt -o my_matches.txt
```

### Script #2: XML Filler

> Update an xml file with the points given as input.

Usage:

```
python xml_filler.py -x <input_xml> -p <input_points> -o <outputfile>
```

Example:
```
python xml_filler.py -x data_samples/riflettori_utf8.xml -p data_samples/point_coordinates.txt -o my_filled-xml.xml
```

### Script #3: Swap Coordinates

> Replace x, y coordinates of lmk input file with new ones read in csv input file. Return a lmk updated file as outputfile.

Usage:

```
python swap_coordinates.py -i <lmkfile> -s <swapfile> -o <outputfile>
```

Example:
```
python swap_coordinates.py -i data_samples/Layoutnew2.lmk -s data_samples/PF1819_d.txt -o data_samples/final_swap.lmk
```

### Script #4: Out To Dxf

> Create a .DXF file from a .OUT one.

Usage:

```
python out_to_dxf.py -i <inputfile> -o <outputfile>
```

Example:
```
python out_to_dxf.py -i data_samples/02651.OUT -o testdxf.dxf
```

### Script #5: Translate lmk

> Translate by given deltas (input via command line) the 2D coordinates in the lmk file.

Usage:

```
python trans_lmk.py -i <lmkfile> -o <outputfile>
```

Example:
```
python trans_lmk.py -i data_samples/Layout190701.lmk -o data_samples/Layout_translated.lmk
```
