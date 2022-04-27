# Introduction

An interactive (and eventually visual) discrete simulation of a custom factory layout defined by the user. Users will be able to specify factory machines and entities in their desired tree or graph structure and customize the machines' time to finish distributions and probability of failure.

Upon running the simulation, jobs are created at user-specifed randomly distributed intervals and are passed through the factory graph from JobSource to JobSink. The simulation collects statistics on each job's throughput and latency, including the breakdown of how much time is spent waiting (in a queue for a machine), processing, or idle (waiting for the next machine, blocking execution).

# Getting Started

Requirements: Python 3.8.0 and the required libraries in `docker/requirements.txt`

TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:

1. Installation process
2. Software dependencies
3. Latest releases
4. API references

# Build and Test

(For Now):  
Run `make run` to run the simulation.
For now, the main method is in `factory.py`, but the Factory object will eventually provide an API to initialize the factory and run the simulation.

# Contribute

To add features or fix a bug, create your own branch from main and open a Pull Request upon finishing. PR's will be subject to code review and shall be **Squash Merged** into the main branch.

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:

- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
