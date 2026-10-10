import os

def replace_in_file(filepath, old_str, new_str):
    with open(filepath, 'r') as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Replaced in {filepath}")

def process_dir(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.cpp', '.hpp', '.xml', '.yaml', '.txt', '.launch', '.cfg')):
                filepath = os.path.join(root, file)
                
                # Replace package names
                replace_in_file(filepath, 'asymmetric_radiation_core', 'asymmetric_radiation_core')
                replace_in_file(filepath, 'asymmetric_radiation_nav', 'asymmetric_radiation_nav')
                replace_in_file(filepath, 'asymmetric_radiation_plugins', 'asymmetric_radiation_plugins')
                
                # Replace hardcoded paths
                replace_in_file(filepath, 'Asymmetric-radiation/asymmetric_radiation_core', 'Asymmetric-radiation/asymmetric_radiation_core')
                replace_in_file(filepath, '/home/oleksandr/ros2_ws/src/Asymmetric-radiation/asymmetric_radiation_core', "os.path.join(os.path.expanduser('~'), 'ros2_ws', 'src', 'Asymmetric-radiation', 'asymmetric_radiation_core')")
                # Fix any broken replacements
                replace_in_file(filepath, 'install/asymmetric_radiation_core/share/asymmetric_radiation_core', 'install/asymmetric_radiation_core/share/asymmetric_radiation_core')

if __name__ == '__main__':
    process_dir('/home/oleksandr/ros2_ws/src/Asymmetric-radiation')
