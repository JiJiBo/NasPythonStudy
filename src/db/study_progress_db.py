import sqlite3
import os
from datetime import datetime


class StudyProgressDB:
    def __init__(self, db_path="study_progress.db"):
        # self.db_path = os.path.join(get_app_path(), db_path)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # 学习进度表
        c.execute("""
            CREATE TABLE IF NOT EXISTS study_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter_name TEXT NOT NULL,
                section_name TEXT NOT NULL,
                study_status INTEGER DEFAULT 0,
                completed_timestamp DATETIME,
                UNIQUE(chapter_name, section_name)
            )
        """)

        conn.commit()
        conn.close()

    def is_section_completed(self, chapter_name, section_name):
        """
        判断一个小节有没有学习完成
        :param chapter_name: 章节名
        :param section_name: 小节名
        :return: True if completed, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT study_status FROM study_progress 
            WHERE chapter_name = ? AND section_name = ?
        """, (chapter_name, section_name))
        
        row = c.fetchone()
        conn.close()
        
        return row is not None and row[0] == 1

    def get_chapter_completed_count(self, chapter_name):
        """
        判断一个章节学习完的个数
        :param chapter_name: 章节名
        :return: 完成的小节数量
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT COUNT(*) FROM study_progress 
            WHERE chapter_name = ? AND study_status = 1
        """, (chapter_name,))
        
        count = c.fetchone()[0]
        conn.close()
        
        return count

    def set_section_status(self, chapter_name, section_name, is_completed=True):
        """
        存取一个小节的学习完成状态
        :param chapter_name: 章节名
        :param section_name: 小节名
        :param is_completed: 是否完成
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        if is_completed:
            # 设置为完成状态，记录完成时间
            c.execute("""
                INSERT OR REPLACE INTO study_progress 
                (chapter_name, section_name, study_status, completed_timestamp) 
                VALUES (?, ?, 1, ?)
            """, (chapter_name, section_name, datetime.now()))
        else:
            # 设置为未完成状态，清除完成时间
            c.execute("""
                INSERT OR REPLACE INTO study_progress 
                (chapter_name, section_name, study_status, completed_timestamp) 
                VALUES (?, ?, 0, NULL)
            """, (chapter_name, section_name))
        
        conn.commit()
        conn.close()

    def get_section_status(self, chapter_name, section_name):
        """
        获取小节的学习状态
        :param chapter_name: 章节名
        :param section_name: 小节名
        :return: dict with status and timestamp
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT study_status, completed_timestamp FROM study_progress 
            WHERE chapter_name = ? AND section_name = ?
        """, (chapter_name, section_name))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                "status": row[0],
                "completed_timestamp": row[1],
                "is_completed": row[0] == 1
            }
        return {
            "status": 0,
            "completed_timestamp": None,
            "is_completed": False
        }

    def get_all_progress(self):
        """
        获取所有学习进度
        :return: list of progress records
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT id, chapter_name, section_name, study_status, completed_timestamp 
            FROM study_progress 
            ORDER BY chapter_name, section_name
        """)
        
        rows = c.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "chapter_name": row[1],
                "section_name": row[2],
                "study_status": row[3],
                "completed_timestamp": row[4],
                "is_completed": row[3] == 1
            }
            for row in rows
        ]

    def get_chapter_progress(self, chapter_name):
        """
        获取指定章节的所有小节进度
        :param chapter_name: 章节名
        :return: list of section progress
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            SELECT id, section_name, study_status, completed_timestamp 
            FROM study_progress 
            WHERE chapter_name = ? 
            ORDER BY section_name
        """, (chapter_name,))
        
        rows = c.fetchall()
        conn.close()
        
        return [
            {
                "id": row[0],
                "section_name": row[1],
                "study_status": row[2],
                "completed_timestamp": row[3],
                "is_completed": row[2] == 1
            }
            for row in rows
        ]

    def delete_section_progress(self, chapter_name, section_name):
        """
        删除小节的学习进度记录
        :param chapter_name: 章节名
        :param section_name: 小节名
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            DELETE FROM study_progress 
            WHERE chapter_name = ? AND section_name = ?
        """, (chapter_name, section_name))
        
        conn.commit()
        conn.close()

    def reset_chapter_progress(self, chapter_name):
        """
        重置指定章节的所有进度
        :param chapter_name: 章节名
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""
            UPDATE study_progress 
            SET study_status = 0, completed_timestamp = NULL 
            WHERE chapter_name = ?
        """, (chapter_name,))
        
        conn.commit()
        conn.close()

    def get_total_statistics(self):
        """
        获取总体学习统计
        :return: dict with statistics
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 总小节数
        c.execute("SELECT COUNT(*) FROM study_progress")
        total_sections = c.fetchone()[0]
        
        # 已完成小节数
        c.execute("SELECT COUNT(*) FROM study_progress WHERE study_status = 1")
        completed_sections = c.fetchone()[0]
        
        # 总章节数
        c.execute("SELECT COUNT(DISTINCT chapter_name) FROM study_progress")
        total_chapters = c.fetchone()[0]
        
        # 已完成章节数（所有小节都完成的章节）
        c.execute("""
            SELECT COUNT(*) FROM (
                SELECT chapter_name 
                FROM study_progress 
                GROUP BY chapter_name 
                HAVING COUNT(*) = SUM(study_status)
            )
        """)
        completed_chapters = c.fetchone()[0]
        
        conn.close()
        
        return {
            "total_sections": total_sections,
            "completed_sections": completed_sections,
            "total_chapters": total_chapters,
            "completed_chapters": completed_chapters,
            "completion_rate": (completed_sections / total_sections * 100) if total_sections > 0 else 0
        }
