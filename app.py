from flask import Flask, jsonify, request, send_from_directory
import os

from flask import session, make_response
import math

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'car-game-demo-key'  # Needed for session

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('templates', 'index.html')


@app.route('/about')
def about():
    """Serve a simple About page that teaches routes"""
    return send_from_directory('templates', 'about.html')


# Car game route

# SVG-based car game (server-side state)
@app.route('/car-game')
def car_game():
    return send_from_directory('templates', 'car_game_svg.html')

@app.route('/car-game/state', methods=['POST'])

def car_game_state():
    # Bigger canvas and track
    W, H = 800, 500
    cx, cy = W//2, H//2
    trackA, trackB, trackW = 320, 180, 70
    carW, carH = 48, 72
    # Get or init state
    state = session.get('car_game_state')
    if not state:
        # Add velocity and angular velocity for smooth movement
        state = {
            'x': cx,
            'y': cy+trackB-trackW/2-40,
            'angle': -math.pi/2,
            'vx': 0.0,
            'vy': 0.0,
            'speed': 0.0,
            'angular_velocity': 0.0
        }
    # Get input
    import json
    data = json.loads(request.data)
    key = data.get('key')
    # Super-smooth controls: velocity and angular velocity
    x = state['x']
    y = state['y']
    angle = state['angle']
    vx = state.get('vx', 0.0)
    vy = state.get('vy', 0.0)
    speed = state.get('speed', 0.0)
    angular_velocity = state.get('angular_velocity', 0.0)
    handbrake = (key == ' ')
    accel = 0.28 if not handbrake else 0.13  # faster acceleration
    turn_accel = 0.014 if not handbrake else 0.028
    max_speed = 13.0 if not handbrake else 7.0  # higher top speed
    max_angular = 0.11 if not handbrake else 0.18
    friction = 0.987 if not handbrake else 0.965
    angular_friction = 0.93

    # Controls: left/right adjust angular velocity, up accelerates, down brakes
    if key == 'ArrowLeft':
        angular_velocity -= turn_accel
    if key == 'ArrowRight':
        angular_velocity += turn_accel
    if key == 'ArrowUp':
        speed += accel
    if key == 'ArrowDown':
        speed -= accel * 1.2

    # Clamp angular velocity and speed
    angular_velocity = max(-max_angular, min(angular_velocity, max_angular))
    speed = max(-max_speed, min(speed, max_speed))

    # Apply friction
    speed *= friction
    angular_velocity *= angular_friction

    # Update angle
    angle += angular_velocity

    # Update velocity vector based on angle and speed
    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed

    # Move
    x += vx
    y += vy
    # Stay on track (oval math)
    dx = x-cx
    dy = y-cy
    dist = ((dx*dx)/((trackA-trackW/2)**2) + (dy*dy)/((trackB-trackW/2)**2))
    if dist > 1:
        # push back in
        theta = math.atan2(dy, dx)
        x = cx + math.cos(theta)*(trackA-trackW/2)*0.98
        y = cy + math.sin(theta)*(trackB-trackW/2)*0.98
        speed *= -0.4
        angular_velocity *= -0.5
    # Save state
    state = {
        'x': x,
        'y': y,
        'angle': angle,
        'vx': vx,
        'vy': vy,
        'speed': speed,
        'angular_velocity': angular_velocity
    }
    session['car_game_state'] = state
    # Render SVG
    svg = render_car_game_svg(state, W, H, trackA, trackB, trackW, carW, carH)
    resp = make_response(svg)
    resp.headers['Content-Type'] = 'image/svg+xml'
    return resp

def render_car_game_svg(state, W, H, trackA, trackB, trackW, carW, carH):
    cx, cy = W//2, H//2
    # Redesigned car SVG: clearer front/rear, wheels, direction
    # Rotate car SVG by -90 degrees so the front (headlights) points in the direction of movement
    car_svg = f'''
    <g transform="translate({state['x']},{state['y']}) rotate({state['angle']*180/3.14159 - 90})">
        <!-- Rear spoiler -->
        <rect x="{-carW/2}" y="{-carH/2-10}" width="{carW}" height="8" rx="2" fill="#333"/>
        <!-- Wheels -->
        <ellipse cx="{-carW/2+8}" cy="{-carH/2+18}" rx="7" ry="5" fill="#222"/>
        <ellipse cx="{carW/2-8}" cy="{-carH/2+18}" rx="7" ry="5" fill="#222"/>
        <ellipse cx="{-carW/2+8}" cy="{carH/2-18}" rx="7" ry="5" fill="#222"/>
        <ellipse cx="{carW/2-8}" cy="{carH/2-18}" rx="7" ry="5" fill="#222"/>
        <!-- Car body -->
        <rect x="{-carW/2}" y="{-carH/2}" width="{carW}" height="{carH}" rx="12" fill="#1976d2" stroke="#333" stroke-width="3"/>
        <!-- Roof -->
        <rect x="{-carW/4}" y="{-carH/2+12}" width="{carW/2}" height="{carH/2}" rx="7" fill="#e3e3e3" stroke="#aaa" stroke-width="2"/>
        <!-- Windshield (front) -->
        <rect x="{-carW/4}" y="{-carH/2}" width="{carW/2}" height="{carH/7}" rx="3" fill="#90caf9"/>
        <!-- Front bumper -->
        <rect x="{-carW/2+8}" y="{carH/2-8}" width="{carW-16}" height="10" rx="4" fill="#333"/>
        <!-- Headlights (front) -->
        <ellipse cx="{-carW/4}" cy="{carH/2-2}" rx="5" ry="2.5" fill="#fffde4"/>
        <ellipse cx="{carW/4}" cy="{carH/2-2}" rx="5" ry="2.5" fill="#fffde4"/>
        <!-- Taillights (rear) -->
        <ellipse cx="{-carW/4}" cy="{-carH/2+2}" rx="4" ry="2" fill="#ff5252"/>
        <ellipse cx="{carW/4}" cy="{-carH/2+2}" rx="4" ry="2" fill="#ff5252"/>
        <!-- Direction arrow (front) -->
        <polygon points="0,{carH/2-2} -7,{carH/2-14} 7,{carH/2-14}" fill="#ffd600" opacity="0.7"/>
    </g>
    '''
    svg = f'''<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#2e7d32"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{trackA}" ry="{trackB}" fill="#888"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{trackA-trackW}" ry="{trackB-trackW}" fill="#2e7d32"/>
    <ellipse cx="{cx}" cy="{cy}" rx="{trackA-trackW/2}" ry="{trackB-trackW/2}" fill="none" stroke="#fff" stroke-dasharray="18,18" stroke-width="4"/>
    {car_svg}
    </svg>'''
    return svg



if __name__ == '__main__':
    app.run(debug=True, port=5000)
