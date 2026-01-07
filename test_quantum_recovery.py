#!/usr/bin/env python3
"""
Test script for quantum recovery simulation
"""
import sys
from quantum_recovery import simulate_recovery

def test_quantum_recovery():
    """Test the quantum recovery simulation"""
    print("="*60)
    print("  Testing Quantum Recovery Simulation")
    print("="*60)
    
    # Run the simulation
    attacked_val, recovered_val = simulate_recovery()
    
    print(f"\nResults:")
    print(f"  Correlation after Attack: {attacked_val:.1f}%")
    print(f"  Correlation after Recovery: {recovered_val:.1f}%")
    
    # Validate results
    success = True
    
    # Check that attack reduces correlation significantly
    if attacked_val > 10.0:
        print(f"\n❌ FAIL: Attack correlation ({attacked_val:.1f}%) should be close to 0%")
        success = False
    else:
        print(f"\n✅ PASS: Attack correlation is low ({attacked_val:.1f}%)")
    
    # Check that recovery restores correlation
    if recovered_val < 95.0:
        print(f"❌ FAIL: Recovery correlation ({recovered_val:.1f}%) should be close to 100%")
        success = False
    else:
        print(f"✅ PASS: Recovery correlation is high ({recovered_val:.1f}%)")
    
    # Check that recovery improves correlation
    improvement = recovered_val - attacked_val
    if improvement < 90.0:
        print(f"❌ FAIL: Recovery improvement ({improvement:.1f}%) is too low")
        success = False
    else:
        print(f"✅ PASS: Recovery shows significant improvement ({improvement:.1f}%)")
    
    print("\n" + "="*60)
    if success:
        print("  All Tests Passed! ✓")
        print("="*60)
        return 0
    else:
        print("  Some Tests Failed ✗")
        print("="*60)
        return 1

if __name__ == "__main__":
    exit_code = test_quantum_recovery()
    sys.exit(exit_code)
