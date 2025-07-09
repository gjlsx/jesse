#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis 基础操作测试脚本
"""

import redis
import time

def test_redis_basic_operations():
    """测试 Redis 基础操作"""
    print("=== Redis 基础操作测试 ===")
    
    try:
        # 连接到 Redis 服务器
        print("1. 连接到 Redis 服务器...")
        r = redis.Redis(host='localhost', port=6379, db=0, password='gj', decode_responses=True)
        
        # 测试连接
        print("2. 测试连接...")
        response = r.ping()
        print(f"   Ping 响应: {response}")
        
        # 基础字符串操作
        print("\n3. 测试字符串操作...")
        r.set('test_key', 'Hello Redis!')
        value = r.get('test_key')
        print(f"   设置键 'test_key': Hello Redis!")
        print(f"   获取键 'test_key': {value}")
        
        # 测试过期时间
        print("\n4. 测试过期时间...")
        r.setex('temp_key', 5, 'This will expire in 5 seconds')
        print(f"   设置临时键 'temp_key'，5秒后过期")
        print(f"   当前值: {r.get('temp_key')}")
        print(f"   剩余生存时间: {r.ttl('temp_key')} 秒")
        
        # 列表操作
        print("\n5. 测试列表操作...")
        r.lpush('test_list', 'item1', 'item2', 'item3')
        list_items = r.lrange('test_list', 0, -1)
        print(f"   创建列表 'test_list': {list_items}")
        
        # 哈希操作
        print("\n6. 测试哈希操作...")
        r.hset('test_hash', 'name', 'wind')
        r.hset('test_hash', 'age', '25')
        r.hset('test_hash', 'city', 'Beijing')
        hash_data = r.hgetall('test_hash')
        print(f"   创建哈希 'test_hash': {hash_data}")
        
        # 集合操作
        print("\n7. 测试集合操作...")
        r.sadd('test_set', 'apple', 'banana', 'orange')
        set_items = r.smembers('test_set')
        print(f"   创建集合 'test_set': {set_items}")
        
        # 有序集合操作
        print("\n8. 测试有序集合操作...")
        r.zadd('test_zset', {'player1': 100, 'player2': 200, 'player3': 150})
        zset_items = r.zrange('test_zset', 0, -1, withscores=True)
        print(f"   创建有序集合 'test_zset': {zset_items}")
        
        # 数据库操作
        print("\n9. 测试数据库操作...")
        keys = r.keys('test_*')
        print(f"   所有测试键: {keys}")
        
        # 清理测试数据
        print("\n10. 清理测试数据...")
        for key in keys:
            r.delete(key)
        print(f"   已删除 {len(keys)} 个测试键")
        
        print("\n=== 测试完成 ===")
        return True
        
    except redis.ConnectionError as e:
        print(f"连接错误: {e}")
        print("请确保 Redis 服务正在运行")
        return False
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        return False

def test_redis_with_auth(username, password):
    """测试带认证的 Redis 连接"""
    print(f"\n=== 测试 Redis 认证 (用户名: {username}) ===")
    
    try:
        # 注意：Redis 通常不使用用户名，只使用密码
        r = redis.Redis(host='localhost', port=6379, db=0, password=password, decode_responses=True)
        
        # 测试连接
        response = r.ping()
        print(f"认证连接成功: {response}")
        
        # 设置和获取数据
        r.set('auth_test', f'Hello {username}!')
        value = r.get('auth_test')
        print(f"认证测试数据: {value}")
        
        # 清理
        r.delete('auth_test')
        print("认证测试完成")
        return True
        
    except redis.AuthenticationError as e:
        print(f"认证失败: {e}")
        return False
    except Exception as e:
        print(f"认证测试错误: {e}")
        return False

if __name__ == "__main__":
    # 基础操作测试
    success = test_redis_basic_operations()
    
    if success:
        print("\n=== Redis 基础功能测试完成 ===")
        print("✓ 连接测试: 成功")
        print("✓ 字符串操作: 成功")
        print("✓ 过期时间: 成功")
        print("✓ 列表操作: 成功")
        print("✓ 哈希操作: 成功")
        print("✓ 集合操作: 成功")
        print("✓ 有序集合: 成功")
        print("✓ 数据库操作: 成功")
        print("✓ 数据清理: 成功")
        
        # 认证测试
        auth_success = test_redis_with_auth('wind', 'gj')
        if auth_success:
            print("✓ 认证测试: 成功")
        else:
            print("✗ 认证测试: 失败")
    
    print("\n按 Enter 键退出...")
    input() 