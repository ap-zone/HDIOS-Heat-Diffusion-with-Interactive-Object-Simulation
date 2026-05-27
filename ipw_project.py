import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

grid_size = 60       
time_steps = 1000
alpha = 0.24         
env_temp = 20.0      

T_grids = [np.ones((grid_size, grid_size)) * env_temp for _ in range(4)]
for T in T_grids:
    T[:, 0] = 100.0  

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 11))
axes = [ax1, ax2, ax3, ax4]
ims = []

configs = []
print("=" * 50)
print("     HDIOS: INTERACTIVE CONFIGURATION PANEL     ")
print("=" * 50)
print("Configure the 4 subplots below.")
print("Options: Shapes: square, circle, triangle")
print("         Placements: center, up, down, left, right\n")

for i in range(1, 5):
    print(f"--- Configuration for Graph {i} ---")
    
    try:
        num_holes = int(input("Enter number of holes (0, 1, or 2): ").strip())
        if num_holes not in [0, 1, 2]:
            print("Invalid number! Defaulting to 1 hole.")
            num_holes = 1
    except ValueError:
        print("Not a number! Defaulting to 0 holes.")
        num_holes = 0

    hole_list = []
    for h in range(num_holes):
        suffix = f" for hole {h+1}" if num_holes > 1 else ""
        
        shape = input(f"Enter shape{suffix} (square/circle/triangle): ").strip().lower()
        if shape not in ['square', 'circle', 'triangle']:
            shape = 'circle'
            
        placement = input(f"Enter placement{suffix} (center/up/down/left/right): ").strip().lower()
        if placement not in ['center', 'up', 'down', 'left', 'right']:
            placement = 'center'
            
        hole_list.append({'shape': shape, 'placement': placement})
        
    configs.append(hole_list)
    print("-" * 30)

print("\nStarting simulation... Loading window...")

def get_coordinates(placement):
    if placement == 'up':
        return 30, 45
    elif placement == 'down':
        return 30, 15
    elif placement == 'left':
        return 18, 30
    elif placement == 'right':
        return 42, 30
    else:  
        return 30, 30

for i, (ax, hole_config) in enumerate(zip(axes, configs)):
    ims.append(ax.imshow(T_grids[i], cmap='jet', vmin=15, vmax=105, origin='lower'))
    title_str = f"Graph {i+1}: "
    
    if len(hole_config) == 0:
        title_str += "Perfect Insulation (No Holes)"
    else:
        title_str += ", ".join([f"{h['placement']} {h['shape']}" for h in hole_config])
    ax.set_title(title_str, fontsize=10, fontweight='bold')
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    for h in hole_config:
        cx, cy = get_coordinates(h['placement'])
        if h['shape'] == 'circle':
            ax.add_patch(plt.Circle((cx, cy), 5, linewidth=1.5, edgecolor='white', linestyle='--', facecolor='none'))
        elif h['shape'] == 'square':
            ax.add_patch(plt.Rectangle((cx-5, cy-5), 10, 10, linewidth=1.5, edgecolor='white', linestyle='--', facecolor='none'))
        elif h['shape'] == 'triangle':
            pts = np.array([[cx-6, cy-4], [cx+6, cy-4], [cx, cy+6]])
            ax.add_patch(plt.Polygon(pts, linewidth=1.5, edgecolor='white', linestyle='--', facecolor='none'))

fig.colorbar(ims[3], ax=axes, label='Temperature (°C)', shrink=0.75, pad=0.05)

def update(frame):
    global T_grids
    
    def diffuse(T_matrix):
        T_new = T_matrix.copy()
        T_new[1:-1, 1:-1] = T_matrix[1:-1, 1:-1] + alpha * (
            T_matrix[2:, 1:-1] + T_matrix[:-2, 1:-1] +   
            T_matrix[1:-1, 2:] + T_matrix[1:-1, :-2] -   
            4 * T_matrix[1:-1, 1:-1]
        )
        T_new[:, 0] = 100.0
        T_new[:, -1] = 20.0
        T_new[0, :] = T_new[1, :]
        T_new[-1, :] = T_new[-2, :]
        return T_new

    for _ in range(3):
        for i in range(4):
            T_grids[i] = diffuse(T_grids[i])
            
            for h in configs[i]:
                cx, cy = get_coordinates(h['placement'])
                
                if h['shape'] == 'square':
                    T_grids[i][cy-5:cy+5, cx-5:cx+5] = env_temp
                    
                elif h['shape'] == 'circle':
                    y_indices, x_indices = np.ogrid[:grid_size, :grid_size]
                    dist_from_center = (x_indices - cx)**2 + (y_indices - cy)**2
                    T_grids[i][dist_from_center <= 5**2] = env_temp
                    
                elif h['shape'] == 'triangle':
                    for x in range(cx-6, cx+7):
                        for y in range(cy-4, cy+7):
                            if (0 <= x < grid_size) and (0 <= y < grid_size):
                                if (y - (cy-4)) <= (x - (cx-6)) * 1.6 and (y - (cy-4)) <= ((cx+6) - x) * 1.6:
                                    T_grids[i][y, x] = env_temp

    for i in range(4):
        ims[i].set_array(T_grids[i])
        
    return ims

ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=1, blit=True, repeat=False)
plt.show()
