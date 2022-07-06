# noise
Noise Generator Experiment

Simplex noise was too slow so I created a simpler 3D noise generator for my purpose

![Output sample](https://github.com/textmmorpg/noise/blob/main/noise.gif)

# 20 seconds faster for a 100x100x100 grid

Note: this was not a rigorous test, just the first run, but I think the difference is significant

```
python3.9 main.py 
Execution time in seconds: 14.121574401855469
```

```
$ python3.9 comparison.py # opensimplex
Execution time in seconds: 35.637431144714355
```

