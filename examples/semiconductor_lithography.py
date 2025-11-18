"""
半導體光刻設備集成示例
展示量子預火光源在光刻機中的應用
"""

import time
import threading
from typing import Dict, List
from src.core.light_source_controller import (
    QuantumLightSourceController, 
    LightSourceConfig, 
    EmissionParameters,
    LightSourceState
)
from src.adapters.device_adapters import DeviceManager, EthernetAdapter

class SemiconductorLithographySystem:
    """
    半導體光刻系統集成
    演示光源在實際生產環境中的應用
    """
    
    def __init__(self):
        # 光源配置 - 針對光刻應用優化
        self.light_source_config = LightSourceConfig(
            wavelength=5.8e-9,      # 5.8nm EUV
            max_power=5.0e-9,       # 5nW 最大功率
            stability_target=0.005, # 0.5% 穩定性要求
            warmup_time=45.0,       # 45秒預熱
            calibration_interval=1800  # 30分鐘校準
        )
        
        # 初始化光源控制器
        self.light_source = QuantumLightSourceController(self.light_source_config)
        
        # 設備管理器
        self.device_manager = DeviceManager()
        
        # 生產狀態
        self.production_state = "IDLE"
        self.current_recipe = None
        self.wafer_count = 0
        
        # 設置回調
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """設置系統回調"""
        self.light_source.register_callback('state_change', self._on_light_source_state_change)
        self.light_source.register_callback('power_update', self._on_power_update)
        self.light_source.register_callback('error', self._on_error)
    
    def initialize_system(self) -> bool:
        """初始化整個光刻系統"""
        print("🔄 初始化半導體光刻系統...")
        
        try:
            # 1. 初始化設備連接
            if not self._initialize_devices():
                return False
            
            # 2. 啟動光源
            if not self.light_source.power_on():
                return False
            
            # 3. 執行系統校準
            if not self.light_source.calibrate():
                return False
            
            print("✅ 光刻系統初始化完成")
            self.production_state = "READY"
            return True
            
        except Exception as e:
            print(f"❌ 系統初始化失敗: {e}")
            return False
    
    def _initialize_devices(self) -> bool:
        """初始化所有外圍設備"""
        # 註冊光刻機主要設備
        devices = {
            "stage_controller": EthernetAdapter("192.168.1.10", 8080),
            "mask_aligner": EthernetAdapter("192.168.1.11", 8080),
            "vacuum_system": EthernetAdapter("192.168.1.12", 8080),
            "temperature_controller": EthernetAdapter("192.168.1.13", 8080),
        }
        
        for device_id, adapter in devices.items():
            self.device_manager.register_device(device_id, adapter, {})
        
        # 連接所有設備
        connection_results = self.device_manager.connect_all()
        
        # 檢查連接結果
        for device_id, connected in connection_results.items():
            status = "✅" if connected else "❌"
            print(f"{status} {device_id}: {'連接成功' if connected else '連接失敗'}")
        
        return all(connection_results.values())
    
    def load_recipe(self, recipe: Dict) -> bool:
        """加載光刻配方"""
        print(f"📁 加載光刻配方: {recipe.get('name', '未知')}")
        
        # 驗證配方參數
        if not self._validate_recipe(recipe):
            return False
        
        self.current_recipe = recipe
        
        # 配置光源參數
        light_params = recipe.get("light_source", {})
        self._configure_light_source(light_params)
        
        print("✅ 配方加載完成")
        return True
    
    def start_exposure(self, wafer_id: str) -> bool:
        """開始晶圓曝光"""
        if self.production_state != "READY":
            print("❌ 系統未就緒，無法開始曝光")
            return False
        
        if not self.current_recipe:
            print("❌ 未加載光刻配方")
            return False
        
        print(f"🚀 開始晶圓曝光: {wafer_id}")
        self.production_state = "EXPOSING"
        
        try:
            # 1. 移動晶圓到曝光位置
            self._move_wafer_to_position(wafer_id)
            
            # 2. 啟動光源發射
            exposure_params = self._get_exposure_parameters()
            if not self.light_source.start_emission(exposure_params):
                return False
            
            # 3. 執行曝光序列
            self._execute_exposure_sequence()
            
            # 4. 停止曝光
            self.light_source.stop_emission()
            
            # 5. 移動晶圓到下一位置
            self._move_wafer_to_unload()
            
            self.wafer_count += 1
            self.production_state = "READY"
            
            print(f"✅ 晶圓曝光完成: {wafer_id} (總計: {self.wafer_count})")
            return True
            
        except Exception as e:
            print(f"❌ 曝光過程出錯: {e}")
            self.production_state = "ERROR"
            return False
    
    def batch_process(self, wafer_list: List[str]) -> Dict:
        """批量處理晶圓"""
        print(f"🏭 開始批量處理 {len(wafer_list)} 個晶圓")
        
        results = {
            "total": len(wafer_list),
            "success": 0,
            "failed": 0,
            "details": []
        }
        
        for i, wafer_id in enumerate(wafer_list, 1):
            print(f"\n--- 處理進度: {i}/{len(wafer_list)} ---")
            
            start_time = time.time()
            success = self.start_exposure(wafer_id)
            process_time = time.time() - start_time
            
            result = {
                "wafer_id": wafer_id,
                "success": success,
                "process_time": process_time,
                "timestamp": time.time()
            }
            
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append(result)
            
            # 每處理5個晶圓執行一次快速校準
            if i % 5 == 0 and i < len(wafer_list):
                print("🛠 執行快速校準...")
                self.light_source.calibrate()
        
        print(f"\n🎉 批量處理完成: {results['success']} 成功, {results['failed']} 失敗")
        return results
    
    def emergency_stop(self):
        """緊急停止"""
        print("🛑 執行緊急停止!")
        
        # 立即停止光源
        self.light_source.stop_emission()
        
        # 停止所有設備
        self.device_manager.broadcast_command("EMERGENCY_STOP", {})
        
        self.production_state = "EMERGENCY"
    
    def get_production_status(self) -> Dict:
        """獲取生產狀態"""
        light_source_status = self.light_source.get_status()
        device_status = self.device_manager.get_system_status()
        
        return {
            "production_state": self.production_state,
            "wafer_count": self.wafer_count,
            "current_recipe": self.current_recipe,
            "light_source": light_source_status,
            "devices": device_status,
            "system_uptime": time.time()  # 簡化示例
        }
    
    def _validate_recipe(self, recipe: Dict) -> bool:
        """驗證光刻配方"""
        required_fields = ["name", "exposure_time", "light_source"]
        for field in required_fields:
            if field not in recipe:
                print(f"❌ 配方缺少必要字段: {field}")
                return False
        
        light_params = recipe.get("light_source", {})
        if "power" not in light_params:
            print("❌ 配方缺少光源功率設置")
            return False
        
        return True
    
    def _configure_light_source(self, light_params: Dict):
        """配置光源參數"""
        # 這裡可以根據配方調整光源配置
        print(f"💡 配置光源參數: {light_params}")
    
    def _move_wafer_to_position(self, wafer_id: str):
        """移動晶圓到曝光位置"""
        print(f"📦 移動晶圓 {wafer_id} 到曝光位置")
        # 實際實現會控制工作台設備
        time.sleep(0.5)  # 模擬移動時間
    
    def _get_exposure_parameters(self) -> EmissionParameters:
        """獲取曝光參數"""
        recipe_light = self.current_recipe.get("light_source", {})
        
        return EmissionParameters(
            power=recipe_light.get("power", 3.0e-9),
            duration=self.current_recipe.get("exposure_time", 10.0),
            frequency=recipe_light.get("frequency", 1000),
            duty_cycle=recipe_light.get("duty_cycle", 0.5)
        )
    
    def _execute_exposure_sequence(self):
        """執行曝光序列"""
        exposure_time = self.current_recipe.get("exposure_time", 10.0)
        
        print(f"⏱ 開始曝光，時長: {exposure_time}秒")
        
        # 模擬曝光過程
        start_time = time.time()
        while time.time() - start_time < exposure_time:
            elapsed = time.time() - start_time
            progress = min(elapsed / exposure_time, 1.0)
            
            # 實時監控和調整
            self._monitor_exposure_progress(progress, elapsed)
            
            time.sleep(0.1)  # 控制循環頻率
    
    def _monitor_exposure_progress(self, progress: float, elapsed: float):
        """監控曝光進度"""
        if progress % 0.2 < 0.01:  # 每20%進度報告一次
            print(f"📊 曝光進度: {progress*100:.1f}% ({elapsed:.1f}s)")
            
            # 檢查光源穩定性
            status = self.light_source.get_status()
            stability = status['performance_metrics'].get('stability', 1.0)
            
            if stability < 0.99:
                print("⚠️  檢測到穩定性下降，進行微調...")
                # 這裡可以觸發實時優化
    
    def _move_wafer_to_unload(self):
        """移動晶圓到卸載位置"""
        print("📤 移動晶圓到卸載位置")
        time.sleep(0.3)  # 模擬移動時間
    
    def _on_light_source_state_change(self, data):
        """光源狀態變化回調"""
        print(f"💡 光源狀態變化: {data['old_state']} → {data['new_state']}")
    
    def _on_power_update(self, power):
        """功率更新回調"""
        print(f"⚡ 光源功率更新: {power:.3e}W")
    
    def _on_error(self, error_data):
        """錯誤處理回調"""
        print(f"🚨 系統錯誤: {error_data}")
        self.production_state = "ERROR"

