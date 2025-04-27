# Optimize Your Tool Ordering

If you use a carrosel or turret style tool changer, and want to minimize the overall time spent tool changing then this script helps solve that. 

There are two versions of the script. One that uses Scipy and one that uses pure python. 
Both of them implement the same optimization of the "Lazy Susan Problem" (so named by Justin Gray and CJ Abraham)

In both cases you'll edit the bottom of the script where it says 

```python
    #######################################
    # Edit this to match your tool numbers
    #######################################
    TOOL_SEQUENCE = [1,13,1,35,17,33,31,29,34,1,37,13,30,8,1,13,8,15]
    M = 28  # your plate size

    sa_solve(TOOL_SEQUENCE, M)
```

then from a terminal call the python script. 

# Pure Python (start here)
Use this one if you don't know how to install Scipy into your python installation 

`python tool_ordering.py`


# Scipy Version
While I haven't done extensive testing, the Scipy simulated annealing solver should be better than the simple one ChatGPT built for me in the pure python one. 
So if you want a better optimizer, install scipy and use this one. 

`python tool_ordering.py`