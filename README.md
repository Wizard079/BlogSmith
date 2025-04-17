# Blogsmith 

Welcome to the Blogsmith project,BlogSmith is a Python-based AI tool for writing SEO-friendly blog posts, powered by popular APIs and capable of generating content in a specified tone.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```
### Customizing

Add your own **API keys** to the `.env` file for tools and the LLM agent.

## Running the Project

To run the agent, simply execute the [run.sh](./run.sh) script.

Once the agent completes the writing, you can access the logs in the `logs` directory.

The complete output of the writing and its metadata will be saved in the `output` directory.

You can specify the tone of the generated content by adding the `--tone` argument. 

