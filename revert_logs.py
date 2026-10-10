import os

def revert_logs(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.json') or file.endswith('.jsonl') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                changed = False
                if 'asymmetric_radiation_plugins' in content:
                    content = content.replace('asymmetric_radiation_plugins', 'smart_plugins')
                    changed = True
                if 'asymmetric_radiation_core' in content:
                    content = content.replace('asymmetric_radiation_core', 'smart_radiation')
                    changed = True
                if 'asymmetric_radiation_nav' in content:
                    content = content.replace('asymmetric_radiation_nav', 'smart_nav')
                    changed = True
                if 'Asymmetric-radiation' in content:
                    content = content.replace('Asymmetric-radiation', 'smart_robotics')
                    changed = True
                    
                if changed:
                    with open(filepath, 'w') as f:
                        f.write(content)
                    print(f"Reverted {filepath}")

if __name__ == '__main__':
    revert_logs('/home/oleksandr/ros2_ws/src/Asymmetric-radiation/logs')
