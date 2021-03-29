# sudokuSolver
Simple Sudoku solver

This is a little solver for Sudoku puzzles.  
On input you provide sequence that represent given field,
in return sudokuSolver gives you calculated solution for it.  


#### Setting initial state
You can specify puzzle's values as a string of 81 char - (9 chars for each row) * 9 rows like:  
```python
#            row_1___|row_2___|row_3___|row_4___|row_5___|row_6___|row_7___|row_8___|row_9___|
field_str = "500006000100000006460000008210050000040807050050000400004010000001300800005002700"  
```  
or as a matrix of size 9 * 9, e.g.:
```python
matrix = [
            [5, 0, 0, 0, 0, 6, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 6],
            [4, 6, 0, 0, 0, 0, 0, 0, 8],
            [2, 1, 0, 0, 5, 0, 0, 0, 0],
            [0, 4, 0, 8, 0, 7, 0, 5, 0],
            [0, 5, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 4, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 3, 0, 0, 8, 0, 0],
            [0, 0, 5, 0, 0, 2, 7, 0, 0]
         ]
```
Empty point is specified as zero.  

##### Sample use:
```python
>>> from sovler import Solver  
>>> s = Solver()  
>>> s.enter_from_str("000090010800000062000072009600010480000809000085030007900560000470000006030040000")  
>>> s.solve()
-------------------------------
| .  .  . | .  9  . | .  1  . |
| 8  .  . | .  .  . | .  6  2 |
| .  .  . | .  7  2 | .  .  9 |
-------------------------------
| 6  .  . | .  1  . | 4  8  . |
| .  .  . | 8  .  9 | .  .  . |
| .  8  5 | .  3  . | .  .  7 |
-------------------------------
| 9  .  . | 5  6  . | .  .  . |
| 4  7  . | .  .  . | .  .  6 |
| .  3  . | .  4  . | .  .  . |
-------------------------------
Solution was found on step #0
-------------------------------
| 2  6  4 | 3  9  8 | 7  1  5 |
| 8  9  7 | 1  5  4 | 3  6  2 |
| 3  5  1 | 6  7  2 | 8  4  9 |
-------------------------------
| 6  2  9 | 7  1  5 | 4  8  3 |
| 7  4  3 | 8  2  9 | 6  5  1 |
| 1  8  5 | 4  3  6 | 9  2  7 |
-------------------------------
| 9  1  8 | 5  6  3 | 2  7  4 |
| 4  7  2 | 9  8  1 | 5  3  6 |
| 5  3  6 | 2  4  7 | 1  9  8 |
-------------------------------
'solve'  90.00 ms

```  

#### Getting puzzles from web
There is a routine to get new Sudoku puzzles from web:
```python
from from_web import matrix_from_web, get_from_web
from sovler import Solver 
matrix = matrix_from_web(get_from_web())

s = Solver()
s.enter_values(matrix, solve=False)
print(s.initial_field)
-------------------------------
| 2  5  . | .  6  . | .  4  . |
| .  7  3 | 4  .  2 | .  1  . |
| 4  .  6 | .  .  7 | .  .  5 |
-------------------------------
| 6  .  8 | 1  .  . | .  .  7 |
| .  .  . | 7  3  9 | 4  .  6 |
| 9  4  7 | .  .  6 | .  3  1 |
-------------------------------
| 7  .  . | .  .  . | 3  .  4 |
| .  6  . | 8  .  4 | .  5  . |
| .  1  4 | .  2  . | 9  7  8 |
-------------------------------
```
Current source is http://www.cs.utep.edu/cheon/ws/sudoku/new/
