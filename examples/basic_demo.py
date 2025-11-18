"""
基礎演示 - 快速展示光源控制功能
"""

from src.core.light_source_controller import (
    QuantumLightSourceController,
    LightSourceConfig, 
    EmissionParameters
)

def quick_demo():
    """快速演示"""
    print("🚀 量子預火光源快速演示")
    print("-" * 40)
    
    # 創建光源控制器
    config = LightSourceConfig(
        wavelength=5.8e-9,
        max_power=5.0e-9
    )
    
    light_source = QuantumLightSourceController(config)
    
    # 啟動光源
    print("1. 啟動光源...")
    if light_source.power_on():
        print("   ✅ 光源啟動成功")
    else:
        print("   ❌ 光源啟動失敗")
        return
    
    # 校準系統
    print("2. 執行系統校準...")
    if light_source.calibrate():
        print("   ✅ 校準完成")
    else:
        print("   ❌ 校準失敗")
        return
    
    # 開始發射
    print("3. 開始光發射...")
    emission_params = EmissionParameters(
        power=2.5e-9,    # 2.5nW
        duration=5.0     # 5秒
    )
    
    if light_source.start_emission(emission_params):
        print("   ✅ 光發射開始")
        
        # 顯示實時狀態
        import time
        for i in range(3):
            status = light_source.get_status()
            print(f"   狀態: {status['state']}, 功率: {status['current_power']:.3e}W")
            time.sleep(1)
        
        # 停止發射
        light_source.stop_emission()
        print("   ✅ 光發射停止")
    
    # 關閉系統
    light_source.power_off()
    print("4. 系統已安全關閉")
    print("\n🎉 演示完成!")

if __name__ == "__main__":
    quick_demo()
