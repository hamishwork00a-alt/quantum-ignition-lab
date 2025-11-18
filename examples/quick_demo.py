"""
快速演示 - 直接運行測試
"""

from quantum_light_controller import QuantumLightSourceController, LightSourceConfig, EmissionParameters

def quick_start():
    """快速開始演示"""
    print("🚀 量子預火光源快速演示")
    print("-" * 40)
    
    # 創建控制器
    config = LightSourceConfig()
    light_source = QuantumLightSourceController(config)
    
    # 狀態回調
    def on_state_change(data):
        print(f"💡 狀態變化: {data['old_state']} → {data['new_state']}")
    
    def on_power_update(power):
        print(f"⚡ 功率: {power:.3e}W")
    
    light_source.register_callback('state_change', on_state_change)
    light_source.register_callback('power_update', on_power_update)
    
    # 1. 啟動
    print("1. 啟動光源...")
    if light_source.power_on():
        print("   ✅ 啟動成功")
    else:
        print("   ❌ 啟動失敗")
        return
    
    # 2. 校準
    print("2. 系統校準...")
    if light_source.calibrate():
        print("   ✅ 校準成功")
    else:
        print("   ❌ 校準失敗")
        return
    
    # 3. 發射測試
    print("3. 光發射測試...")
    params = EmissionParameters(
        power=2.5e-9,
        duration=3.0  # 3秒自動停止
    )
    
    if light_source.start_emission(params):
        print("   ✅ 發射開始")
        
        # 監控狀態
        import time
        for i in range(5):
            status = light_source.get_status()
            print(f"   狀態: {status['state']}, 功率: {status['current_power']:.3e}W")
            time.sleep(1)
            if status['state'] != 'emitting':
                break
    else:
        print("   ❌ 發射失敗")
    
    # 4. 關閉
    light_source.power_off()
    print("4. 系統關閉")
    print("\n🎉 演示完成!")

if __name__ == "__main__":
    quick_start()
