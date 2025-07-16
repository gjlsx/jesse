import pytest
import jesse.math_utils as mu


@pytest.mark.math
@pytest.mark.unit
def test_igcdex_basic_cases():
    """测试 igcdx 函数的基本用例"""
    # 测试用例 1: gcd(2,3) = 1
    result = mu.igcdex(2, 3)
    expected = (-1, 1, 1)
    assert result == expected, f"igcdex(2, 3) = {result}, 期望 {expected}"
    
    # 验证数学公式: x*a + y*b = gcd(a,b)
    x, y, g = result
    assert x*2 + y*3 == g, f"验证失败: {x}*2 + {y}*3 ≠ {g}"


@pytest.mark.math  
@pytest.mark.unit
def test_igcdex_larger_numbers():
    """测试 igcdex 函数的较大数字用例"""
    # 测试用例 2: gcd(10,12) = 2
    result = mu.igcdex(10, 12)
    expected = (-1, 1, 2)
    assert result == expected, f"igcdex(10, 12) = {result}, 期望 {expected}"
    
    # 验证数学公式: x*a + y*b = gcd(a,b)
    x, y, g = result
    assert x*10 + y*12 == g, f"验证失败: {x}*10 + {y}*12 ≠ {g}"


@pytest.mark.math
@pytest.mark.unit  
def test_igcdex_edge_cases():
    """测试 igcdex 函数的边界情况"""
    # 可以添加更多测试用例，比如:
    # - 一个数为0的情况
    # - 负数的情况
    # - 较大数字的情况
    pass


if __name__ == "__main__":
    # 如果直接运行此文件，使用简单的测试输出
    print("=" * 50)
    print("Jesse Math Utils 测试 (简单模式)")
    print("=" * 50)
    
    print("🧮 测试 igcdex 基本用例...")
    test_igcdex_basic_cases()
    print("✅ 基本用例测试通过!")
    
    print("🧮 测试 igcdex 较大数字...")
    test_igcdex_larger_numbers()
    print("✅ 较大数字测试通过!")
    
    print("\n🎉 所有测试完成!")
