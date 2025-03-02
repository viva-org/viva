import sys
import os
from pathlib import Path

# 获取项目根目录
current_dir = Path(__file__).resolve().parent
project_root = str(current_dir.parent.parent)

# 将项目根目录添加到 Python 路径
sys.path.insert(0, project_root)

from infrastructure.repositories.user_repository import UserRepository

def test_user_repository():
    # 初始化 repository
    repo = UserRepository()
    
    # 测试创建用户
    test_user = repo.create_user(
        google_id="test123",
        email="test@example.com",
        username="testuser",
        profile_picture="http://example.com/pic.jpg"
    )
    print("Created user:", test_user)
    
    # 测试查询用户
    found_user = repo.get_user_by_google_id("test123")
    print("Found user by google_id:", found_user)
    
    # 测试更新用户
    updated_user = repo.update_user(
        google_id="test123",
        username="updated_username"
    )
    print("Updated user:", updated_user)
    
    # 测试搜索用户
    search_results = repo.search_users("updated")
    print("Search results:", search_results)
    
    # 测试删除用户
    delete_result = repo.delete_user("test123")
    print("Delete result:", delete_result)
    
    # 验证用户已被删除
    deleted_user = repo.get_user_by_google_id("test123")
    print("Deleted user check (should be None):", deleted_user)

if __name__ == "__main__":
    try:
        test_user_repository()
        print("All tests completed successfully!")
    except Exception as e:
        print(f"Test failed with error: {str(e)}") 