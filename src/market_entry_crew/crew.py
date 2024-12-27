from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MarketEntryCrew():
	"""MarketEntryCrew crew"""

	@before_kickoff
	def before_kickoff_function(self, inputs):
		print(f"Before kickoff function with inputs: {inputs}")
		return inputs
	
	@after_kickoff
	def after_kickoff_function(self, results):
		print(f"After kickoff function with outputs: {results}")
		return results

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def market_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['market_expert'],
			verbose=True,
			tools=[SerperDevTool()],
		)
	
	@agent
	def company_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['company_expert'],
			verbose=True,
			tools=[SerperDevTool()]
		)
	
	@agent
	def competitor_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['competitor_expert'],
			verbose=True,
			tools=[SerperDevTool()]
		)
	
	@agent 
	def country_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['country_expert'],
			verbose=True,
			tools=[SerperDevTool()]
		)
	
	@agent
	def product_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['product_expert'],
			verbose=True,
			tools=[SerperDevTool()]
		)
	
	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True,
			tools=[]
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def market_research(self) -> Task:
		return Task(
			config=self.tasks_config['market_research'],
			output_file='output/market_research.md'
		)
	
	@task
	def competitor_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['competitor_analysis'],
			output_file='output/competitor_analysis.md'
		)
	
	@task
	def product_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['product_analysis'],
			output_file='output/product_analysis.md'
		)

	@task 
	def country_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['country_analysis'],
			output_file='output/country_analysis.md'
		)
	@task
	def company_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['company_analysis'],
			output_file='output/company_analysis.md'
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='output/report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the MarketEntryCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
