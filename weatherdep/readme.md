# Simple display of current temperature

Temperature data parsed from *drops.live*. The temperature is colored based on its value. Script also scrapes the weather icon. 

## Usage
Data are displaying based on url:
* Current temperature for Zielona Góra
    
        {HOST}/temperature/zielona_gora

* Current temperature based on geographical coordinates.

        {HOST}/temperature/current/<longitude>,<lattitude>/

        # Example
        {HOST}/temperature/current/40.0,20.0/
    
___


## Screenshots

* Weather for Zielona Góra

![Temperature for Zielona góra](https://kamilkorczak.pl/images/temperature-zg.png)


* Weather based on geographrapical coordinates (longitude=40.0, lattitude=20.0)

![Temperature for sample coordinates](https://kamilkorczak.pl/images/temperature-ol.png)