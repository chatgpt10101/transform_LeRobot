#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import argparse
import sys
from pathlib import Path


def transform_features(features):
    """
    转换 features 部分为新的格式
    
    Args:
        features: 原始 features 字典
    
    Returns:
        转换后的新格式字典
    """
    result = {
        "action": {},
        "state": {},
        "video": {}
    }
    
    # 处理所有键
    for key, value in features.items():
        # 处理 observation.images 开头的键 -> video
        if key.startswith("observation.images."):
            # 提取子键名称 (例如: observation.images.head -> head)
            sub_key = key.replace("observation.images.", "")
            result["video"][sub_key] = {
                "original_key": key
            }
        
        # 处理 observation.states 开头的键 -> state
        elif key.startswith("observation.states."):
            # 提取子键名称 (例如: observation.states.effector.position -> effector.position)
            sub_key = key.replace("observation.states.", "")
            
            # 从 shape 获取维度信息
            if "shape" in value and isinstance(value["shape"], list):
                shape_len = value["shape"][0] if value["shape"] else 0
                result["state"][sub_key] = {
                    "start": 0,
                    "end": shape_len,
                    "original_key": key
                }
        
        # 处理 actions 开头的键 -> action
        elif key.startswith("actions."):
            # 提取子键名称 (例如: actions.effector.position -> effector.position)
            sub_key = key.replace("actions.", "")
            
            # 从 shape 获取维度信息
            if "shape" in value and isinstance(value["shape"], list):
                shape_len = value["shape"][0] if value["shape"] else 0
                result["action"][sub_key] = {
                    "start": 0,
                    "end": shape_len,
                    "original_key": key
                }
    
    # 移除空的顶级键
    for key in list(result.keys()):
        if not result[key]:
            del result[key]
    
    return result


def process_info_json(input_path):
    """
    处理指定路径下的 info.json 文件
    
    Args:
        input_path: 输入路径
    """
    # 确保路径是 Path 对象
    path = Path(input_path)
    
    # 构建 info.json 的完整路径
    info_json_path = path / "info.json"
    
    # 检查文件是否存在
    if not info_json_path.exists():
        print(f"错误: 在 {path} 中未找到 info.json 文件")
        return
    
    try:
        # 读取 info.json 文件
        with open(info_json_path, 'r', encoding='utf-8') as f:
            info_data = json.load(f)
        
        # 检查是否包含 features 部分
        if "features" not in info_data:
            print(f"错误: info.json 中未找到 features 部分")
            return
        
        # 转换 features 部分
        transformed_features = transform_features(info_data["features"])
        
        # 创建输出文件路径
        output_path = path / "modify.json"
        
        # 写入转换后的结果
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transformed_features, f, indent=4, ensure_ascii=False)
        
        print(f"转换完成! 结果已保存到: {output_path}")
        
    except json.JSONDecodeError:
        print(f"错误: info.json 不是有效的 JSON 文件")
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='转换 info.json 中的 features 部分为新格式')
    parser.add_argument('path', type=str, help='包含 info.json 的目录路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 处理 info.json 文件
    process_info_json(args.path)


if __name__ == "__main__":
    main()