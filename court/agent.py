import os
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent

MODEL_NAME = os.getenv('ADK_MODEL', 'gemini-2.0-flash-001')

# 検事エージェント
def create_prosecutor():
    return LlmAgent(
        name="Prosecutor",
        model=MODEL_NAME,
        description="事件の主張と証拠を提示する検事エージェントです。",
        instruction="あなたは検事です。事件の主張や証拠を提示し、被告の有罪を主張してください。"
    )

# 弁護士エージェント
def create_lawyer():
    return LlmAgent(
        name="Lawyer",
        model=MODEL_NAME,
        description="被告を弁護し反論を行う弁護士エージェントです。",
        instruction="あなたは弁護士です。被告を弁護し、検事の主張に反論してください。"
    )

# 裁判官エージェント
judge = LlmAgent(
    name="Judge",
    model=MODEL_NAME,
    description="議論を監督し、最終的な判決を下す裁判官エージェントです。",
    instruction="あなたは裁判官です。検事と弁護士の議論を監督し、十分な議論がなされたと判断したら最終的な判決を下してください。"
)

# 検事・弁護士のやりとりを3回繰り返すLoopAgent
debate_loop = LoopAgent(
    name="DebateLoop",
    description="検事と弁護士が3回議論を繰り返すループエージェントです。",
    sub_agents=[create_prosecutor(), create_lawyer()],
    max_iterations=3
)

# ループ後に裁判官が判決を出すSequentialAgent
Court = SequentialAgent(
    name="Court",
    description="検事・弁護士の議論の後、裁判官が判決を下す裁判エージェントです。",
    sub_agents=[debate_loop, judge]
)

root_agent = LlmAgent(
    name="RootAgent",
    model=MODEL_NAME,
    description="裁判エージェントのルートエージェントです。",
    instruction="あなたは裁判エージェントのルートエージェントです。",
    sub_agents=[Court]
)
