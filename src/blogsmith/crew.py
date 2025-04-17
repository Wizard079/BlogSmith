from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from blogsmith.tools.custom_tool import SaveFileTool , SearchNewsTool , WordSearchingTool
from blogsmith.env import DEBUG

@CrewBase
class Blogsmith():
    """Blogsmith crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def context_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['context_collector'],
            verbose=DEBUG,
            tools=[SearchNewsTool()] 
        )
    
    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator'],
            verbose=DEBUG,
            tools=[WordSearchingTool()]
        )
    
    @agent
    def exporter(self) -> Agent:
        return Agent(
            config=self.agents_config['exporter'],
            verbose=DEBUG,
            tools=[SaveFileTool()]
        )

    @task
    def gather_blog_context(self) -> Task:
        return Task(
            config=self.tasks_config['gather_blog_context'],
        )

    @task
    def write_blog_content(self) -> Task:
        return Task(
            config=self.tasks_config['write_blog_content'],
        )
    @task
    def finalize_and_export(self) -> Task:
        return Task(
            config=self.tasks_config['finalize_and_export'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Blogsmith crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
