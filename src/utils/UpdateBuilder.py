"""
增量更新构建工具
用于生成 update.json 文件，支持文件分块、哈希计算、版本管理
"""

import os
import json
import hashlib
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class UpdateBuilder:
    """增量更新构建器"""
    
    def __init__(self, app_dir: str, output_dir: str = "updates"):
        self.app_dir = Path(app_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 大文件分块大小 (50MB)
        self.chunk_size = 50 * 1024 * 1024
        
        # 忽略的文件和目录
        self.ignore_patterns = {
            "__pycache__",
            "*.pyc",
            "*.pyo",
            ".git",
            ".gitignore",
            "*.log",
            "*.tmp",
            ".DS_Store",
            "Thumbs.db"
        }
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """计算文件MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"计算文件哈希失败 {file_path}: {e}")
            return ""
    
    def calculate_chunk_hashes(self, file_path: Path) -> List[str]:
        """计算大文件的分块哈希值"""
        chunk_hashes = []
        try:
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    chunk_hash = hashlib.md5(chunk).hexdigest()
                    chunk_hashes.append(chunk_hash)
            return chunk_hashes
        except Exception as e:
            print(f"计算分块哈希失败 {file_path}: {e}")
            return []
    
    def should_ignore_file(self, file_path: Path) -> bool:
        """检查文件是否应该被忽略"""
        file_name = file_path.name
        for pattern in self.ignore_patterns:
            if pattern.startswith("*"):
                if file_name.endswith(pattern[1:]):
                    return True
            elif pattern in str(file_path.parts):
                return True
        return False
    
    def scan_files(self) -> List[Dict]:
        """扫描应用目录，生成文件列表"""
        files_info = []
        
        if not self.app_dir.exists():
            print(f"应用目录不存在: {self.app_dir}")
            return files_info
        
        for root, dirs, files in os.walk(self.app_dir):
            # 过滤忽略的目录
            dirs[:] = [d for d in dirs if not self.should_ignore_file(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # 过滤忽略的文件
                if self.should_ignore_file(file_path):
                    continue
                
                try:
                    # 计算相对路径
                    rel_path = file_path.relative_to(self.app_dir)
                    rel_path_str = str(rel_path).replace("\\", "/")
                    
                    # 获取文件信息
                    file_size = file_path.stat().st_size
                    file_hash = self.calculate_file_hash(file_path)
                    
                    file_info = {
                        "path": rel_path_str,
                        "hash": file_hash,
                        "size": file_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    }
                    
                    # 如果是大文件，计算分块哈希
                    if file_size > self.chunk_size:
                        chunk_hashes = self.calculate_chunk_hashes(file_path)
                        if chunk_hashes:
                            file_info["chunks"] = chunk_hashes
                            file_info["chunk_size"] = self.chunk_size
                    
                    files_info.append(file_info)
                    
                except Exception as e:
                    print(f"处理文件失败 {file_path}: {e}")
        
        return files_info
    
    def generate_update_json(self, version: str, changelog: str = "", 
                           previous_version: Optional[str] = None) -> Dict:
        """生成更新信息JSON"""
        files_info = self.scan_files()
        
        update_info = {
            "version": version,
            "previous_version": previous_version,
            "build_time": datetime.now().isoformat(),
            "changelog": changelog,
            "total_files": len(files_info),
            "total_size": sum(f["size"] for f in files_info),
            "files": files_info
        }
        
        return update_info
    
    def save_update_json(self, update_info: Dict, filename: str = None) -> Path:
        """保存更新信息到JSON文件"""
        if filename is None:
            filename = f"update_{update_info['version']}.json"
        
        output_path = self.output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(update_info, f, indent=2, ensure_ascii=False)
        
        print(f"更新信息已保存到: {output_path}")
        return output_path
    
    def compare_with_previous(self, current_info: Dict, 
                            previous_info: Dict) -> Dict:
        """与之前版本比较，生成增量更新信息"""
        current_files = {f["path"]: f for f in current_info["files"]}
        previous_files = {f["path"]: f for f in previous_info["files"]}
        
        # 找出变化的文件
        changed_files = []
        new_files = []
        deleted_files = []
        
        for path, file_info in current_files.items():
            if path not in previous_files:
                new_files.append(file_info)
            elif file_info["hash"] != previous_files[path]["hash"]:
                changed_files.append(file_info)
        
        for path in previous_files:
            if path not in current_files:
                deleted_files.append({"path": path})
        
        incremental_info = {
            "version": current_info["version"],
            "previous_version": previous_info["version"],
            "build_time": current_info["build_time"],
            "changelog": current_info["changelog"],
            "update_type": "incremental",
            "changed_files": changed_files,
            "new_files": new_files,
            "deleted_files": deleted_files,
            "total_changes": len(changed_files) + len(new_files) + len(deleted_files),
            "total_size": sum(f["size"] for f in changed_files + new_files)
        }
        
        return incremental_info
    
    def create_update_package(self, version: str, changelog: str = "",
                            previous_version: Optional[str] = None,
                            create_incremental: bool = True) -> Tuple[Path, Path]:
        """创建完整的更新包"""
        print(f"开始构建版本 {version} 的更新包...")
        
        # 生成当前版本信息
        current_info = self.generate_update_json(version, changelog, previous_version)
        current_json_path = self.save_update_json(current_info)
        
        # 如果是增量更新，尝试与之前版本比较
        incremental_json_path = None
        if create_incremental and previous_version:
            previous_json_path = self.output_dir / f"update_{previous_version}.json"
            if previous_json_path.exists():
                try:
                    with open(previous_json_path, "r", encoding="utf-8") as f:
                        previous_info = json.load(f)
                    
                    incremental_info = self.compare_with_previous(current_info, previous_info)
                    incremental_json_path = self.save_update_json(
                        incremental_info, f"incremental_{version}.json"
                    )
                    print(f"增量更新信息已保存到: {incremental_json_path}")
                    
                except Exception as e:
                    print(f"生成增量更新信息失败: {e}")
        
        # 复制应用文件到输出目录
        app_output_dir = self.output_dir / f"app_{version}"
        if app_output_dir.exists():
            shutil.rmtree(app_output_dir)
        
        print(f"复制应用文件到: {app_output_dir}")
        shutil.copytree(self.app_dir, app_output_dir, 
                       ignore=shutil.ignore_patterns(*self.ignore_patterns))
        
        return current_json_path, incremental_json_path
    
    def generate_model_update_info(self, models_dir: str = "models") -> Dict:
        """生成模型更新信息"""
        models_path = Path(models_dir)
        if not models_path.exists():
            return {"models": []}
        
        models_info = []
        for model_file in models_path.glob("*.gguf"):
            try:
                file_size = model_file.stat().st_size
                file_hash = self.calculate_file_hash(model_file)
                
                model_info = {
                    "name": model_file.stem,
                    "filename": model_file.name,
                    "size": file_size,
                    "hash": file_hash,
                    "modified": datetime.fromtimestamp(model_file.stat().st_mtime).isoformat()
                }
                
                # 大模型文件分块
                if file_size > self.chunk_size:
                    chunk_hashes = self.calculate_chunk_hashes(model_file)
                    if chunk_hashes:
                        model_info["chunks"] = chunk_hashes
                        model_info["chunk_size"] = self.chunk_size
                
                models_info.append(model_info)
                
            except Exception as e:
                print(f"处理模型文件失败 {model_file}: {e}")
        
        return {
            "models": models_info,
            "total_models": len(models_info),
            "total_size": sum(m["size"] for m in models_info)
        }

def main():
    """命令行工具入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="增量更新构建工具")
    parser.add_argument("app_dir", help="应用目录路径")
    parser.add_argument("version", help="版本号")
    parser.add_argument("--changelog", default="", help="更新日志")
    parser.add_argument("--previous", help="之前版本号")
    parser.add_argument("--output", default="updates", help="输出目录")
    parser.add_argument("--no-incremental", action="store_true", help="不生成增量更新")
    
    args = parser.parse_args()
    
    # 创建构建器
    builder = UpdateBuilder(args.app_dir, args.output)
    
    # 构建更新包
    current_json, incremental_json = builder.create_update_package(
        version=args.version,
        changelog=args.changelog,
        previous_version=args.previous,
        create_incremental=not args.no_incremental
    )
    
    print(f"\n✅ 更新包构建完成!")
    print(f"完整更新信息: {current_json}")
    if incremental_json:
        print(f"增量更新信息: {incremental_json}")
    
    # 生成模型更新信息
    models_info = builder.generate_model_update_info()
    models_json_path = builder.output_dir / f"models_{args.version}.json"
    with open(models_json_path, "w", encoding="utf-8") as f:
        json.dump(models_info, f, indent=2, ensure_ascii=False)
    print(f"模型更新信息: {models_json_path}")

if __name__ == "__main__":
    main()