# 使用示例
def demo_semiconductor_lithography():
    """演示半導體光刻應用"""
    print("=" * 60)
    print("🏭 半導體光刻系統演示")
    print("=" * 60)
    
    # 創建光刻系統
    litho_system = SemiconductorLithographySystem()
    
    # 初始化系統
    if not litho_system.initialize_system():
        print("❌ 系統初始化失敗，演示中止")
        return
    
    # 加載光刻配方
    advanced_recipe = {
        "name": "5nm EUV 工藝",
        "exposure_time": 8.0,
        "light_source": {
            "power": 3.5e-9,    # 3.5nW
            "frequency": 2000,  # 2kHz 脈衝
            "duty_cycle": 0.6   # 60% 佔空比
        }
    }
    
    if not litho_system.load_recipe(advanced_recipe):
        print("❌ 配方加載失敗")
        return
    
    # 創建測試晶圓列表
    test_wafers = [f"Wafer_{i:03d}" for i in range(1, 4)]
    
    # 執行批量處理
    results = litho_system.batch_process(test_wafers)
    
    # 顯示生產報告
    print("\n" + "=" * 60)
    print("📊 生產報告")
    print("=" * 60)
    print(f"總處理: {results['total']} 晶圓")
    print(f"成功: {results['success']}")
    print(f"失敗: {results['failed']}")
    
    # 顯示系統狀態
    status = litho_system.get_production_status()
    print(f"\n🔧 系統狀態: {status['production_state']}")
    print(f"📦 已處理晶圓: {status['wafer_count']}")
    
    # 安全關閉系統
    litho_system.light_source.power_off()
    print("\n✅ 演示完成")

if __name__ == "__main__":
    demo_semiconductor_lithography()
