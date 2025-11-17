"""
量子預火光源基礎演示 - 安全公開版本
"""

import numpy as np
import matplotlib.pyplot as plt
from src.core.shenqu_engine import ShenquOptimizer
from src.core.quantum_jet_sim import QuantumJetSimulator
from src.utils.visualization import ResultVisualizer

class QuantumIgnitionDemo:
    """量子預火光源技術演示器"""
    
    def __init__(self):
        self.shenqu_optimizer = ShenquOptimizer()
        self.visualizer = ResultVisualizer()
        
    def demonstrate_quantum_jet(self):
        """演示量子噴流技術"""
        print("🔬 演示量子噴流生成...")
        
        # 使用公開參數演示
        simulator = QuantumJetSimulator(
            flow_rate=5e-9,
            electric_field=1e6,
            frequency=28e9
        )
        
        # 生成量子膠囊
        capsules, metrics = simulator.generate_capsules()
        
        # 顯示結果
        print(f"✅ 生成 {len(capsules)} 個量子膠囊")
        print(f"📊 平均尺寸: {metrics['mean_diameter']:.2e} m")
        print(f"🎯 尺寸均勻性: {metrics['uniformity']:.3f}")
        
        return capsules, metrics
    
    def demonstrate_shenqu_optimization(self):
        """演示神曲優化算法"""
        print("\n🎯 演示神曲自適應優化...")
        
        # 定義優化目標函數（公開版本）
        def objective_function(params):
            # 簡化的目標函數，不包含敏感技術細節
            x, y = params['x'], params['y']
            return -((x-2)**2 + (y-3)**2) + np.random.normal(0, 0.1)
        
        # 運行神曲優化
        best_params, history = self.shenqu_optimizer.optimize(
            objective_function, 
            param_bounds={'x': (0, 5), 'y': (0, 5)},
            max_iterations=50
        )
        
        print(f"✅ 找到最優參數: {best_params}")
        print(f"📈 優化收斂歷程: {len(history)} 次迭代")
        
        return best_params, history
    
    def run_full_demonstration(self):
        """運行完整演示"""
        print("🚀 啟動量子預火光源完整技術演示")
        print("=" * 50)
        
        # 1. 量子噴流演示
        capsules, jet_metrics = self.demonstrate_quantum_jet()
        
        # 2. 神曲優化演示
        best_params, opt_history = self.demonstrate_shenqu_optimization()
        
        # 3. 結果可視化
        self.visualizer.plot_demonstration_results(
            capsules, jet_metrics, opt_history
        )
        
        print("\n🎉 演示完成！")
        print("💡 核心技術要點:")
        print("   • 量子噴流精確控制")
        print("   • 神曲自適應優化") 
        print("   • 多模塊協同工作")

if __name__ == "__main__":
    demo = QuantumIgnitionDemo()
    demo.run_full_demonstration()
