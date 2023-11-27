from .agent_status import AgentStatus
from .agi_client_initializer import AGIClientInitializer
from superagi_client import AgentConfig, AgentRunFilter


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
        json_template = (
            "{\n"
            '   "title": "{company_name} Report",\n'
            '   "headings": [\n'
            '       {"heading": "Company Overview", "content": "{company_overview}"},\n'
            '       {"heading": "Market Analysis", "content": "{market_analysis}"},\n'
            '       {"heading": "Competitor Analysis", "content": "{competitor_analysis}"},\n'
            '       {"heading": "Comparative Analysis", "content": "{comparative_analysis}"},\n'
            '       {"heading": "Rating", "content": "{company_rating}"},\n'
            '       {"heading": "Action Plan", "content": "{action_plan}"},\n'
            "   ]\n"
            "}"
        )

        return AgentConfig(
            name=f"{data['company_name']} Company Researcher",
            description="The agent researches the given company. It collects foundational information, rates the company and comes up with an action plan.",
            goal=[
                f"Collect foundational information about the company[{data['company_name']}] given their website[{data['company_website']}, including services offered, target market, and any other relevant details.",
                f"Conduct a comprehensive market analysis for in the {data['industry']}. Include market trends, sizing, growth prospects, potential risks, market share, and potential.",
                "Research and compile a list of primary competitors, including their websites.",
                "Conduct a comparative analysis of competitors, focusing on brand narrative, outreach, visibility, impact, and originality.",
                "Rate the company on a scale of 1 to 10 based on the collected data, where 1 indicates poor performance compared to competitors, and 10 indicates superior performance.",
                f"Generate a detailed action plan for the company to improve its market position and to achieve their goals[{data['goals']}], incorporating findings from the analysis.",
                f"Create a well-formatted and detailed report (in a json file) using the following template:\n\n{json_template}",
            ],
            instruction=[
                "Use the provided template for the generated report to ensure a consistent and reproducible structure. Substitute placeholders ({company_name}, {company_overview}, {market_analysis}, etc.) with the actual information gathered during the process. All the headings and placeholders in the template are necessary.",
                "Generate detailed content for each section of the report. Provide comprehensive information, elaborate on key points, and ensure that the content is sufficiently detailed to convey a thorough understanding of each aspect. Aim for clarity and depth in your responses, using complete sentences and additional context where necessary.",
                "Ensure the authenticity of the collected data.",
                "Focus on the indian context when researching.",
                "Elaborate on market analysis, covering key aspects identified in the goal.",
                "Offer detailed guidance on action plan elements and strategic recommendations.",
                "Verify the accuracy of the URL when using the webscraper tool to ensure the collected data is relevant and reliable.",
            ],
            agent_workflow="Goal Based Workflow",
            constraints=[
                "If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.",
                "Ensure the tool and args are as per current plan and reasoning",
                'Exclusively use the tools listed under "TOOLS"',
                'REMEMBER to format your response as JSON, using double quotes ("") around keys and string values, and commas (,) to separate items in arrays and objects. IMPORTANTLY, to use a JSON object as a string in another JSON object, you need to escape the double quotes.',
                "Strive for detailed content, considering all relevant aspects.",
            ],
            tools=[
                {"name": "Google Search Toolkit"},
                {"name": "File Toolkit"},
                {"name": "Web Scrapper Toolkit"},
            ],
            iteration_interval=500,
            max_iterations=25,
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

    def resume_agent(self, agent_id: int, run_id: int) -> bool:
        result = self.client.resume_agent(agent_id=agent_id, agent_run_ids=[run_id])
        return True if result["result"] == "success" else False

    def check_run_status(self, agent_id: int, run_id: int) -> AgentStatus:
        filter = AgentRunFilter(run_ids=[run_id])
        status = self.client.get_agent_run_status(agent_id, agent_run_filter=filter)
        return AgentStatus[status["status"]]

    def get_resource_url(self, run_id: int) -> str:
        resource_dict = self.client.get_agent_run_resources(agent_run_ids=[run_id])
        return resource_dict[str(run_id)][0]
