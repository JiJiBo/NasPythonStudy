from src.utils.ChatUtils import AIRequestHandlerWithHistory
from src.utils.KVUtils import KVUtils
from src.utils.LocalModelManager import LocalModelManager
from src.db.llm_config_db import LLMConfigDB

APP_NAME = 'Aithon'
kvUtils = KVUtils()
ai_handler = AIRequestHandlerWithHistory()
STUDY_DIR="assets/study"

# 全局实例
local_model_manager = LocalModelManager()
llm_config_db = LLMConfigDB()

def auto_load_local_model():
    """应用启动时自动加载本地模型"""
    try:
        print("🔍 检查是否需要自动加载本地模型...")
        
        # 检查是否已有模型加载
        if local_model_manager.is_model_loaded():
            loaded_model = local_model_manager.get_loaded_model_name()
            print(f"✅ 已有模型加载: {loaded_model}")
            return True
        
        # 获取当前配置
        current_config = llm_config_db.get_current_config()
        if not current_config:
            print("ℹ️ 没有找到当前配置，跳过自动加载")
            return False
            
        # 检查是否是本地模型配置
        if current_config.get('provider') not in ['local', '本地']:
            print(f"ℹ️ 当前配置不是本地模型: {current_config.get('provider')}")
            return False
            
        model_name = current_config.get('model')
        if not model_name:
            print("⚠️ 本地模型配置中没有指定模型名称")
            return False
            
        print(f"🎯 检测到本地模型配置: {model_name}")
        
        # 检查模型是否已安装
        if not local_model_manager.is_model_installed(model_name):
            print(f"⚠️ 模型 {model_name} 未安装，跳过自动加载")
            return False
            
        # 尝试加载模型
        print(f"🚀 开始自动加载模型: {model_name}")
        success = local_model_manager.load_model(model_name)
        
        if success:
            print(f"✅ 自动加载模型成功: {model_name}")
            return True
        else:
            print(f"❌ 自动加载模型失败: {model_name}")
            return False
            
    except Exception as e:
        print(f"❌ 自动加载本地模型时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False