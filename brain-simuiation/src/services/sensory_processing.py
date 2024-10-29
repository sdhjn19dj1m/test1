import numpy as np

class SensoryProcessingService:
    def process(self, data):
        """
        處理感官數據
        接收輸入數據並進行處理，返回處理後的數據
        """
        # 將數據轉換為 NumPy 陣列進行處理
        sensor_data = np.array(data['sensor_values'])
        
        # 假設進行一些簡單的數據處理，例如標準化數據
        normalized_data = self.normalize(sensor_data)
        
        # 返回處理後的數據
        processed_data = {
            "status": "processed",
            "original_data": data,
            "normalized_data": normalized_data.tolist()
        }
        return processed_data

    def normalize(self, data):
        """
        標準化數據
        將數據標準化到 [0, 1] 範圍內
        """
        min_val = np.min(data)
        max_val = np.max(data)
        normalized_data = (data - min_val) / (max_val - min_val)
        return normalized_data
