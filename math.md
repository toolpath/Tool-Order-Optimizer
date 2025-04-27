# Math behind this 

This section is written down to keep notes for myself so I can remember what Im doing if I have to come back to this. 
You Don't need to read it. 


- Given a circular platter with M spaces in it.
- Fill up N (where N <= M) places with tools. 
- Given a tool squence, order the tools to minimize the total time spent rotating the platter 


The simplest form of this problem is the Mimimum Linear Arrangement form, which can be solved exactly using a linear solver. 
However, the reality that its a circular turret means that its really a Circular Mimnimum Distance problem which can only be solve approximately. 