import os
from google.adk.agents import LlmAgent

MODEL_NAME = os.getenv('ADK_MODEL', 'gemini-2.5-flash-preview-05-20')

# サブエージェントを3つ作成
agent1 = LlmAgent(
    name="agent1",
    model=MODEL_NAME,
    description="親切な答えを返します",
    instruction="あなたは親切なアシスタントです。"
)

agent2 = LlmAgent(
    name="agent2",
    model=MODEL_NAME,
    description="イジワルな答えを返します",
    instruction="あなたはイジワルなアシスタントです。"
)

agent3 = LlmAgent(
    name="agent3",
    model=MODEL_NAME,
    description="論理的な答えを返します",
    instruction="あなたは論理的なアシスタントです。"
)

# 3つのサブエージェントを持つTestAgentを作成
TestAgent = LlmAgent(
    name="TestAgent",
    model=MODEL_NAME,
    description="3つのLLMAgentをまとめるテスト用エージェントです。",
    instruction="あなたは3つのサブエージェントをまとめるコーディネーターです。",
    sub_agents=[agent1, agent2, agent3]
)

root_agent = TestAgent