import pytest
import numpy as np
from src.core.shenqu_engine import ShenquOptimizer
from src.core.quantum_jet_sim import QuantumJetSimulator

class TestCoreModules:
    """核心模塊測試"""
    
    def test_shenqu_optimizer_initialization(self):
        """測試神曲優化器初始化"""
        optimizer = ShenquOptimizer()
        assert optimizer is not None
        assert hasattr(optimizer, 'optimize')
    
    def test_quantum_jet_basic_operation(self):
        """測試量子噴流基礎操作"""
        simulator = QuantumJetSimulator()
        capsules, metrics = simulator.generate_capsules()
        
        assert len(capsules) > 0
        assert 'mean_diameter' in metrics
        assert metrics['uniformity'] > 0
    
    def test_optimization_convergence(self):
        """測試優化收斂性"""
        def simple_objective(params):
            return -params['x']**2
        
        optimizer = ShenquOptimizer()
        best_params, history = optimizer.optimize(
            simple_objective, 
            {'x': (-5, 5)}, 
            max_iterations=20
        )
        
        assert abs(best_params['x']) < 1.0
        assert len(history) <= 20
