# DeepONet

# PDE Results Visualizer

A powerful Python tool for visualizing Partial Differential Equation (PDE) solutions with dynamic contour maps and animations. Perfect for DeepONet results and other spatial-temporal data.

## Features

- Beautiful visualizations with custom colormaps and vibrant colors
- Animated contours showing dynamic evolution over time with GIF export
- Multiple snapshots in grid layouts showing different time steps  
- Highly customizable with adjustable contour levels, colors, and animations
- High-quality output suitable for presentations and publications
- Easy integration with simple interface for your DeepONet results

## Installation

```bash
pip install numpy matplotlib pillow
```

## Quick Start

```python
from pde_visualizer import PDEVisualizer

# Initialize visualizer
visualizer = PDEVisualizer(figsize=(12, 8), dpi=100)

# Load your data (X, Y are 2D coordinates, t is 1D time, u is 3D solution)
X, Y, t, u = load_your_data()

# Create animated visualization
fig, anim = visualizer.create_animated_contour(
    X, Y, t, u, 
    title="PDE Evolution",
    save_gif=True,
    gif_name="results.gif"
)
```

## Usage with Your DeepONet Results

### Step 1: Replace Sample Data Function

```python
def load_your_data():
    """
    Load your DeepONet results
    
    Returns:
    --------
    X, Y : 2D arrays
        Spatial coordinate meshgrids
    t : 1D array  
        Time coordinates
    u : 3D array of shape (n_time, n_y, n_x)
        Solution field
    """
    X = your_x_coordinates
    Y = your_y_coordinates  
    t = your_time_array
    u = your_solution_field
    
    return X, Y, t, u
```

### Step 2: Update Main Function

```python
def main():
    visualizer = PDEVisualizer()
    
    # Replace sample data generation with your data
    X, Y, t, u = load_your_data()  # Change this line
    
    # Create visualizations
    visualizer.create_animated_contour(X, Y, t, u, save_gif=True)
```

### Step 3: Customize Parameters

```python
# Adjust visualization parameters
visualizer.create_animated_contour(
    X, Y, t, u,
    title="My PDE Solution",
    levels=25,           # Number of contour levels
    interval=150,        # Animation speed (ms)
    gif_name="my_pde.gif"
)
```

## Available Methods

| Method | Description | Output |
|--------|-------------|---------|
| `create_static_contour()` | Single time step visualization | PNG image |
| `create_animated_contour()` | Dynamic evolution animation | GIF/MP4 file |
| `create_multiple_snapshots()` | Grid of different time steps | PNG with subplots |

## Customization Options

### Colormap Customization

```python
def setup_custom_colormap(self):
    colors = ['#your_color1', '#your_color2', '#your_color3']
    self.custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
```

### Animation Settings

```python
visualizer.create_animated_contour(
    X, Y, t, u,
    levels=30,           # More contour lines
    interval=100,        # Faster animation
    figsize=(15, 10),    # Larger figure
    save_gif=True
)
```

### Output Quality

```python
visualizer = PDEVisualizer(
    figsize=(16, 12),    # High resolution
    dpi=150              # Print quality
)
```

## Output Files

Running the script generates:

```
your_project/
├── static_contour.png          # Static contour plot
├── pde_evolution.gif           # Animated evolution  
└── snapshots/                  # Directory with snapshots
    └── snapshots_YYYYMMDD_HHMMSS.png
```

## Advanced Usage

### Batch Processing Multiple Solutions

```python
solutions = ["solution1.npy", "solution2.npy", "solution3.npy"]

for i, sol_file in enumerate(solutions):
    X, Y, t, u = load_solution(sol_file)
    visualizer.create_animated_contour(
        X, Y, t, u,
        gif_name=f"animation_{i}.gif",
        title=f"Solution {i+1}"
    )
```

### Custom Snapshot Times

```python
# Create snapshots at specific times
snapshot_indices = [0, 10, 20, 30, -1]  # Including last frame
visualizer.create_multiple_snapshots(
    X, Y, t, u,
    snapshot_times=snapshot_indices
)
```

## Requirements

- Python 3.7+
- NumPy
- Matplotlib  
- Pillow (for GIF generation)
- Optional: FFmpeg (for MP4 fallback)

## Example Data Format

Your data should be structured as:

```python
# Spatial coordinates (2D meshgrids)
X.shape = (ny, nx)  # e.g., (50, 100)
Y.shape = (ny, nx)  # e.g., (50, 100)

# Time array  
t.shape = (nt,)     # e.g., (25,)

# Solution field
u.shape = (nt, ny, nx)  # e.g., (25, 50, 100)
```

## Performance Tips

- **Large datasets**: Reduce `levels` and `dpi` for faster processing
- **Memory optimization**: Use `cache_frame_data=False` for animations
- **File size**: Lower DPI for GIF files, higher for static plots
- **Speed**: Increase `interval` for smoother animations

## Troubleshooting

### Common Issues

**GIF not saving:**
```python
# The script automatically falls back to MP4
# Install pillow: pip install pillow
```

**Memory errors:**
```python
# Reduce resolution
visualizer = PDEVisualizer(dpi=75)
# Or reduce contour levels
levels=15
```

**Slow animations:**
```python
# Increase interval between frames
interval=300  # milliseconds
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for visualizing DeepONet and neural operator results
- Inspired by scientific visualization best practices
- Designed for researchers and practitioners in computational physics
