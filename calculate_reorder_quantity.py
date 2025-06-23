import json
import os

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReorderQuantityRequest(BaseModel):
    current_inventory: int
    historic_data: int
    forecast: int


# WatsonX LLM Initialization
llm = LLM(
    api_key=os.environ["WATSONX_API_KEY"],
    model=os.environ["MODEL_ID"],
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 10000,
        "temperature": 0,
        "repetition_penalty": 1.05,
    },
)


# Inventory Optimization Agent
def create_inventory_agent():
    return Agent(
        role="Inventory Optimizer",
        goal="Determine optimal reorder quantity to maintain ideal stock levels.",
        backstory="""당신은 AI 기반 재고 관리자입니다. 과거 추세와 예측된 수요를 사용하여 
        재주문 수량을 계산하는 것이 목표입니다. 재고 부족을 방지하면서도 과잉 재고를 
        예방해야 합니다. 데이터 패턴을 기반으로 결정 사항을 설명하세요.
        
        중요: 모든 응답은 반드시 한국어로 작성하세요.""",
        llm=llm,
        allow_delegation=False,
    )


# Task Definition
def create_inventory_task(agent, current_inventory, historic_data, forecast):
    return Task(
        description=f"""
다음 데이터가 주어졌습니다:
- 현재 재고: {current_inventory}
- 전월 판매량: {historic_data}
- 다음 달 예상 판매량: {forecast}

충분한 재고를 확보하면서도 과잉 재고를 최소화할 수 있는 최적의 재주문 수량을 결정하세요.

최적 재주문 수량 계산 지침:
1. 부족량 계산
    - 부족량 = 예상 판매량 - 현재 재고
2. 안전 재고 계산
    - 부족량 <= 전월 판매량인 경우:
        안전 재고 = 전월 판매량의 10%
        재주문 수량 = 부족량 + 안전 재고
    - 부족량 > 전월 판매량인 경우:
        재주문 수량 = 부족량

JSON 형식으로 구조화된 응답을 제공하세요:
1. "reorder_quantity": 재주문 수량을 나타내는 정수
2. "reasoning": 이 재주문 수량을 선택한 이유에 대한 상세한 설명 (한국어로 작성)
        """,
        expected_output="""A JSON object: 
        {
          "reorder_quantity": <integer>,
          "reasoning": "<string explanation>"
        }""",
        agent=agent,
    )


@app.post("/calculate-reorder-quantity")
def calculate_reorder_quantity(request: ReorderQuantityRequest):
    inventory_agent = create_inventory_agent()
    inventory_task = create_inventory_task(
        inventory_agent,
        request.current_inventory,
        request.historic_data,
        request.forecast,
    )

    # Create and execute CrewAI workflow
    inventory_crew = Crew(
        agents=[inventory_agent],
        tasks=[inventory_task],
        process=Process.sequential,
        verbose=True,
    )

    response = str(inventory_crew.kickoff()).strip()
    response = json.loads(response)
    return {
        "reorder_quantity": response["reorder_quantity"],
        "reasoning": response["reasoning"],
    }
