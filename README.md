# achtung-die-PLE
Download anaconda or miniconda or something similar.   

Clone the repo   
Create an environment using the file dml_game_env.yml and activate it   
```
conda env create -f dml_game_env.yml
source activate dml_game
```

Install the gym-achtung with pip   

```
cd gym_achtung
pip install -e .
```


# Play against agent
```
python achtungdiekurve_againstplayer.py
```

# Play against yourself
```
python achtungdiekurve_humanplayer.py
```
