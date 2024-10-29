from flask import Flask, request, jsonify
from services.sensory_processing import SensoryProcessingService
from services.memory_service import MemoryService
from services.decision_making import DecisionMakingService

app = Flask(__name__)

# 初始化各個服務
sensory_service = SensoryProcessingService()
memory_service = MemoryService()
decision_service = DecisionMakingService()

@app.route('/sensory', methods=['POST'])
def sensory():
    "" "
    Sensory processing endpoint
    Receive sensory data and process it
    "" "
    # 接收來自客戶端的 JSON 數據
    data = request.json
    
    # 使用感官處理服務對數據進行處理
    response = sensory_service.process(data)
    
    # 返回處理結果作為 JSON 響應
    return jsonify(response)

@app.route('/memory', methods=['POST'])
def memory():
    "" "
    Memory Services
    Receive data and store storage
    "" "
    data = request.json
    response = memory_service.store(data)
    return jsonify(response)

@app.route('/decision', methods=['POST'])
def decision():
    """
    Decision Services
    Receive data and make decisions
    """
    data = request.json
    response = decision_service.decide(data)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
