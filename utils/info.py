import json
import os
import sys

def modify_info_json(input_file, output_file=None):
    """
    修改info.json文件，将所有observation.images.开头的键中的：
    1. "names"中的"rgb"改为"channels"
    2. "video.codec"的值从"av1"改为"h264"
    
    Args:
        input_file: 输入的info.json文件路径
        output_file: 输出的info.json文件路径，如果为None则覆盖输入文件
    """
    # 如果output_file为None，则覆盖输入文件
    if output_file is None:
        output_file = input_file
    
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 遍历features中的所有键
    for key in data.get('features', {}):
        # 检查键是否以"observation.images."开头
        if key.startswith('observation.images.'):
            feature = data['features'][key]
            
            # 修改names中的"rgb"为"channels"
            if 'names' in feature and isinstance(feature['names'], list):
                names = feature['names']
                for i, name in enumerate(names):
                    if name == 'rgb':
                        names[i] = 'channels'
            
            # 修改video.codec从"av1"为"h264"
            if 'info' in feature and 'video.codec' in feature['info']:
                if feature['info']['video.codec'] == 'av1':
                    feature['info']['video.codec'] = 'h264'
    
    # 将修改后的数据写回文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    
    print(f"已成功修改 {input_file} 并保存到 {output_file}")

def main():
    # 默认的输入文件路径
    input_file = "/Users/macbook/Workspace/project/pjlab/test/S2data/a2d/task_1/meta/info.json"
    output_file = "/Users/macbook/Workspace/project/pjlab/test/S2data/a2d/task_1/meta/info_1.json"
    # # 如果命令行提供了参数，则使用命令行参数作为输入文件路径
    # if len(sys.argv) > 1:
    #     input_file = sys.argv[1]
    # else:
    #     input_file = default_input_file
    
    # # 如果命令行提供了第二个参数，则使用它作为输出文件路径
    # if len(sys.argv) > 2:
    #     output_file = sys.argv[2]
    # else:
    #     output_file = None
    
    # # 检查输入文件是否存在
    # if not os.path.isfile(input_file):
    #     print(f"错误：输入文件 {input_file} 不存在")
    #     sys.exit(1)
    
    # 修改info.json文件
    modify_info_json(input_file, output_file)

if __name__ == "__main__":
    main()