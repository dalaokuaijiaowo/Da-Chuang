from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from detector import BatchAIDetector
from task_manager import task_manager
import os
import pandas as pd
import subprocess
import shutil
import threading

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化检测器 - 添加错误处理
try:
    # 使用绝对路径更安全
    model_path = os.path.join(os.path.dirname(__file__), "Chinese_v3")
    detector = BatchAIDetector(model_path)
    print("AI检测器初始化成功！")
except Exception as e:
    print(f"AI检测器初始化失败: {e}")
    detector = None

@app.route('/api/analyze', methods=['POST'])
def analyze_comments():
    """API接口：分析评论"""
    if detector is None:
        return jsonify({"error": "AI检测器未正确初始化"}), 500
    
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"error": "未上传文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        # 创建临时目录
        os.makedirs("./temp", exist_ok=True)
        detected_dir = os.path.join(os.path.dirname(__file__), '../detected')
        os.makedirs(detected_dir, exist_ok=True)
        
        # 保存临时文件
        temp_path = "./temp/uploaded_file.csv"
        file.save(temp_path)
        
        # 检测评论
        result_path = os.path.join(detected_dir, 'uploaded_result.csv')
        success = detector.detect_batch(temp_path, result_path)
        
        if not success:
            return jsonify({"error": "分析失败"}), 500
        
        # 读取结果，使用适当的编码处理
        df = pd.read_csv(result_path, encoding='utf-8-sig')
        
        # 只保留前端需要的字段
        df = df[["序号", "用户名", "评论内容", "ai_prob", "human_prob", "conclusion"]]
        results = df.to_dict('records')
        
        # 统计信息
        ai_count = len(df[df['conclusion'] == 'AI生成'])
        total_count = len(df)
        
        stats = {
            "total": total_count,
            "ai_count": ai_count,
            "human_count": total_count - ai_count,
            "ai_ratio": round(ai_count / total_count * 100, 2) if total_count > 0 else 0
        }
        
        return jsonify({
            "success": True,
            "results": results,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crawl/video', methods=['POST'])
def crawl_video_comments():
    """API接口：爬取B站视频评论"""
    try:
        data = request.get_json()
        bv = data.get('bv')
        is_second = data.get('is_second', False)
        
        if not bv:
            return jsonify({"error": "缺少bv参数"}), 400
        
        # 调用B站评论爬虫.py
        result = subprocess.run(
            ['python', '../B站/B站评论爬虫.py', bv, str(is_second)],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"爬取失败: {result.stderr}"}), 500
        
        return jsonify({
            "success": True,
            "message": "视频评论爬取完成",
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crawl/dynamic', methods=['POST'])
def crawl_dynamic_comments():
    """API接口：爬取B站动态评论"""
    try:
        data = request.get_json()
        opus = data.get('opus')
        is_second = data.get('is_second', False)
        
        if not opus:
            return jsonify({"error": "缺少opus参数"}), 400
        
        # 调用B站动态爬虫.py
        result = subprocess.run(
            ['python', '../B站/B站动态爬虫.py', opus, str(is_second)],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"爬取失败: {result.stderr}"}), 500
        
        return jsonify({
            "success": True,
            "message": "动态评论爬取完成",
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crawl/zhihu', methods=['POST'])
def crawl_zhihu_comments():
    """API接口：爬取知乎回答评论"""
    try:
        data = request.get_json()
        answer_id = data.get('answer_id')
        max_count = data.get('max_count', 500)
        
        if not answer_id:
            return jsonify({"error": "缺少answer_id参数"}), 400
        
        # 调用知乎评论爬虫.py
        result = subprocess.run(
            ['python', '../知乎/知乎评论爬虫.py', answer_id, str(max_count)],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"爬取失败: {result.stderr}"}), 500
        
        return jsonify({
            "success": True,
            "message": "知乎评论爬取完成",
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crawl/netease', methods=['POST'])
def crawl_netease_comments():
    """API接口：爬取网易云音乐评论"""
    try:
        data = request.get_json()
        song_id = data.get('song_id')
        
        if not song_id:
            return jsonify({"error": "缺少song_id参数"}), 400
        
        # 调用网易云音乐评论爬虫.py
        result = subprocess.run(
            ['python', '../网易云/网易云音乐评论爬虫.py', str(song_id)],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"爬取失败: {result.stderr}"}), 500
        
        return jsonify({
            "success": True,
            "message": "网易云音乐评论爬取完成",
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/crawl/douban', methods=['POST'])
def crawl_douban_books():
    """API接口：爬取豆瓣月度热书"""
    try:
        data = request.get_json()
        max_books = data.get('max_books')
        
        # 构建命令参数
        cmd = ['python', '../豆瓣/豆瓣月度热书爬虫.py']
        if max_books:
            cmd.append(str(max_books))
        
        # 调用豆瓣月度热书爬虫.py
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        if result.returncode != 0:
            return jsonify({"error": f"爬取失败: {result.stderr}"}), 500
        
        return jsonify({
            "success": True,
            "message": "豆瓣月度热书爬取完成",
            "output": result.stdout
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/files', methods=['GET'])
def get_files():
    """API接口：获取已爬取的文件列表"""
    try:
        data_dir = os.path.join(os.path.dirname(__file__), '../result')
        if not os.path.exists(data_dir):
            return jsonify({"files": []})
        
        files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        return jsonify({
            "files": files
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/files/content/<filename>', methods=['GET'])
def get_file_content(filename):
    """API接口：获取文件内容"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), '../result', filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 读取文件内容，使用适当的编码处理
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        # 确保文件格式与detector兼容，只保留需要的列
        # 支持多种评论内容和用户名的列名
        content_columns = ['评论内容', '内容', 'comment', 'text', 'content']
        username_columns = ['用户名', '用户', 'user', '评论用户', 'user_name', 'nickname']
        
        # 查找匹配的列名
        content_col = next((col for col in content_columns if col in df.columns), None)
        username_col = next((col for col in username_columns if col in df.columns), None)
        
        if content_col and username_col:
            # 重命名列以确保格式兼容
            if content_col != '评论内容':
                df = df.rename(columns={content_col: '评论内容'})
            if username_col != '用户名':
                df = df.rename(columns={username_col: '用户名'})
            
            # 添加序号列如果不存在
            if '序号' not in df.columns:
                df['序号'] = range(1, len(df) + 1)
            # 只返回需要的列（不包含序号，前端会自动生成）
            df = df[['用户名', '评论内容']]
            
            return jsonify({
                "success": True,
                "filename": filename,
                "data": df.to_dict('records')
            })
        else:
            return jsonify({"error": "文件格式不兼容"}), 400
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/files/download/<filename>', methods=['GET'])
def download_file(filename):
    """API接口：下载文件"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), '../result', filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 发送文件下载响应
        return send_from_directory(
            directory=os.path.join(os.path.dirname(__file__), '../result'),
            path=filename,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_detection_task(task_id, file_path, result_path):
    """在后台运行检测任务"""
    try:
        # 定义进度回调函数
        def progress_callback(current):
            task_manager.update_progress(task_id, current)
        
        # 检测评论
        success = detector.detect_batch(file_path, result_path, progress_callback)
        
        if not success:
            task_manager.fail_task(task_id, "分析失败")
            return
        
        # 读取结果，使用适当的编码处理
        df = pd.read_csv(result_path, encoding='utf-8-sig')
        
        # 只保留前端需要的字段
        df = df[["序号", "用户名", "评论内容", "ai_prob", "human_prob", "conclusion"]]
        results = df.to_dict('records')
        
        # 统计信息
        ai_count = len(df[df['conclusion'] == 'AI生成'])
        total_count = len(df)
        
        stats = {
            "total": total_count,
            "ai_count": ai_count,
            "human_count": total_count - ai_count,
            "ai_ratio": round(ai_count / total_count * 100, 2) if total_count > 0 else 0
        }
        
        # 完成任务
        task_manager.complete_task(task_id, {
            "success": True,
            "results": results,
            "stats": stats
        })
        
    except Exception as e:
        task_manager.fail_task(task_id, str(e))

@app.route('/api/analyze/file/<filename>', methods=['POST'])
def start_analyze_file(filename):
    """API接口：启动异步检测任务"""
    if detector is None:
        return jsonify({"error": "AI检测器未正确初始化"}), 500
    
    try:
        # 构建文件路径
        file_path = os.path.join(os.path.dirname(__file__), '../result', filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 读取文件获取总行数
        import pandas as pd
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        total = len(df)
        
        # 创建任务
        task_id = task_manager.create_task(filename, total)
        
        # 创建结果目录
        detected_dir = os.path.join(os.path.dirname(__file__), '../detected')
        os.makedirs(detected_dir, exist_ok=True)
        result_path = os.path.join(detected_dir, filename)
        
        # 在后台线程中运行检测任务
        thread = threading.Thread(
            target=run_detection_task,
            args=(task_id, file_path, result_path)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "success": True,
            "task_id": task_id,
            "message": "检测任务已启动"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """API接口：获取任务状态和进度"""
    task = task_manager.get_task(task_id)
    if task is None:
        return jsonify({"error": "任务不存在"}), 404
    
    return jsonify({
        "success": True,
        "task": task
    })

@app.route('/api/analyze/file/<filename>', methods=['GET'])
def analyze_file_by_name(filename):
    """API接口：根据文件名分析评论（同步版本，保留用于兼容）"""
    if detector is None:
        return jsonify({"error": "AI检测器未正确初始化"}), 500
    
    try:
        # 构建文件路径
        file_path = os.path.join(os.path.dirname(__file__), '../result', filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 创建结果目录
        detected_dir = os.path.join(os.path.dirname(__file__), '../detected')
        os.makedirs(detected_dir, exist_ok=True)
        
        # 检测评论
        result_path = os.path.join(detected_dir, filename)
        success = detector.detect_batch(file_path, result_path)
        
        if not success:
            return jsonify({"error": "分析失败"}), 500
        
        # 读取结果，使用适当的编码处理
        df = pd.read_csv(result_path, encoding='utf-8-sig')
        
        # 只保留前端需要的字段
        df = df[["序号", "用户名", "评论内容", "ai_prob", "human_prob", "conclusion"]]
        results = df.to_dict('records')
        
        # 统计信息
        ai_count = len(df[df['conclusion'] == 'AI生成'])
        total_count = len(df)
        
        stats = {
            "total": total_count,
            "ai_count": ai_count,
            "human_count": total_count - ai_count,
            "ai_ratio": round(ai_count / total_count * 100, 2) if total_count > 0 else 0
        }
        
        return jsonify({
            "success": True,
            "results": results,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    if detector is None:
        return jsonify({"status": "error", "message": "AI检测器未初始化"}), 500
    return jsonify({"status": "ok", "message": "服务正常运行"})

@app.route('/api/detected/files', methods=['GET'])
def get_detected_files():
    """API接口：获取已检测的文件列表"""
    try:
        detected_dir = os.path.join(os.path.dirname(__file__), '../detected')
        if not os.path.exists(detected_dir):
            return jsonify({"files": []})
        
        files = [f for f in os.listdir(detected_dir) if f.endswith('.csv')]
        return jsonify({
            "files": files
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detected/file/<filename>', methods=['GET'])
def get_detected_file_content(filename):
    """API接口：获取检测报告文件内容"""
    try:
        file_path = os.path.join(os.path.dirname(__file__), '../detected', filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 读取文件内容，使用适当的编码处理
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # 确保文件格式正确，只返回需要的列
        required_columns = ["序号", "用户名", "评论内容", "ai_prob", "human_prob", "conclusion"]
        
        # 检查所有必需列是否存在
        for col in required_columns:
            if col not in df.columns:
                return jsonify({"error": f"文件格式不兼容，缺少列: {col}"}), 400
        
        # 只返回需要的列
        df = df[required_columns]
        results = df.to_dict('records')
        
        # 统计信息
        ai_count = len(df[df['conclusion'] == 'AI生成'])
        total_count = len(df)
        
        stats = {
            "total": total_count,
            "ai_count": ai_count,
            "human_count": total_count - ai_count,
            "ai_ratio": round(ai_count / total_count * 100, 2) if total_count > 0 else 0
        }
        
        return jsonify({
            "success": True,
            "filename": filename,
            "results": results,
            "stats": stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 检查模型目录是否存在
    model_dir = os.path.join(os.path.dirname(__file__), "Chinese_v3")
    if not os.path.exists(model_dir):
        print(f"错误: 模型目录不存在: {model_dir}")
        print("请将 Chinese_v3 文件夹放在 backend 目录下")
    else:
        print(f"找到模型目录: {model_dir}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)