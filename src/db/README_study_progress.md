# 学习进度数据库使用说明

## 概述

`StudyProgressDB` 类用于管理Python学习课程中每个小节的学习进度。数据库存储每个小节的学习状态和完成时间。

## 数据库结构

### 表结构：study_progress

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键，自增 |
| chapter_name | TEXT | 章节名 |
| section_name | TEXT | 小节名 |
| study_status | INTEGER | 学习状态（0=未完成，1=已完成） |
| completed_timestamp | DATETIME | 学习完成时间戳 |

## 主要功能

### 1. 判断小节是否完成
```python
from src.db.study_progress_db import StudyProgressDB

db = StudyProgressDB()
is_completed = db.is_section_completed("第001章-开始", "第001节-写在前面")
print(f"是否完成: {is_completed}")  # True/False
```

### 2. 获取章节完成数量
```python
count = db.get_chapter_completed_count("第001章-开始")
print(f"已完成小节数: {count}")
```

### 3. 设置小节学习状态
```python
# 标记为已完成
db.set_section_status("第001章-开始", "第001节-写在前面", True)

# 标记为未完成
db.set_section_status("第001章-开始", "第001节-写在前面", False)
```

### 4. 获取小节详细状态
```python
status = db.get_section_status("第001章-开始", "第001节-写在前面")
print(status)
# 输出: {'status': 1, 'completed_timestamp': '2025-09-04 13:27:42.956686', 'is_completed': True}
```

### 5. 获取章节所有小节进度
```python
progress = db.get_chapter_progress("第001章-开始")
for section in progress:
    print(f"{section['section_name']}: {'已完成' if section['is_completed'] else '未完成'}")
```

### 6. 获取总体统计
```python
stats = db.get_total_statistics()
print(f"总小节数: {stats['total_sections']}")
print(f"已完成小节数: {stats['completed_sections']}")
print(f"完成率: {stats['completion_rate']:.1f}%")
```

### 7. 获取所有进度
```python
all_progress = db.get_all_progress()
for record in all_progress:
    print(f"{record['chapter_name']}/{record['section_name']}: {'已完成' if record['is_completed'] else '未完成'}")
```

### 8. 重置章节进度
```python
db.reset_chapter_progress("第001章-开始")  # 将该章节所有小节标记为未完成
```

### 9. 删除小节进度
```python
db.delete_section_progress("第001章-开始", "第001节-写在前面")  # 删除该小节的进度记录
```

## 使用示例

```python
from src.db.study_progress_db import StudyProgressDB

# 初始化数据库
db = StudyProgressDB("study_progress.db")

# 标记学习完成
db.set_section_status("第001章-开始", "第001节-写在前面", True)

# 检查是否完成
if db.is_section_completed("第001章-开始", "第001节-写在前面"):
    print("该小节已完成学习")

# 获取章节完成情况
completed_count = db.get_chapter_completed_count("第001章-开始")
print(f"第001章已完成 {completed_count} 个小节")

# 获取学习统计
stats = db.get_total_statistics()
print(f"总体完成率: {stats['completion_rate']:.1f}%")
```

## 注意事项

1. 数据库文件默认保存在当前目录，可以通过参数指定路径
2. 章节名和小节名的组合是唯一的，重复设置会更新现有记录
3. 完成时间戳在标记为完成时自动记录
4. 重置章节进度会将所有小节标记为未完成，但保留记录
5. 删除小节进度会完全移除该记录
