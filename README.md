# Asymmetric Radiation-Aware Navigation for Mobile Robots

This repository contains the core ROS 2 reference implementation for the paper on **Asymmetric Radiation-Aware Navigation**. It provides a reference implementation of the dynamic radiation field mapping, the non-linear cost transfer function, and the Nav2 Costmap2D integration.

## Repository Structure

- **`asymmetric_radiation_core`**: Python-based ROS 2 nodes for the radiation field server (`radiation_field_server`), virtual geiger counter simulation (`virtual_geiger`), map generators, and viewers.
- **`asymmetric_radiation_plugins`**: High-performance C++ implementations of the core components:
  - `AsymmetricRadiationLayer`: A custom `nav2_costmap_2d` plugin that dynamically integrates the non-linear transfer function outputs into the global costmap.
  - `radiation_mapper_node`: A C++ node for real-time radiation field mapping using Gaussian splatting and shared memory.
  - `virtual_geiger_node`: A C++ node simulating a geiger counter based on ground-truth maps and TF.
- **`asymmetric_radiation_nav`**: Baseline and customized Nav2 configurations (`nav2_params.yaml`) demonstrating how to integrate the custom `AsymmetricRadiationLayer` into the global costmap.
- **`logs`**: Experimental data, passport files, and ROS bag summaries from the test runs described in the paper.

## Architecture and Components

For the purpose of open-source reproducibility and peer review, the components here rely **only** on standard ROS 2 interfaces (parameters, TF2, standard messages) and represent components extracted from a broader robotics system.

- **Non-Linear Transform**: Note that the actual non-linear transfer function (converting physical radiation limits into Nav2 routing costs) is performed by the Python `radiation_field_server`. The C++ plugin (`AsymmetricRadiationLayer`) scales this pre-computed grid and merges it into the Costmap2D master grid.
- **Constants vs Parameters**: In this published reference implementation, the limits are hardcoded model constants rather than dynamic ROS parameters. The server uses `D_noise = 50.0`, `D_crit = 1000.0`, `K = 10.0`. The plugin scales the received 0-100 values to a maximum penalty of `220`. 
- **Mapping Implementations**: The repository provides both Python and C++ implementations of the radiation mapper. The **Python mapper** (`radiation_mapper.py`) was the one used in the mapping verification (which creates the CSV with measurement logs), and is the reference implementation for that experiment. The C++ version is provided for real-time online use.

## Experimental Data and Result Reproduction

The `logs` directory contains the raw data and summaries used for the paper:

| Paper Material | Source Location |
|---|---|
| Table 1, baseline | `logs/series_00/R*_baseline_*` |
| Table 1, proposed | `logs/series_01/R*_proposed_*` |
| Table 2 | `logs/Rad_test(A,B,C)_robot/` |
| Mapping Verification | `logs/radiation_mapping_run_01/ros_bag.zip` |

*Note: Old `proposed` runs in `series_00` and additional `A/B/C` simulations are historical checkpoints and are not included in the main tables of the current article.*

- Movement boundaries are determined by velocity thresholds: `|v| > 0.03` m/s or `|ω| > 0.03` rad/s.
- Internal stops are preserved in the total duration.
- Cumulative exposure in simulation is integrated using the trapezoidal rule over the initial ground-truth field.
- Results average three runs per mode.

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
**Note**: The system requires an active `/map` topic and a valid TF tree providing `map -> base_footprint`.

**1. Start the System using Launch:**
This is the recommended way to start all components together:
```bash
ros2 launch asymmetric_radiation_core radiation_bringup.launch.py \
  maps_dir:=/home/oleksandr/ros2_ws/src/Asymmetric-radiation/asymmetric_radiation_core/maps \
  map_path:=explored_map.npy \
  sensor_map_path:=radiation_map_complex.npy
```

*(Alternatively, you can run individual nodes with `ros2 run` using `maps_dir` and `map_path` parameters)*

**2. Control via Parameters:**

To enable the virtual geiger:
```bash
ros2 param set /virtual_geiger is_active True
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
