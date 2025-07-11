import json
import numpy as np
import argparse
from pathlib import Path
import os

def calculate_stats(data_dict):
    """
    计算数据字典中每个键对应值的统计信息
    
    Args:
        data_dict: 包含数据的字典，键为特征名称，值为对应的数据列表
        
    Returns:
        包含统计信息的字典
    """
    stats = {}
    
    for key, values in data_dict.items():
        values = np.array(values)
        if values.ndim == 1:
            stats[key] = {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "q01": float(np.percentile(values, 1)),
                "q99": float(np.percentile(values, 99))
            }
        else:
            stats[key] = {
                "mean": np.mean(values, axis=0).tolist(),
                "std": np.std(values, axis=0).tolist(),
                "min": np.min(values, axis=0).tolist(),
                "max": np.max(values, axis=0).tolist(),
                "q01": np.percentile(values, 1, axis=0).tolist(),
                "q99": np.percentile(values, 99, axis=0).tolist()
            }

    return stats


def extract_states_and_actions(jsonl_file):
    """
    从JSONL文件中提取observation.states和actions开头的数据
    
    Args:
        jsonl_file: JSONL文件路径
        
    Returns:
        包含提取数据的字典，用于计算全局统计信息
    """
    # 用于存储所有提取的数据
    all_data = {}
    
    # 读取JSONL文件
    with open(jsonl_file, 'r') as f:
        for line in f:
            episode_data = json.loads(line)
            stats_data = episode_data.get('stats', {})
            
            # 提取observation.states和actions开头的数据
            for key, value in stats_data.items():
                if key.startswith('observation.states') or key.startswith('actions'):
                    # 将数据添加到字典中
                    all_data[key] = value
                    
    return all_data


def process_jsonl_file(meta_path):
    """
    处理JSONL文件，提取observation.states和actions开头的数据，并计算全局统计信息
    
    Args:
        jsonl_path: JSONL文件路径
        output_path: 输出文件路径，如果为None则打印到控制台
    """
    # 提取数据
    episodes_stats_path = os.path.join(meta_path, "episodes_stats.jsonl")
    stats_path = os.path.join(meta_path, "stats.json")
    extracted_data = extract_states_and_actions(episodes_stats_path)
    
    # 输出提取的数据
    print("提取的observation.states和actions开头的数据:")
    print(json.dumps(extracted_data, indent=4))
    
    # 使用提供的calculate_stats函数计算全局统计信息
    # 准备用于计算统计信息的数据字典
    data_for_stats = {}
    
    # 从提取的数据中收集所有值
    for key, value in extracted_data.items():
        # 对于每个键，我们需要收集所有的值
        if key not in data_for_stats:
            data_for_stats[key] = []
        
        # 如果有mean字段，使用mean作为代表值
        if isinstance(value, dict) and 'mean' in value:
            data_for_stats[key].append(value['mean'])
    
    # 计算全局统计信息
    global_stats = calculate_stats(data_for_stats)
    
    # 输出全局统计信息
    print("\n全局统计信息:")
    print(json.dumps(global_stats, indent=4))
    
    with open(stats_path, 'w') as f:
        json.dump(global_stats, f, indent=4)

def save_stats_to_json(output_path, data_dict):
    stats = calculate_stats(data_dict)
    meta_dir = output_path / "meta"
    meta_dir.mkdir(exist_ok=True)
    stats_file = meta_dir / "stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=4)

process_jsonl_file('/Users/macbook/Workspace/project/pjlab/test/S2data/a2d/task_1/meta')