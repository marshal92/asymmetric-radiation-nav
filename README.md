# Asymmetric Radiation-Aware Navigation for Mobile Robots

This repository contains the core ROS 2 reference implementation for the paper on **Asymmetric Radiation-Aware Navigation**. It provides a fully decoupled, standalone implementation of the dynamic radiation field mapping, the non-linear cost transfer function, and the Nav2 Costmap2D integration.

## Repository Structure

- **`asymmetric_radiation_core`**: Python-based ROS 2 nodes for the radiation field server (`radiation_field_server`), virtual geiger counter simulation (`virtual_geiger`), map generators, and viewers.
- **`asymmetric_radiation_plugins`**: High-performance C++ implementations of the core components:
  - `AsymmetricRadiationLayer`: A custom `nav2_costmap_2d` plugin that dynamically applies the non-linear transfer function (converting physical radiation limits into Nav2 routing costs).
  - `radiation_mapper_node`: A C++ node for real-time radiation field mapping using Gaussian splatting and shared memory.
  - `virtual_geiger_node`: A C++ node simulating a geiger counter based on ground-truth maps and TF.
- **`asymmetric_radiation_nav`**: Baseline and customized Nav2 configurations (`nav2_params.yaml`) demonstrating how to integrate the custom `AsymmetricRadiationLayer` into the global costmap.
- **`logs`**: Experimental data, passport files, and ROS bag summaries from the test runs described in the paper.

## Decoupled Architecture

For the purpose of open-source reproducibility and peer review, this repository has been explicitly decoupled from our proprietary robot control systems (lifelong mission managers, telemetry multiplexers, etc.). The components here rely **only** on standard ROS 2 interfaces (parameters, TF2, standard messages).

## How to Build

1. Clone this repository into the `src` folder of a ROS 2 workspace.
2. Install dependencies:
   ```bash
   rosdep install --from-paths src --ignore-src -r -y
   ```
3. Build the workspace:
   ```bash
   colcon build --packages-select asymmetric_radiation_core asymmetric_radiation_plugins asymmetric_radiation_nav
   ```

## How to Run (Minimal Working Example)

You can run the core components using standard ROS 2 CLI tools.

**1. Start the Radiation Field Server:**
```bash
ros2 run asymmetric_radiation_core radiation_field_server
```

**2. Start the C++ Mapper:**
```bash
ros2 run asymmetric_radiation_plugins radiation_mapper_node
```

**3. Trigger Mapping or Load a Map:**
Since the components are decoupled from our custom mission manager, you can control them using standard ROS 2 parameters:

To load a pre-existing map:
```bash
ros2 param set /radiation_mapper map_path "radiation_map_complex.npy"
```

To start online mapping (recording):
```bash
ros2 param set /radiation_mapper is_recording True
```

To enable the field server to publish the Nav2 cost field:
```bash
ros2 param set /radiation_field_server is_active True
```

## Citation
If you use this code in your research, please cite our paper (citation details to be updated upon publication).
