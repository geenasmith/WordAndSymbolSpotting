# WordAndSymbolSpotting
Word and symbol recognition project for ECE471 (Spring 2020).   
  
This project is based on the paper "*Word and Symbol Spotting Using Spatial Organization of Local Descriptors*" by M. Rusiñol and J. Lladós. We implemented the described process in order to facilitate querying of both words and symbols from a set of documents in an efficient way without first separating words and graphical symbols.

For a detailed description of our implementation and results, please read our [final report](./documentation/final_report.pdf).
  
## Usage  
1. Clone this repo into your development environment:  
```
git clone https://github.com/geenasmith/WordAndSymbolSpotting.git
```  
2. Install dependencies using pip:  
```
pip install -r requirements.txt
```  
3. Run the program, including the optional randomize argument if the data should be randomized or not:  
```
python3 algRunner.py src/dataSet
  
    or

python3 algRunner.py src/dataSet randomize
```
  
## Data structure
If you wish to use a different data set, make sure it is in the described format to ensure the data can be read and parsed appropriately. The top-level directory which is passed as the second argument when running [algRunner.py](./src/algRunner.py) should formatted in the following way:  
```
.  
+--- queries/
|    +--- query1.jpg  
|    +--- query2.jpg   
+--- data/  
|    +--- data1.jpg  
|    +--- data2.jpg  
|    +--- data3.jpg  
          ...  
+--- label/  
|    +--- data1.csv  
|    +--- data2.csv  
|    +--- data3.csv  
          ...  
```  
The csv files in the [label](./src/dataSet/label) directory maps to the jpg files in the [data](./src/dataSet/data) directory for use in [evaluateAlgorithm.py](./src/evaluateAlgorithm.py).  
CSV files should be in the following format:  
```
query1,x1,y1,x2,y2
query2,x1,y1
etc
```  
Where query1, and query2 map to the jpg images in the queries directory, and the (xi,yi) values map to the location of the query symbol within the corresponding image. For a concrete example, see [src/dataSet/label/img-03.csv](./src/dataSet/label/img-03.csv).  
  

## Contributors
- [Josh McIntosh](https://github.com/joshmcintosh)  
- [Geena Smith](https://github.com/geenasmith)