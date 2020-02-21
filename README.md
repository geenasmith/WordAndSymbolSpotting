# WordAndSymbolSpotting
Word and symbol recognition project for ECE471 (Spring 2020).   
  
Based on the paper "*Word and Symbol Spotting Using Spatial Organization of Local Descriptors*" by M. Rusiñol and J. Lladós.  
  
  
## Data structure
To ensure the data can be read and parsed, ensure the top-level directory passed into the dataLoader.py is formatted in the following way:  
```
.  
+--- queries/
|    +--- query1.jpg  
|    +--- query2.jpg  
+--- train/  
|    +--- data/  
|         +--- data1.jpg  
|         +--- data2.jpg  
|         +--- data3.jpg  
          ...  
|    +--- label/  
|         +--- data1.csv  
|         +--- data2.csv  
|         +--- data3.csv  
          ...  
+--- test/  
|    +--- data/  
|         +--- data4.jpg  
|         +--- data5.jpg  
          ...  
|    +--- label/  
|         +--- data4.jpg  
|         +--- data5.jpg  
          ...  
```  
The csv files in the label/ directories map to the jpg files in the data/ directory for use in evaluateAlgorithm.py.  
CSV files should be in the following format:  
```
query1,x1,y1,x2,y2
query2,x1,x2
etc
```  
Where query1, and query2 map to the jpg images in the queries directory, and the (xi,yi) values map to the location of the query symbol within the corresponding image. For a concrete example, see [dataSet/train/label/img-03.csv](./dataSet/train/label/img-03.csv).  
  

---
[Josh McIntosh](https://github.com/joshmcintosh) and [Geena Smith](https://github.com/geenasmith)