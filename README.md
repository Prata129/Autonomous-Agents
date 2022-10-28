# MultiAgentCooperativeGridSweep

A Python implementation of a Multi Agent System whose purpose is to clean an environment full of trash. Different types of agents were developed in order to test the efficiency of each one in our environment. In order to accomplish the task, the team of agents must clean all the trash in a limited amount of steps while avoiding the obstacles.

## Getting Started

### Installation

1. Install requirements
  ```sh
   pip install -r requirements.txt
  ```

## Run the project

The simplest way to run the project with the default settings is by running the follow command:
```sh
 python3 main.py --render
```

However, in case you want to change some settings, you can do that by adding --flag=value the previous command.

List of the existing flags:
  * episodes
  * width
  * height
  * uncertainty
  * render
  * episodes_per_training
  * episodes_per_evaluation
  * evaluations

The flags all work with integers except the uncertainty which works with floats and render which only is used if we want to see the grid. In case we only want the results we remove the render flag.

## Work Distribution

All work was developed equally by all members of the group and all members worked together to face the adversities of the project.
