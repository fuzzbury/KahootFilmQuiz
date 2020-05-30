# KahootFilmQuiz
Gradual reveal of a film still - players can complete on Kahoot to name it first

### Using it
* Create an account on Kahoot
  * Create a quiz with a load of questions (all will be "What film is this?" and 4 possible answers)
  * Host quiz on zoom with screen share
  * Use this App to do the actual reveal
* This is the Kahoot quiz that goes with the example
	* quiz1
		* https://create.kahoot.it/share/film-tv/85d27bb5-c9b4-47f7-a984-4b1b6e69e0c9

	* quiz2
		* https://create.kahoot.it/share/film-quiz-2/e1a2df11-a264-4ce8-a722-2f15f6113d8f

	* quiz3
		* https://create.kahoot.it/share/film-quiz-3/858cdf4d-d331-44f7-9077-432a4780d5b7
  
![How to use with Kahoot](docs/UsageScreenshot.png?raw=true "How to use with Kahoot")  


### Arguments
If you run it without arguments you get the example clips
To provide your own clips use the directory argument eg
* > python.exe film_round.py --directory C:\Documents\FilmRound20200508

### Prerequisites

You need python and these 2 pip (pip/conda packages)
* pygame  
    * https://pypi.org/project/pygame/
* python dateutil 
  * https://pypi.org/project/python-dateutil/
  * note package name is not just 'dateutil' it is 'python dateutil'


## Acknowledgments

* This tutorial was used as a starting point
  * https://inventwithpython.com/pygame/chapter3.html
