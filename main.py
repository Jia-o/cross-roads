from cmu_graphics import *
import random

# Game constants
GRID_SIZE = 40
PLAYER_START_ROW = 140
LANE_WIDTH = GRID_SIZE
WIN_SCORE = 50  # Score needed to win the level

# Game state
class GameState:
    def __init__(self):
        self.player_row = PLAYER_START_ROW
        self.player_col = 5
        self.score = 0
        self.game_over = False
        self.camera_offset = 0
        self.furthest_row = PLAYER_START_ROW  # Track the furthest row reached
        self.lanes = []
        self.init_lanes()
    
    def init_lanes(self):
        # Create initial lanes
        for i in range(150):
            # Make sure the starting lane (140) is always grass
            if i == PLAYER_START_ROW:
                self.lanes.append({'type': 'grass'})
            else:
                lane_type = random.choice(['road', 'grass', 'grass', 'water'])
                if lane_type == 'road':
                    speed = random.choice([-1.0, -0.8, -0.6, 0.6, 0.8, 1.0])
                    spacing = random.randint(5, 12)
                    offset = random.randint(0, 20)
                    self.lanes.append({
                        'type': 'road',
                        'speed': speed,
                        'spacing': spacing,
                        'offset': offset,
                        'vehicles': []
                    })
                elif lane_type == 'water':
                    speed = random.choice([-0.9, -0.7, 0.7, 0.9])
                    spacing = random.randint(2, 4)
                    offset = random.randint(0, 10)
                    self.lanes.append({
                        'type': 'water',
                        'speed': speed,
                        'spacing': spacing,
                        'offset': offset,
                        'logs': []
                    })
                else:
                    self.lanes.append({'type': 'grass'})
    
    def add_lane(self):
        lane_type = random.choice(['road', 'grass', 'grass', 'water'])
        if lane_type == 'road':
            speed = random.choice([-1.0, -0.8, -0.6, 0.6, 0.8, 1.0])
            spacing = random.randint(5, 12)
            offset = random.randint(0, 20)
            self.lanes.append({
                'type': 'road',
                'speed': speed,
                'spacing': spacing,
                'offset': offset,
                'vehicles': []
            })
        elif lane_type == 'water':
            speed = random.choice([-0.9, -0.7, 0.7, 0.9])
            spacing = random.randint(2, 4)
            offset = random.randint(0, 10)
            self.lanes.append({
                'type': 'water',
                'speed': speed,
                'spacing': spacing,
                'offset': offset,
                'logs': []
            })
        else:
            self.lanes.append({'type': 'grass'})

game = GameState()

def onAppStart(app):
    app.stepsPerSecond = 30
    reset()

def reset():
    global game
    game = GameState()

def onKeyPress(app, key):
    if game.game_over:
        if key == 'r':
            reset()
        return
    
    old_row = game.player_row
    
    if key == 'up':
        game.player_row -= 1
        if game.player_row < 0:
            game.player_row = 0
    elif key == 'down':
        game.player_row += 1
        if game.player_row >= len(game.lanes):
            game.player_row = len(game.lanes) - 1
    elif key == 'left':
        game.player_col -= 1
        if game.player_col < 0:
            game.player_col = 0
    elif key == 'right':
        game.player_col += 1
        if game.player_col > 9:
            game.player_col = 9
    
    # Update score when moving forward to a new row
    if game.player_row < game.furthest_row:
        game.furthest_row = game.player_row
        game.score += 1
        
        # Update camera
        if game.player_row < 7:
            game.camera_offset = game.player_row - 7
            
        # Add new lanes at the top
        while len(game.lanes) - game.player_row < 10:
            game.add_lane()

def onStep(app):
    if game.game_over:
        return
    
    # Update vehicles and logs
    for lane_idx, lane in enumerate(game.lanes):
        if lane['type'] == 'road':
            # Add vehicles
            lane['offset'] += abs(lane['speed']) / 10
            if lane['offset'] >= lane['spacing']:
                lane['offset'] = 0
                start_col = -2 if lane['speed'] > 0 else 12
                lane['vehicles'].append({'col': start_col, 'row': lane_idx})
            
            # Move vehicles
            for vehicle in lane['vehicles']:
                vehicle['col'] += lane['speed'] * 0.1
            
            # Remove off-screen vehicles
            lane['vehicles'] = [v for v in lane['vehicles'] 
                              if -3 < v['col'] < 13]
            
            # Check collision
            for vehicle in lane['vehicles']:
                if (lane_idx == game.player_row and 
                    abs(vehicle['col'] - game.player_col) < 0.8):
                    game.game_over = True
        
        elif lane['type'] == 'water':
            # Add logs
            lane['offset'] += abs(lane['speed']) / 10
            if lane['offset'] >= lane['spacing']:
                lane['offset'] = 0
                start_col = -3 if lane['speed'] > 0 else 13
                log_length = random.randint(1, 2)
                lane['logs'].append({'col': start_col, 'row': lane_idx, 'length': log_length})
            
            # Move logs
            for log in lane['logs']:
                log['col'] += lane['speed'] * 0.1
            
            # Remove off-screen logs
            lane['logs'] = [l for l in lane['logs'] 
                          if -5 < l['col'] < 15]
            
            # Check if player is on a log in this water lane
            if lane_idx == game.player_row:
                on_log = False
                for log in lane['logs']:
                    # Check if player is on this log
                    log_start = log['col'] - log['length'] / 2
                    log_end = log['col'] + log['length'] / 2
                    if log_start <= game.player_col <= log_end:
                        on_log = True
                        # Move player with the log
                        game.player_col += lane['speed'] * 0.1
                        # Keep player in bounds
                        if game.player_col < 0:
                            game.player_col = 0
                        elif game.player_col > 9:
                            game.player_col = 9
                        break
                
                # If not on a log in water, player drowns
                if not on_log:
                    game.game_over = True

