import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import os
from datetime import datetime

class PDEVisualizer:
    """
    A class to visualize PDE solutions with dynamic contour maps and animations.
    Suitable for DeepONet results and other spatial-temporal data.
    """
    
    def __init__(self, figsize=(12, 8), dpi=100):
        """
        Initialize the visualizer.
        
        Parameters:
        figsize (tuple): Figure size (width, height)
        dpi (int): Figure DPI for high quality output
        """
        self.figsize = figsize
        self.dpi = dpi
        self.setup_colormap()
        
    def setup_colormap(self):
        """Setup a beautiful colormap similar to coolwarm but more vibrant"""
        # Create custom colormap with more vibrant colors
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']  # Blue, Purple, Orange, Red
        n_bins = 256
        self.custom_cmap = LinearSegmentedColormap.from_list('custom_coolwarm', colors, N=n_bins)
        
    def generate_sample_data(self, nx=50, ny=50, nt=20):
        """
        Generate sample PDE solution data for demonstration.
        Replace this with your actual DeepONet results.
        
        Parameters:
        nx, ny (int): Spatial grid points
        nt (int): Number of time steps
        
        Returns:
        x, y (arrays): Spatial coordinates
        t (array): Time coordinates
        u (array): Solution field of shape (nt, ny, nx)
        """
        # Create spatial grid
        x = np.linspace(0, 2*np.pi, nx)
        y = np.linspace(0, 2*np.pi, ny)
        X, Y = np.meshgrid(x, y)
        
        # Create time array
        t = np.linspace(0, 2, nt)
        
        # Generate sample solution: evolving wave pattern
        u = np.zeros((nt, ny, nx))
        for i, time in enumerate(t):
            u[i] = np.sin(X + time) * np.cos(Y + 0.5*time) * np.exp(-0.1*time)
            # Add some complexity
            u[i] += 0.3 * np.sin(2*X - time) * np.sin(Y + time)
            
        return X, Y, t, u
    
    def create_static_contour(self, X, Y, u, time_idx=0, title="PDE Solution", 
                             save_path=None, levels=20):
        """
        Create a static contour plot for a specific time step.
        
        Parameters:
        X, Y (arrays): Meshgrid coordinates
        u (array): Solution field
        time_idx (int): Time step index to plot
        title (str): Plot title
        save_path (str): Path to save the figure
        levels (int): Number of contour levels
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Create contour plot
        contour_filled = ax.contourf(X, Y, u[time_idx], levels=levels, 
                                   cmap=self.custom_cmap, extend='both')
        contour_lines = ax.contour(X, Y, u[time_idx], levels=levels, 
                                 colors='white', alpha=0.3, linewidths=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(contour_filled, ax=ax, shrink=0.8, aspect=20)
        cbar.set_label('Solution Value', fontsize=12)
        
        # Styling
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_title(f'{title} (t = {time_idx})', fontsize=14)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Static plot saved to: {save_path}")
            
        return fig, ax
    
    def create_animated_contour(self, X, Y, t, u, title="Dynamic PDE Evolution", 
                               save_gif=True, gif_name="pde_evolution.gif", 
                               levels=20, interval=200):
        """
        Create an animated contour plot showing evolution over time.
        
        Parameters:
        X, Y (arrays): Meshgrid coordinates
        t (array): Time array
        u (array): Solution field of shape (nt, ny, nx)
        title (str): Animation title
        save_gif (bool): Whether to save as GIF
        gif_name (str): GIF filename
        levels (int): Number of contour levels
        interval (int): Animation interval in milliseconds
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Find global min/max for consistent color scale
        vmin, vmax = u.min(), u.max()
        
        # Create initial contour plot
        contour_filled = ax.contourf(X, Y, u[0], levels=levels, 
                                   cmap=self.custom_cmap, vmin=vmin, vmax=vmax)
        
        # Add colorbar
        cbar = plt.colorbar(contour_filled, ax=ax, shrink=0.8, aspect=20)
        cbar.set_label('Solution Value', fontsize=12)
        
        # Styling
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Title that will be updated
        title_text = ax.set_title(f'{title} (t = {t[0]:.3f})', fontsize=14)
        
        def animate(frame):
            """Animation function"""
            # Clear previous contours
            for collection in ax.collections:
                collection.remove()
            
            # Create new contour plot
            contour_filled = ax.contourf(X, Y, u[frame], levels=levels, 
                                       cmap=self.custom_cmap, vmin=vmin, vmax=vmax)
            contour_lines = ax.contour(X, Y, u[frame], levels=levels, 
                                     colors='white', alpha=0.3, linewidths=0.5)
            
            # Update title
            title_text.set_text(f'{title} (t = {t[frame]:.3f})')
            
            # Return all collections properly
            all_collections = []
            if hasattr(contour_filled, 'collections'):
                all_collections.extend(contour_filled.collections)
            if hasattr(contour_lines, 'collections'):
                all_collections.extend(contour_lines.collections)
            
            return all_collections
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(t), 
                                     interval=interval, blit=False, repeat=True)
        
        plt.tight_layout()
        
        if save_gif:
            # Save as GIF
            writer = animation.PillowWriter(fps=5, metadata=dict(artist='PDE Visualizer'))
            anim.save(gif_name, writer=writer, dpi=self.dpi)
            print(f"Animation saved as: {gif_name}")
            
        return fig, anim
    
    def create_multiple_snapshots(self, X, Y, t, u, snapshot_times=None, 
                                 save_dir="snapshots", levels=20):
        """
        Create multiple snapshot plots at different time steps.
        
        Parameters:
        X, Y (arrays): Meshgrid coordinates
        t (array): Time array
        u (array): Solution field
        snapshot_times (list): List of time indices to plot
        save_dir (str): Directory to save snapshots
        levels (int): Number of contour levels
        """
        if snapshot_times is None:
            # Default: 4 evenly spaced snapshots
            snapshot_times = [0, len(t)//3, 2*len(t)//3, len(t)-1]
        
        # Create output directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Create subplot figure
        n_plots = len(snapshot_times)
        cols = min(2, n_plots)
        rows = (n_plots + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(self.figsize[0]*cols//2, 
                                                     self.figsize[1]*rows//2), 
                               dpi=self.dpi)
        
        if n_plots == 1:
            axes = [axes]
        elif rows == 1 and cols > 1:
            axes = axes
        else:
            axes = axes.flatten()
        
        vmin, vmax = u.min(), u.max()
        
        for i, time_idx in enumerate(snapshot_times):
            ax = axes[i] if n_plots > 1 else axes[0]
            
            # Create contour plot
            contour_filled = ax.contourf(X, Y, u[time_idx], levels=levels, 
                                       cmap=self.custom_cmap, vmin=vmin, vmax=vmax)
            contour_lines = ax.contour(X, Y, u[time_idx], levels=levels, 
                                     colors='white', alpha=0.3, linewidths=0.5)
            
            # Styling
            ax.set_xlabel('X', fontsize=10)
            ax.set_ylabel('Y', fontsize=10)
            ax.set_title(f't = {t[time_idx]:.3f}', fontsize=12)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
        
        # Hide empty subplots
        for i in range(len(snapshot_times), len(axes)):
            axes[i].set_visible(False)
        
        # Add colorbar
        cbar = plt.colorbar(contour_filled, ax=axes[:len(snapshot_times)], 
                          shrink=0.8, aspect=20)
        cbar.set_label('Solution Value', fontsize=12)
        
        plt.suptitle('PDE Solution Snapshots', fontsize=16)
        plt.tight_layout()
        
        # Save combined plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(save_dir, f"snapshots_{timestamp}.png")
        plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
        print(f"Snapshots saved to: {save_path}")
        
        return fig, axes


def main():
    """
    Main function demonstrating the PDE visualization capabilities.
    Replace the sample data generation with your actual DeepONet results.
    """
    print("Starting PDE Visualization...")
    
    # Initialize visualizer
    visualizer = PDEVisualizer(figsize=(12, 8), dpi=100)
    
    # Generate or load your data
    # Replace this with your actual DeepONet results
    print("Generating sample data...")
    X, Y, t, u = visualizer.generate_sample_data(nx=60, ny=60, nt=25)
    
    # Create static contour plot
    print("Creating static contour plot...")
    fig_static, ax_static = visualizer.create_static_contour(
        X, Y, u, time_idx=10, 
        title="PDE Solution", 
        save_path="static_contour.png"
    )
    
    # Create animated contour plot
    print("Creating animated contour plot...")
    fig_anim, anim = visualizer.create_animated_contour(
        X, Y, t, u, 
        title="Dynamic PDE Evolution",
        save_gif=True,
        gif_name="pde_evolution.gif",
        levels=25,
        interval=150
    )
    
    # Create multiple snapshots
    print("Creating multiple snapshots...")
    fig_snaps, axes_snaps = visualizer.create_multiple_snapshots(
        X, Y, t, u,
        snapshot_times=[0, 8, 16, 24],
        save_dir="snapshots"
    )
    
    print("\nVisualization complete!")
    print("Generated files:")
    print("- static_contour.png: Static contour plot")
    print("- pde_evolution.gif: Animated evolution")
    print("- snapshots/: Directory with snapshot images")
    
    # Show plots (comment out if running headless)
    plt.show()


if __name__ == "__main__":
    main()


