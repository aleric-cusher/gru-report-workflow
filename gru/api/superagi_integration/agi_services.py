from .agi_client_initializer import AGIClientInitializer
from superagi_client import AgentConfig


class AGIServices:
    def __init__(
        self,
        client_initializer_instance: AGIClientInitializer,
    ) -> None:
        if not isinstance(client_initializer_instance, AGIClientInitializer):
            raise TypeError(
                "client_initializer_instance must be of type AGIClientInitializer"
            )

        self.client = client_initializer_instance.get_client()

    def _generate_agent_config(self, data: dict) -> AgentConfig:
        return AgentConfig(
            name=f"{data['company_name']} Company Researcher",
            description="The agent researches the given company. It collects foundational information, rates the company and comes up with an action plan.",
            goal=[
                f"Collect foundational information about the company {data['company_name']} (website: {data['company_website']} ), including the services offered and target market",
                f"The company operates in the {data['industry']} and their goals are: `{data['goals']}`. Conduct a market analysis encompassing the examination of market trends, sizing, growth prospects, and potential risks, while also evaluating the company's market share and its market potential",
                "Search the company's primary competitors, find their website links and compile a list",
                "Look through the competitor websites and compare the company based on all the data collected. Assess brand narrtive, outreach, visibility, impact, originality etc",
                "Rate the company based on all the data collected from 1 to 10 where 1 is the company performing badly as compared to the competition and 10 is the company performing better than the competition",
                "Come up with a detailed action plan for the company to improve their market position",
                "Generate a detailed report with all the above details with proper formatting(Highlighting, bullet points, headings) in a txt file with word limit of 600 words",
            ],
            instruction=["Make sure the data is authentic"],
            agent_workflow="Goal Based Workflow",
            constraints=[
                "If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.",
                "Ensure the tool and args are as per current plan and reasoning",
                'Exclusively use the tools listed under "TOOLS"',
                "REMEMBER to format your response as JSON, using double quotes ("
                ") around keys and string values, and commas (,) to separate items in arrays and objects. IMPORTANTLY, to use a JSON object as a string in another JSON object, you need to escape the double quotes.",
                "When using the webscraper tool make sure the url is accurate",
                "Make sure the report as detailed as possible",
            ],
            tools=[
                {"name": "Google Search Toolkit"},
                {"name": "File Toolkit"},
                {"name": "Web Scraper Toolkit"},
            ],
            iteration_interval=500,
            max_iterations=10,
            model="gpt-4",
        )

    def create_agent(self, data: dict) -> int:
        agent_config = self._generate_agent_config(data)
        agent = self.client.create_agent(agent_config=agent_config)
        return agent["agent_id"]

    def run_agent(self, agent_id: int) -> int:
        run = self.client.create_agent_run(agent_id)
        return run["run_id"]

    def create_and_run_agent(self, data: dict) -> list[int, int]:
        agent_id = self.create_agent(data)
        run_id = self.run_agent(agent_id)
        return agent_id, run_id

    def pause_agent(self, agent_id: int, run_id: int) -> bool:
        result = self.client.pause_agent(agent_id=agent_id, agent_run_ids=[run_id])
        return True if result["result"] == "success" else False

    def resume_agent(self, agent_id: int, run_id: int) -> None:
        pass

    def check_run_status(self, agent_id: int, run_id: int = None):
        pass