def drawLane(row, lane, screen_y):
    if lane['type'] == 'grass':
        fill = rgb(100, 200, 100)
        drawRect(0, screen_y, 400, LANE_WIDTH, fill=fill)
        # Draw some grass details
        for i in range(0, 400, 20):
            drawCircle(i + 10, screen_y + 15, 3, fill=rgb(80, 180, 80))
            drawCircle(i + 5, screen_y + 25, 2, fill=rgb(80, 180, 80))
    elif lane['type'] == 'water':
        # Water
        fill = rgb(50, 150, 200)
        drawRect(0, screen_y, 400, LANE_WIDTH, fill=fill)
        # Water ripples
        for i in range(0, 400, 30):
            drawOval(i + 15, screen_y + 10, 20, 8, fill=rgb(70, 170, 220), opacity=50)
            drawOval(i + 5, screen_y + 25, 15, 6, fill=rgb(70, 170, 220), opacity=50)
    else:
        # Road
        fill = rgb(60, 60, 70)
        drawRect(0, screen_y, 400, LANE_WIDTH, fill=fill)
        # Road markings
        if row % 2 == 0:
            for i in range(0, 400, 40):
                drawRect(i, screen_y + LANE_WIDTH//2 - 2, 20, 4, 
                        fill='white', opacity=50)

def drawVehicle(col, screen_y, speed):
    x = col * GRID_SIZE
    y = screen_y + LANE_WIDTH // 2
    
    # Vehicle color based on direction
    if speed > 0:
        color = rgb(255, 100, 100)  # Red car going right
        drawRect(x - 15, y - 8, 30, 16, fill=color, border='darkRed', borderWidth=2)
        drawCircle(x - 8, y + 8, 4, fill='black')
        drawCircle(x + 8, y + 8, 4, fill='black')
        drawRect(x + 8, y - 6, 8, 12, fill='lightBlue')  # Windshield
    else:
        color = rgb(100, 100, 255)  # Blue car going left
        drawRect(x - 15, y - 8, 30, 16, fill=color, border='darkBlue', borderWidth=2)
        drawCircle(x - 8, y + 8, 4, fill='black')
        drawCircle(x + 8, y + 8, 4, fill='black')
        drawRect(x - 16, y - 6, 8, 12, fill='lightBlue')  # Windshield

def drawLog(col, length, screen_y):
    x = col * GRID_SIZE
    y = screen_y + LANE_WIDTH // 2
    
    # Draw log
    log_width = length * GRID_SIZE
    drawRect(x - log_width/2, y - 12, log_width, 24, fill=rgb(139, 90, 43), 
             border=rgb(101, 67, 33), borderWidth=2)
    # Add wood texture lines
    for i in range(int(length)):
        line_x = x - log_width/2 + i * GRID_SIZE + GRID_SIZE/2
        drawLine(line_x, y - 12, line_x, y + 12, fill=rgb(101, 67, 33), lineWidth=1)

def drawPlayer(col, screen_y):
    x = col * GRID_SIZE
    y = screen_y + LANE_WIDTH // 2
    
    # Draw simple character (chicken style)
    drawCircle(x, y - 5, 8, fill='yellow', border='orange', borderWidth=2)  # Head
    drawCircle(x, y + 5, 10, fill='yellow', border='orange', borderWidth=2)  # Body
    drawCircle(x - 3, y - 7, 2, fill='black')  # Eye
    drawCircle(x + 3, y - 7, 2, fill='black')  # Eye
    drawPolygon(x, y - 3, x - 3, y - 1, x + 3, y - 1, fill='orange')  # Beak

def redrawAll(app):
    # Background
    drawRect(0, 0, 400, 400, fill=rgb(135, 206, 235))  # Sky blue
    
    # Calculate visible lanes
    start_row = max(0, game.player_row - 7 + game.camera_offset)
    end_row = min(len(game.lanes), start_row + 15)
    
    # Draw lanes
    for i, row in enumerate(range(start_row, end_row)):
        screen_y = i * LANE_WIDTH
        lane = game.lanes[row]
        drawLane(row, lane, screen_y)
        
        # Draw vehicles
        if lane['type'] == 'road':
            for vehicle in lane['vehicles']:
                drawVehicle(vehicle['col'], screen_y, lane['speed'])
        
        # Draw logs
        elif lane['type'] == 'water':
            for log in lane['logs']:
                drawLog(log['col'], log['length'], screen_y)
    
    # Draw player
    player_screen_row = game.player_row - start_row
    player_y = player_screen_row * LANE_WIDTH
    drawPlayer(game.player_col, player_y)
    
    # Draw UI
    drawRect(0, 0, 400, 40, fill='black', opacity=70)
    drawLabel(f'Score: {game.score}', 200, 20, size=20, fill='white', bold=True)
    
    if game.game_over:
        drawRect(0, 0, 400, 400, fill='black', opacity=80)
        drawLabel('GAME OVER!', 200, 150, size=40, fill='red', bold=True)
        drawLabel(f'Final Score: {game.score}', 200, 200, size=25, fill='white', bold=True)
        drawLabel('Press R to Restart', 200, 250, size=20, fill='white')

runApp(width=400, height=400)