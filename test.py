import json

import requests


# HTTP requests를 사용한 테스트
def test_api(
    base_url="https://calculate-reorder-quantity.1wpveihz0wfq.us-south.codeengine.appdomain.cloud",
):
    """HTTP requests를 사용한 API 테스트"""
    print("=== 재고 재주문 수량 계산 API 테스트 ===")
    print(f"서버 URL: {base_url}")

    # 테스트 케이스들
    test_cases = [
        {
            "name": "기본 케이스 - 부족분이 과거 판매량보다 적은 경우",
            "data": {"current_inventory": 100, "historic_data": 150, "forecast": 200},
        },
        {
            "name": "부족분이 과거 판매량보다 큰 경우",
            "data": {"current_inventory": 50, "historic_data": 100, "forecast": 300},
        },
        {
            "name": "재고가 충분한 경우",
            "data": {"current_inventory": 500, "historic_data": 100, "forecast": 150},
        },
        {
            "name": "최소 재고 케이스",
            "data": {"current_inventory": 10, "historic_data": 50, "forecast": 80},
        },
        {
            "name": "높은 수요 예측",
            "data": {"current_inventory": 50, "historic_data": 100, "forecast": 400},
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- 테스트 케이스 {i}: {test_case['name']} ---")
        print(f"입력 데이터: {test_case['data']}")

        try:
            response = requests.post(
                f"{base_url}/calculate-reorder-quantity",
                json=test_case["data"],
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                print(f"응답 성공!")
                print(f"재주문 수량: {result['reorder_quantity']}")
                print(f"설명: {result['reasoning']}")
            else:
                print(f"응답 실패: {response.status_code}")
                print(f"오류 메시지: {response.text}")

        except requests.exceptions.ConnectionError:
            print("서버에 연결할 수 없습니다. 서버 URL이 올바른지 확인해주세요.")
            break
        except requests.exceptions.Timeout:
            print("요청 시간이 초과되었습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")


if __name__ == "__main__":
    print("재고 재주문 수량 계산 API 테스트")
    print("=" * 50)

    # API 테스트 실행
    test_api()
