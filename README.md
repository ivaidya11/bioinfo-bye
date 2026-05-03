# Broaden Your Experience Project:
#### Lucía Calzado - 5684226

## How to run it
After you have cloned the repository to your local machine, follow these steps to run the project:

Navigate to this repository (outside of src still). Then run these commands to create and activate the virtual environment:

````
conda env create -f environment.yml
conda activate bye-bioinfo
````

Then, also from this location, and with the environment active, run:

```
python -m src.main
```

The window should pop up.

## What to do with it
The game window opens to an introductory window where the grade level can be chosen. This determines which sequences are used, and how fast they appear (tuning the difficulty).

After clicking on a grade level, the instructions are shown in another window. Click "ok" to move on to the game. Once the game has started (after a couple of seconds), sequences appear in the purple box at the top. Drag and drop these sequences into the dropping boxes (four rectangles of different colors). Try to put all sequences of the same cluster in the same box.

If you need to access the instructions again, click on the "Info" button at the bottom left. Once you are done, click on the "Finish" button at the bottom right to launch the final explanation window.

## Proposed changes
There are many avenues to expand and improve the game. These are my suggestions of how to continue:

- Incorporate code to keep track of which sequences are at each dropping box.

*I think this is the most important upcoming change. Adding an updating dictionary that keeps track of the sequences in each dropping box would allow these to be compared to the correct dictionary (which can be obtained with the methods in src/models/sequence_file) and get a number of accurate guesses. This should be incorporated into a points system to get the game a way to win it.*

- Fix the counter to be a working stopwatch.

*Right now, the counter is not working, and confuses the players. It makes sense to change it to a stopwatch to also introduce some perceived time constrain, and hence more investment.*

- Split up text into panels or reduce.

*The text felt long to most of the students. I think splitting it up into more panels, adding some visuals, and making the text font and color a bit better would be a good improvement, since the instructions weren't clear to a lot of the students, indicating that they didn't read it all the way through.*

- Fix or remove the "Analyze" button.

*The analyze button at the bottom center is what I got the most questions about. The original idea was to make it be a bit like spending time on programming or designing an algorithm, and give the users a time penalty in exhange for changing the color of the sequence blocks to match their correct cluster. I think this could easily become very complicated, but having the button do nothing is confusing, so I think either fix it, or it needs to be removed.*

- Tune the difficulty of the levels

*The difficulty difference between the third and fifth grade levels is not enough at the moment. Most students felt no difference. I think the sequences need to be tweaked: the spèed has little influence at the moment, most students go a lot slower than the spawning (at least in the first few tries)*

## Repository information
```docs``` has all of the documentation for the project, including the project setup (requirements, brainstorming, etc), synthesis of the feedback (as well as the feedback interview notes), and the report.

```src``` has the code for the project. In the ```data```folder, you can find the input files, including the sequences and instruction texts. You can change these as you like (keeping the format). In ```models``` there are some classes used in the project. ```view``` has the user interface files. ```main.py`` executes the application.

In ``testing`` there are some intermediate files for the project, from previous attempts, like the code for the terminal-based version of the game (`functionality_test.py`) or the tetris attempt (unsuccesful).