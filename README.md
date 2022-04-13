# Installation
https://p5.readthedocs.io/en/latest/install.html

https://p5.readthedocs.io/en/latest/install.html#windows  
The most important prerequisit is this glfw binary, once it's added you can just 
```bash
 pip install p5
 ```  
If you're having issues with the pillow dependancy on p5 then try updating 
```bash
pip install --upgrade pip
```  

## Profiling
To generate the profiles, run the following commands  
```bash
python -m cProfile -o fast_boid.prof .\fast_boid\fast_profile_main.py  
python -m cProfile -o slow_boid.prof profile_main.py
```

### Snakeviz
To start the snakeviz server and open the profile just run
```
snakeviz .\slow_boid.prof
```