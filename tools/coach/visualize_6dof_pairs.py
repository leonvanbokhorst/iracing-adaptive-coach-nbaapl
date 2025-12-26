#!/usr/bin/env python3
"""
Visualize the 6 Degrees of Freedom as CAUSE-EFFECT PAIRS

Shows the relationship between forces and rotations:
1. Longitudinal G → Pitch
2. Lateral G → Roll  
3. Combined G → Yaw

Usage:
    python tools/coach/visualize_6dof_pairs.py [--output-dir path/to/dir]
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Arc, Rectangle, Circle, FancyBboxPatch
from matplotlib.transforms import Affine2D
import numpy as np
import argparse
from pathlib import Path


def draw_car_top_view(ax, x, y, width, length, color='#333333'):
    """Draw a simple top-down car"""
    car = Rectangle((x - width/2, y - length/2), width, length, 
                    facecolor=color, edgecolor='black', linewidth=2, zorder=3)
    ax.add_patch(car)
    
    wheel_width = width * 0.15
    wheel_length = length * 0.2
    wheel_offset_x = width * 0.4
    wheel_offset_y = length * 0.4
    
    for wx, wy in [(-wheel_offset_x, wheel_offset_y), (wheel_offset_x, wheel_offset_y),
                   (-wheel_offset_x, -wheel_offset_y), (wheel_offset_x, -wheel_offset_y)]:
        wheel = Rectangle((x + wx - wheel_width/2, y + wy - wheel_length/2),
                         wheel_width, wheel_length, facecolor='black', zorder=4)
        ax.add_patch(wheel)
    
    driver = Circle((x, y), width * 0.15, facecolor='#ff6b6b', 
                   edgecolor='black', linewidth=1, zorder=5)
    ax.add_patch(driver)
    
    nose = Circle((x, y + length/2), width * 0.08, facecolor='white', 
                 edgecolor='black', linewidth=1, zorder=5)
    ax.add_patch(nose)


def draw_car_side_view(ax, x, y, width, height, color='#333333'):
    """Draw a simple side view car"""
    body_height = height * 0.4
    car = Rectangle((x - width/2, y), width, body_height,
                   facecolor=color, edgecolor='black', linewidth=2, zorder=3)
    ax.add_patch(car)
    
    cockpit_x = x - width * 0.1
    cockpit_width = width * 0.3
    cockpit = Rectangle((cockpit_x - cockpit_width/2, y + body_height),
                       cockpit_width, body_height * 0.6,
                       facecolor=color, edgecolor='black', linewidth=2, zorder=3)
    ax.add_patch(cockpit)
    
    wheel_radius = height * 0.15
    wheel_offset = width * 0.35
    
    for wx in [-wheel_offset, wheel_offset]:
        wheel = Circle((x + wx, y), wheel_radius,
                      facecolor='black', edgecolor='black', linewidth=2, zorder=4)
        ax.add_patch(wheel)
    
    driver = Circle((cockpit_x, y + body_height + body_height * 0.3), wheel_radius * 0.5,
                   facecolor='#ff6b6b', edgecolor='black', linewidth=1, zorder=5)
    ax.add_patch(driver)


def create_longitudinal_pitch_pair(output_path=None):
    """Longitudinal G Force → Pitch Response"""
    
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Color scheme: Blue-purple for this pair
    force_color = '#3498db'
    response_color = '#9b59b6'
    
    # ===== LEFT: LONGITUDINAL FORCE =====
    ax = ax_left
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Title
    ax.text(0, 1.85, 'FORCE: Longitudinal G', fontsize=16,
            fontweight='bold', ha='center', color=force_color)
    ax.text(0, 1.6, '(What YOU Create)', fontsize=12,
            ha='center', style='italic', color='#666')
    
    # Draw car (top view)
    draw_car_top_view(ax, 0, 0, 0.8, 1.5, color=force_color)
    
    # Braking arrow (front, pointing back)
    arrow = FancyArrowPatch((0, 1.5), (0, 0.9),
                           arrowstyle='->', mutation_scale=40,
                           linewidth=5, color='#e74c3c', zorder=2)
    ax.add_patch(arrow)
    ax.text(0.5, 1.2, 'BRAKE\n(−G)', fontsize=13, fontweight='bold',
            color='#e74c3c', ha='center')
    
    # Acceleration arrow (rear, pointing forward)
    arrow = FancyArrowPatch((0, -1.5), (0, -0.9),
                           arrowstyle='->', mutation_scale=40,
                           linewidth=5, color='#2ecc71', zorder=2)
    ax.add_patch(arrow)
    ax.text(-0.5, -1.2, 'ACCEL\n(+G)', fontsize=13, fontweight='bold',
            color='#2ecc71', ha='center')
    
    # Info box
    info_text = (
        "Braking: Weight shifts forward\n"
        "Acceleration: Weight shifts back\n\n"
        "Telemetry: Longitudinal G trace"
    )
    ax.text(0, -1.75, info_text, fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.7))
    
    # ===== RIGHT: PITCH RESPONSE =====
    ax = ax_right
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Title
    ax.text(0, 1.85, 'RESPONSE: Pitch Rotation', fontsize=16,
            fontweight='bold', ha='center', color=response_color)
    ax.text(0, 1.6, '(What the CAR Does)', fontsize=12,
            ha='center', style='italic', color='#666')
    
    # Neutral car (faded)
    draw_car_side_view(ax, 0, -0.3, 1.5, 0.8, color='#ecf0f1')
    
    # Pitched forward car (braking - nose dive)
    t_brake = Affine2D().rotate_deg_around(-0.3, -0.3, -12) + ax.transData
    
    body = Rectangle((-1.05, -0.3), 1.5, 0.32,
                    facecolor='#e74c3c', edgecolor='black',
                    linewidth=2, zorder=3, alpha=0.7, transform=t_brake)
    ax.add_patch(body)
    
    cockpit = Rectangle((-0.45, 0.02), 0.45, 0.24,
                       facecolor='#e74c3c', edgecolor='black',
                       linewidth=2, zorder=3, alpha=0.7, transform=t_brake)
    ax.add_patch(cockpit)
    
    for wx in [-0.525, 0.525]:
        wheel = Circle((-0.3 + wx, -0.3), 0.12, facecolor='black',
                      edgecolor='black', linewidth=2, zorder=4, transform=t_brake)
        ax.add_patch(wheel)
    
    # Rotation arrow (nose dive)
    arc = Arc((-0.3, -0.3), 1.8, 1.8, angle=0, theta1=200, theta2=300,
             color='#e74c3c', linewidth=4, zorder=2)
    ax.add_patch(arc)
    
    arrow = FancyArrowPatch((-1.1, 0.25), (-1.15, 0.4),
                           arrowstyle='->', mutation_scale=25,
                           linewidth=4, color='#e74c3c', zorder=2)
    ax.add_patch(arrow)
    
    ax.text(-1.5, 0.6, 'NOSE\nDIVE', fontsize=11, fontweight='bold',
            color='#e74c3c', ha='center')
    
    # Pitched backward car (accelerating - squat)
    t_accel = Affine2D().rotate_deg_around(0.3, -0.3, 8) + ax.transData
    
    body2 = Rectangle((0.3 - 0.75, -0.3), 1.5, 0.32,
                     facecolor='#2ecc71', edgecolor='black',
                     linewidth=2, zorder=3, alpha=0.7, transform=t_accel)
    ax.add_patch(body2)
    
    cockpit2 = Rectangle((0.3 - 0.15, 0.02), 0.45, 0.24,
                        facecolor='#2ecc71', edgecolor='black',
                        linewidth=2, zorder=3, alpha=0.7, transform=t_accel)
    ax.add_patch(cockpit2)
    
    for wx in [-0.525, 0.525]:
        wheel = Circle((0.3 + wx, -0.3), 0.12, facecolor='black',
                      edgecolor='black', linewidth=2, zorder=4, transform=t_accel)
        ax.add_patch(wheel)
    
    # Rotation arrow (squat)
    arc2 = Arc((0.3, -0.3), 1.8, 1.8, angle=0, theta1=240, theta2=340,
              color='#2ecc71', linewidth=4, zorder=2)
    ax.add_patch(arc2)
    
    arrow2 = FancyArrowPatch((1.1, 0.25), (1.15, 0.4),
                            arrowstyle='->', mutation_scale=25,
                            linewidth=4, color='#2ecc71', zorder=2)
    ax.add_patch(arrow2)
    
    ax.text(1.5, 0.6, 'REAR\nSQUAT', fontsize=11, fontweight='bold',
            color='#2ecc71', ha='center')
    
    # Axis line
    ax.plot([-1.2, 1.2], [-0.3, -0.3], 'k--', linewidth=2, alpha=0.4, zorder=1)
    ax.text(0, -0.65, '← Pitch Axis (lateral) →', fontsize=10,
            ha='center', fontweight='bold', color='#666')
    
    # Info box
    info_text = (
        "Nose dive: Front loads, rear unloads\n"
        "Squat: Rear loads, front unloads\n\n"
        "Telemetry: Long G transitions"
    )
    ax.text(0, -1.75, info_text, fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.7))
    
    # Main title
    fig.suptitle('Longitudinal G Force → Pitch Rotation\n' +
                 '"Brake/Accel makes the car pitch forward/back"',
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Connection arrow between panels
    fig.text(0.5, 0.5, '→', fontsize=60, ha='center', va='center',
            color=response_color, weight='bold', alpha=0.3)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Saved Longitudinal→Pitch visualization to: {output_path}")
    else:
        plt.show()
    
    plt.close()


def create_lateral_roll_pair(output_path=None):
    """Lateral G Force → Roll Response"""
    
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Color scheme: Orange for this pair
    force_color = '#e67e22'
    response_color = '#e74c3c'
    
    # ===== LEFT: LATERAL FORCE =====
    ax = ax_left
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Title
    ax.text(0, 1.85, 'FORCE: Lateral G', fontsize=16,
            fontweight='bold', ha='center', color=force_color)
    ax.text(0, 1.6, '(What YOU Create)', fontsize=12,
            ha='center', style='italic', color='#666')
    
    # Draw car (top view)
    draw_car_top_view(ax, 0, 0, 0.8, 1.5, color=force_color)
    
    # Left turn arrow
    arrow = FancyArrowPatch((-0.5, 0), (-1.5, 0),
                           arrowstyle='->', mutation_scale=40,
                           linewidth=5, color=force_color, zorder=2)
    ax.add_patch(arrow)
    ax.text(-1.0, -0.5, 'LEFT\nTURN', fontsize=13, fontweight='bold',
            color=force_color, ha='center')
    
    # Right turn arrow
    arrow = FancyArrowPatch((0.5, 0), (1.5, 0),
                           arrowstyle='->', mutation_scale=40,
                           linewidth=5, color=force_color, zorder=2)
    ax.add_patch(arrow)
    ax.text(1.0, 0.5, 'RIGHT\nTURN', fontsize=13, fontweight='bold',
            color=force_color, ha='center')
    
    # Corner path visualization
    theta = np.linspace(0, np.pi/2, 50)
    radius = 1.2
    path_x = -radius + radius * np.cos(theta)
    path_y = -radius + radius * np.sin(theta)
    ax.plot(path_x, path_y, 'k--', linewidth=2, alpha=0.3, zorder=1)
    ax.arrow(path_x[35], path_y[35], 
            path_x[40]-path_x[35], path_y[40]-path_y[35],
            head_width=0.1, head_length=0.05, fc='black', alpha=0.3, zorder=1)
    
    # Info box
    info_text = (
        "Cornering: Weight shifts to outside\n"
        "Higher speed = More lateral G\n\n"
        "Telemetry: Lateral G trace"
    )
    ax.text(0, -1.75, info_text, fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.7))
    
    # ===== RIGHT: ROLL RESPONSE =====
    ax = ax_right
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Title
    ax.text(0, 1.85, 'RESPONSE: Roll Rotation', fontsize=16,
            fontweight='bold', ha='center', color=response_color)
    ax.text(0, 1.6, '(What the CAR Does)', fontsize=12,
            ha='center', style='italic', color='#666')
    
    # Neutral car (faded, centered)
    car_neutral = Rectangle((-0.6, 0.2), 1.2, 0.5,
                           facecolor='#ecf0f1', edgecolor='black',
                           linewidth=2, alpha=0.4, zorder=1)
    ax.add_patch(car_neutral)
    
    # Neutral wheels
    wheel_n1 = Circle((-0.5, 0.15), 0.12, facecolor='#666',
                     edgecolor='black', linewidth=1, alpha=0.4, zorder=1)
    wheel_n2 = Circle((0.5, 0.15), 0.12, facecolor='#666',
                     edgecolor='black', linewidth=1, alpha=0.4, zorder=1)
    ax.add_patch(wheel_n1)
    ax.add_patch(wheel_n2)
    
    ax.text(0, 0.95, 'Neutral (upright)', fontsize=9,
            ha='center', color='#666', style='italic')
    
    # Rolled car (left turn - leans right) - BIGGER and CLEARER
    car_roll_right = Rectangle((-0.6, -0.5), 1.2, 0.5,
                              facecolor=force_color, edgecolor='black',
                              linewidth=3, zorder=3)
    t_right = Affine2D().rotate_deg_around(0, -0.25, -20) + ax.transData
    car_roll_right.set_transform(t_right)
    ax.add_patch(car_roll_right)
    
    # Wheels (rolled)
    wheel_left = Circle((-0.5, -0.55), 0.13, facecolor='black',
                       edgecolor='black', linewidth=2, transform=t_right, zorder=4)
    wheel_right = Circle((0.5, -0.55), 0.13, facecolor='black',
                        edgecolor='black', linewidth=2, transform=t_right, zorder=4)
    ax.add_patch(wheel_left)
    ax.add_patch(wheel_right)
    
    # Driver (red dot)
    driver = Circle((0, -0.25), 0.12, facecolor='#ff6b6b',
                   edgecolor='black', linewidth=1.5, transform=t_right, zorder=5)
    ax.add_patch(driver)
    
    # Rotation arrow (big curved arrow)
    arc_right = Arc((0, -0.25), 2.0, 2.0, angle=0, theta1=165, theta2=15,
                   color=response_color, linewidth=5, zorder=2)
    ax.add_patch(arc_right)
    
    arrow = FancyArrowPatch((0.85, 0.3), (0.95, 0.45),
                           arrowstyle='->', mutation_scale=30,
                           linewidth=5, color=response_color, zorder=2)
    ax.add_patch(arrow)
    
    # Label
    ax.text(1.4, 0.5, 'LEAN\nRIGHT', fontsize=14, fontweight='bold',
            color=response_color, ha='center')
    ax.text(1.4, 0.0, '(In a left turn)', fontsize=10,
            color='#666', ha='center', style='italic')
    
    # Show weight shift with annotations
    ax.text(-0.7, -0.85, 'Outside tires\nCOMPRESS\n(more load)', fontsize=9,
            ha='center', color=response_color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor=response_color, linewidth=2))
    
    ax.text(0.7, -0.85, 'Inside tires\nEXTEND\n(less load)', fontsize=9,
            ha='center', color='#666', style='italic',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor='#999', linewidth=1, linestyle='--'))
    
    # Axis indicator
    ax.plot([-1.5, 1.5], [-0.25, -0.25], 'k--', linewidth=2, alpha=0.4, zorder=1)
    ax.text(0, -1.35, '← Roll Axis (longitudinal, front-to-back) →', fontsize=10,
            ha='center', fontweight='bold', color='#666')
    
    # Info box
    info_text = (
        "Outside tires compress (more load)\n"
        "Inside tires extend (less load)\n\n"
        "Telemetry: Lateral G ramp rate"
    )
    ax.text(0, -1.75, info_text, fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.7))
    
    # Main title
    fig.suptitle('Lateral G Force → Roll Rotation\n' +
                 '"Cornering makes the car lean to the outside"',
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Connection arrow
    fig.text(0.5, 0.5, '→', fontsize=60, ha='center', va='center',
            color=response_color, weight='bold', alpha=0.3)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Saved Lateral→Roll visualization to: {output_path}")
    else:
        plt.show()
    
    plt.close()


def create_combined_yaw_pair(output_path=None):
    """Combined G Forces → Yaw Response"""
    
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(14, 7))
    
    # Color scheme: Green for neutral, red for problem
    force_color = '#27ae60'
    problem_color = '#e74c3c'
    
    # ===== LEFT: COMBINED FORCES =====
    ax = ax_left
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Title
    ax.text(0, 1.85, 'FORCE: Combined G (Long + Lat)', fontsize=16,
            fontweight='bold', ha='center', color=force_color)
    ax.text(0, 1.6, '(What YOU Create)', fontsize=12,
            ha='center', style='italic', color='#666')
    
    # Draw car (top view)
    draw_car_top_view(ax, 0, 0, 0.8, 1.5, color=force_color)
    
    # Combined force arrows (trail braking scenario)
    # Brake arrow (smaller, fading)
    arrow_brake = FancyArrowPatch((0.3, 0.9), (0.3, 0.4),
                                 arrowstyle='->', mutation_scale=30,
                                 linewidth=4, color='#e74c3c', zorder=2, alpha=0.7)
    ax.add_patch(arrow_brake)
    ax.text(0.8, 0.65, 'Brake\n(fading)', fontsize=10, fontweight='bold',
            color='#e74c3c', ha='center')
    
    # Turn arrow (growing)
    arrow_turn = FancyArrowPatch((-0.5, -0.3), (-1.2, -0.3),
                                arrowstyle='->', mutation_scale=35,
                                linewidth=5, color='#e67e22', zorder=2)
    ax.add_patch(arrow_turn)
    ax.text(-0.85, -0.8, 'Turn\n(adding)', fontsize=10, fontweight='bold',
            color='#e67e22', ha='center')
    
    # Traction circle representation (small)
    circle = plt.Circle((0, -1.3), 0.3, fill=False, edgecolor='#2ecc71',
                       linewidth=2, linestyle='--', zorder=1)
    ax.add_patch(circle)
    
    # Point on circle (at limit)
    ax.plot([0], [-1.1], 'o', markersize=10, color=force_color, zorder=3)
    ax.text(0.4, -1.3, 'At limit\n(on circle)', fontsize=8,
            ha='left', va='center', color=force_color)
    
    # Info box
    info_text = (
        "Trail braking: Brake + Turn together\n"
        "Balance determines rotation\n\n"
        "Telemetry: Traction circle path"
    )
    ax.text(0, -1.9, info_text, fontsize=10, ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.7))
    
    # ===== RIGHT: YAW RESPONSE =====
    ax = ax_right
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_axis_off()
    
    # Title
    ax.text(0, 1.85, 'RESPONSE: Yaw Rotation', fontsize=16,
            fontweight='bold', ha='center', color='#666')
    ax.text(0, 1.6, '(What the CAR Does)', fontsize=12,
            ha='center', style='italic', color='#666')
    
    # Three scenarios side by side
    
    # --- NEUTRAL (center) ---
    x_neutral = 0
    draw_car_top_view(ax, x_neutral, 0, 0.6, 1.0, color=force_color)
    
    # Rotation arrow (smooth)
    arc_neutral = Arc((x_neutral, 0), 1.8, 1.8, angle=0, theta1=100, theta2=200,
                     color=force_color, linewidth=3, zorder=2)
    ax.add_patch(arc_neutral)
    
    arrow = FancyArrowPatch((x_neutral - 0.7, 0.6), (x_neutral - 0.8, 0.7),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=3, color=force_color, zorder=2)
    ax.add_patch(arrow)
    
    ax.text(x_neutral, -0.85, 'NEUTRAL\nPerfect rotation', fontsize=10,
            fontweight='bold', ha='center', color=force_color)
    
    # --- UNDERSTEER (left) ---
    x_under = -1.0
    
    # Car pointing more forward (not turning enough)
    car_under = Rectangle((x_under - 0.3, -0.5), 0.6, 1.0,
                         facecolor=problem_color, edgecolor='black',
                         linewidth=2, zorder=3, alpha=0.6)
    t_under = Affine2D().rotate_deg_around(x_under, 0, 15) + ax.transData
    car_under.set_transform(t_under)
    ax.add_patch(car_under)
    
    # Wheels
    for wx, wy in [(-0.24, 0.4), (0.24, 0.4), (-0.24, -0.4), (0.24, -0.4)]:
        wheel = Rectangle((x_under + wx - 0.09, wy - 0.15),
                         0.09, 0.15, facecolor='black', zorder=4, transform=t_under)
        ax.add_patch(wheel)
    
    # Driver
    driver = Circle((x_under, 0), 0.09, facecolor='#ff6b6b',
                   edgecolor='black', linewidth=1, zorder=5, transform=t_under)
    ax.add_patch(driver)
    
    # Nose
    nose = Circle((x_under, 0.5), 0.05, facecolor='white',
                 edgecolor='black', linewidth=1, zorder=5, transform=t_under)
    ax.add_patch(nose)
    
    # Weak rotation arrow
    arc_under = Arc((x_under, 0), 1.4, 1.4, angle=0, theta1=100, theta2=170,
                   color=problem_color, linewidth=2, linestyle='--', zorder=2)
    ax.add_patch(arc_under)
    
    ax.text(x_under, -0.85, 'UNDERSTEER\nWon\'t turn', fontsize=10,
            fontweight='bold', ha='center', color=problem_color)
    
    # --- OVERSTEER (right) ---
    x_over = 1.0
    
    # Car rotated too much
    car_over = Rectangle((x_over - 0.3, -0.5), 0.6, 1.0,
                        facecolor=problem_color, edgecolor='black',
                        linewidth=2, zorder=3, alpha=0.6)
    t_over = Affine2D().rotate_deg_around(x_over, 0, 55) + ax.transData
    car_over.set_transform(t_over)
    ax.add_patch(car_over)
    
    # Wheels
    for wx, wy in [(-0.24, 0.4), (0.24, 0.4), (-0.24, -0.4), (0.24, -0.4)]:
        wheel = Rectangle((x_over + wx - 0.09, wy - 0.15),
                         0.09, 0.15, facecolor='black', zorder=4, transform=t_over)
        ax.add_patch(wheel)
    
    # Driver
    driver = Circle((x_over, 0), 0.09, facecolor='#ff6b6b',
                   edgecolor='black', linewidth=1, zorder=5, transform=t_over)
    ax.add_patch(driver)
    
    # Nose
    nose = Circle((x_over, 0.5), 0.05, facecolor='white',
                 edgecolor='black', linewidth=1, zorder=5, transform=t_over)
    ax.add_patch(nose)
    
    # Over-rotation arrow
    arc_over = Arc((x_over, 0), 1.4, 1.4, angle=0, theta1=80, theta2=200,
                  color=problem_color, linewidth=3, zorder=2)
    ax.add_patch(arc_over)
    
    arrow_over = FancyArrowPatch((x_over - 0.5, 0.6), (x_over - 0.6, 0.75),
                                arrowstyle='->', mutation_scale=20,
                                linewidth=3, color=problem_color, zorder=2)
    ax.add_patch(arrow_over)
    
    ax.text(x_over, -0.85, 'OVERSTEER\nToo much turn', fontsize=10,
            fontweight='bold', ha='center', color=problem_color)
    
    # Vertical axis indicator (through neutral car)
    ax.plot([0, 0], [-1.5, 1.5], 'k--', linewidth=1, alpha=0.3, zorder=1)
    ax.text(0, 1.15, '↑ Yaw Axis (vertical)', fontsize=10,
            ha='center', fontweight='bold', color='#666')
    
    # Info box
    info_text = (
        "Neutral: Steering matches grip\n"
        "Understeer: Too much speed/not enough grip\n"
        "Oversteer: Rear loses grip first\n\n"
        "Telemetry: Steering vs Lateral G"
    )
    ax.text(0, -1.9, info_text, fontsize=9, ha='center',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='wheat', alpha=0.7))
    
    # Main title
    fig.suptitle('Combined G Forces → Yaw Rotation\n' +
                 '"How you balance brake+turn determines rotation"',
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Connection arrow
    fig.text(0.5, 0.5, '→', fontsize=60, ha='center', va='center',
            color='#666', weight='bold', alpha=0.3)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✅ Saved Combined→Yaw visualization to: {output_path}")
    else:
        plt.show()
    
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description='Visualize the 6DOF as cause-effect pairs'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='assets',
        help='Output directory (default: assets)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("🎨 Generating 6DOF cause-effect visualizations...")
    print()
    
    create_longitudinal_pitch_pair(output_dir / 'longitudinal-pitch-pair.png')
    create_lateral_roll_pair(output_dir / 'lateral-roll-pair.png')
    create_combined_yaw_pair(output_dir / 'combined-yaw-pair.png')
    
    print()
    print("✨ All three visualizations created!")
    print(f"📁 Location: {output_dir}/")
    print()
    print("Generated files:")
    print("  1. longitudinal-pitch-pair.png - Brake/Accel → Pitch")
    print("  2. lateral-roll-pair.png - Cornering → Roll")
    print("  3. combined-yaw-pair.png - Combined Forces → Yaw")


if __name__ == "__main__":
    main()

