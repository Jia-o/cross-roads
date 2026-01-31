from cmu_graphics import *
import random
import math

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
        self.character = 'duck'  # Can be 'duck', 'frog', or 'fish'
        self.death_type = None  # 'road' or 'water'
        self.death_animation_frame = 0  # Track animation progress
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
    app.selectedCharacter = 'duck'  # Store selected character in app

def reset(app):
    global game
    game = GameState()
    game.character = app.selectedCharacter  # Use the selected character

############################################################
# Character Selection Screen
############################################################
def start_redrawAll(app):
    # Background
    drawRect(0, 0, 400, 400, fill=rgb(135, 206, 235))
    
    # Title
    drawLabel('CROSSY ROAD', 200, 50, size=40, fill='white', bold=True)
    drawLabel('Select Your Character', 200, 100, size=20, fill='white')
    
    # Character boxes
    box_y = 200
    box_width = 100
    box_height = 120
    
    # Duck
    duck_x = 70
    if app.selectedCharacter == 'duck':
        drawRect(duck_x - box_width//2, box_y - box_height//2, box_width, box_height, 
                fill='gold', border='yellow', borderWidth=4)
    else:
        drawRect(duck_x - box_width//2, box_y - box_height//2, box_width, box_height, 
                fill='white', border='gray', borderWidth=2)
    drawCircle(duck_x, box_y - 15, 8, fill='yellow', border='orange', borderWidth=2)
    drawCircle(duck_x, box_y - 5, 10, fill='yellow', border='orange', borderWidth=2)
    drawCircle(duck_x - 3, box_y - 17, 2, fill='black')
    drawCircle(duck_x + 3, box_y - 17, 2, fill='black')
    drawPolygon(duck_x, box_y - 13, duck_x - 3, box_y - 11, duck_x + 3, box_y - 11, fill='orange')
    drawLabel('Duck', duck_x, box_y + 30, size=16, bold=True)
    drawLabel('Press 1', duck_x, box_y + 45, size=12)
    
    # Frog
    frog_x = 200
    if app.selectedCharacter == 'frog':
        drawRect(frog_x - box_width//2, box_y - box_height//2, box_width, box_height, 
                fill='gold', border='yellow', borderWidth=4)
    else:
        drawRect(frog_x - box_width//2, box_y - box_height//2, box_width, box_height, 
                fill='white', border='gray', borderWidth=2)
    drawCircle(frog_x, box_y - 10, 12, fill='green', border='darkGreen', borderWidth=2)
    drawCircle(frog_x - 5, box_y - 13, 5, fill='lightGreen', border='darkGreen', borderWidth=1)
    drawCircle(frog_x + 5, box_y - 13, 5, fill='lightGreen', border='darkGreen', borderWidth=1)
    drawCircle(frog_x - 5, box_y - 13, 2, fill='black')
    drawCircle(frog_x + 5, box_y - 13, 2, fill='black')
    drawRect(frog_x - 2, box_y - 5, 4, 2, fill='darkGreen')
    drawLabel('Frog', frog_x, box_y + 30, size=16, bold=True)
    drawLabel('Press 2', frog_x, box_y + 45, size=12)
    
    # Fish
    fish_x = 330
    if app.selectedCharacter == 'fish':
        drawRect(fish_x - box_width//2, box_y - box_height//2, box_width, box_height, 
                fill='gold', border='yellow', borderWidth=4)
    else:
        drawRect(fish_x - box_width//2, box_y - box_height//2, box_width, box_height, 
                fill='white', border='gray', borderWidth=2)
    drawOval(fish_x, box_y - 10, 20, 12, fill='blue', border='darkBlue', borderWidth=2)
    drawPolygon(fish_x + 10, box_y - 10, fish_x + 16, box_y - 16, fish_x + 16, box_y - 4, 
                fill='blue', border='darkBlue', borderWidth=2)
    drawCircle(fish_x - 5, box_y - 10, 3, fill='white', border='black', borderWidth=1)
    drawCircle(fish_x - 5, box_y - 10, 1, fill='black')
    drawLabel('Fish', fish_x, box_y + 30, size=16, bold=True)
    drawLabel('Press 3', fish_x, box_y + 45, size=12)
    
    # Start instruction
    drawLabel('Press SPACE to Start!', 200, 320, size=24, fill='white', bold=True)

def start_onKeyPress(app, key):
    if key == '1':
        app.selectedCharacter = 'duck'
    elif key == '2':
        app.selectedCharacter = 'frog'
    elif key == '3':
        app.selectedCharacter = 'fish'
    elif key == 'space':
        reset(app)
        setActiveScreen('game')

############################################################
# Game Screen
############################################################
def game_onScreenActivate(app):
    # Game is already reset when we switch screens
    pass

def game_onKeyPress(app, key):
    if game.game_over:
        # Only allow restart after animation completes
        if key == 'r' and game.death_animation_frame >= 30:
            setActiveScreen('start')
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

def game_onStep(app):
    if game.game_over:
        # Increment death animation frame
        if game.death_animation_frame < 30:
            game.death_animation_frame += 1
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
                    game.death_type = 'road'
        
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
                    game.death_type = 'water'

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
    
    # If game is over, show death animation
    if game.game_over and game.death_type:
        drawDeathAnimation(x, y)
        return
    
    if game.character == 'duck':
        # Draw duck (yellow character)
        drawCircle(x, y - 5, 8, fill='yellow', border='orange', borderWidth=2)  # Head
        drawCircle(x, y + 5, 10, fill='yellow', border='orange', borderWidth=2)  # Body
        drawCircle(x - 3, y - 7, 2, fill='black')  # Eye
        drawCircle(x + 3, y - 7, 2, fill='black')  # Eye
        drawPolygon(x, y - 3, x - 3, y - 1, x + 3, y - 1, fill='orange')  # Beak
    
    elif game.character == 'frog':
        # Draw frog (green character)
        drawCircle(x, y, 12, fill='green', border='darkGreen', borderWidth=2)  # Body
        drawCircle(x - 5, y - 3, 5, fill='lightGreen', border='darkGreen', borderWidth=1)  # Left eye
        drawCircle(x + 5, y - 3, 5, fill='lightGreen', border='darkGreen', borderWidth=1)  # Right eye
        drawCircle(x - 5, y - 3, 2, fill='black')  # Left pupil
        drawCircle(x + 5, y - 3, 2, fill='black')  # Right pupil
        drawRect(x - 2, y + 5, 4, 2, fill='darkGreen')  # Mouth
    
    elif game.character == 'fish':
        # Draw fish (blue character)
        drawOval(x, y, 20, 12, fill='blue', border='darkBlue', borderWidth=2)  # Body
        drawPolygon(x + 10, y, x + 16, y - 6, x + 16, y + 6, fill='blue', border='darkBlue', borderWidth=2)  # Tail
        drawCircle(x - 5, y, 3, fill='white', border='black', borderWidth=1)  # Eye
        drawCircle(x - 5, y, 1, fill='black')  # Pupil

def drawDeathAnimation(x, y):
    frame = game.death_animation_frame
    
    if game.death_type == 'road':
        # Road death - squashed/impact animation
        if game.character == 'duck':
            # Duck gets flattened
            squash = min(frame / 10, 2)
            width = max(1, 20 + squash * 10)
            height = max(1, 15 - squash * 8)
            opacity = max(0, 100 - frame * 3)
            drawOval(x, y, width, height, fill='yellow', opacity=opacity)
            drawCircle(x - 5, y, 2, fill='black', opacity=opacity)
            drawCircle(x + 5, y, 2, fill='black', opacity=opacity)
            # Feathers flying
            if frame < 20:
                for i in range(3):
                    offset_x = (frame - i * 3) * 2
                    offset_y = -frame + i * 5
                    feather_opacity = max(0, 100 - frame * 5)
                    drawCircle(x + offset_x, y + offset_y, 3, fill='yellow', opacity=feather_opacity)
        
        elif game.character == 'frog':
            # Frog gets squashed
            squash = min(frame / 10, 2)
            width = max(1, 25 + squash * 10)
            height = max(1, 12 - squash * 6)
            opacity = max(0, 100 - frame * 3)
            drawOval(x, y, width, height, fill='green', opacity=opacity)
            drawCircle(x - 5, y - 5, 3, fill='lightGreen', opacity=opacity)
            drawCircle(x + 5, y - 5, 3, fill='lightGreen', opacity=opacity)
            # Stars/dazed effect
            if frame < 15:
                for i in range(4):
                    angle = (frame * 20 + i * 90) % 360
                    star_x = x + 15 * math.cos(math.radians(angle))
                    star_y = y - 20 + 15 * math.sin(math.radians(angle))
                    star_opacity = max(0, 100 - frame * 6)
                    drawStar(star_x, star_y, 5, 5, fill='yellow', opacity=star_opacity)
        
        elif game.character == 'fish':
            # Fish gets flattened
            squash = min(frame / 10, 2)
            width = max(1, 25 + squash * 10)
            height = max(1, 10 - squash * 5)
            opacity = max(0, 100 - frame * 3)
            drawOval(x, y, width, height, fill='blue', opacity=opacity)
            drawCircle(x - 5, y, 2, fill='white', opacity=opacity)
            # Bubbles
            if frame < 20:
                for i in range(3):
                    bubble_y = y - frame * 2 - i * 10
                    bubble_x = x + (i - 1) * 8
                    bubble_opacity = max(0, 100 - frame * 5)
                    drawCircle(bubble_x, bubble_y, 4, fill='lightBlue', opacity=bubble_opacity)
    
    elif game.death_type == 'water':
        # Water death - sinking/drowning animation
        sink_amount = min(frame * 2, 40)
        
        if game.character == 'duck':
            # Duck sinks with bubbles
            opacity = max(0, 100 - frame * 3)
            drawCircle(x, y + sink_amount - 5, 8, fill='yellow', border='orange', borderWidth=2, opacity=opacity)
            drawCircle(x, y + sink_amount + 5, 10, fill='yellow', border='orange', borderWidth=2, opacity=opacity)
            # X eyes when drowning
            drawLine(x - 5, y + sink_amount - 7, x - 1, y + sink_amount - 5, fill='black', lineWidth=2, opacity=opacity)
            drawLine(x - 1, y + sink_amount - 7, x - 5, y + sink_amount - 5, fill='black', lineWidth=2, opacity=opacity)
            drawLine(x + 1, y + sink_amount - 7, x + 5, y + sink_amount - 5, fill='black', lineWidth=2, opacity=opacity)
            drawLine(x + 5, y + sink_amount - 7, x + 1, y + sink_amount - 5, fill='black', lineWidth=2, opacity=opacity)
            # Bubbles rising
            if frame < 25:
                for i in range(4):
                    bubble_y = y - frame * 1.5 + i * 10
                    bubble_x = x + (i % 2) * 8 - 4
                    bubble_size = max(1, 3 + i)
                    bubble_opacity = max(0, 100 - frame * 4)
                    drawCircle(bubble_x, bubble_y, bubble_size, fill='lightBlue', opacity=bubble_opacity)
        
        elif game.character == 'frog':
            # Frog actually swims initially then sinks
            if frame < 10:
                # Swimming motion
                bob = frame % 4 - 2
                drawCircle(x, y + bob, 12, fill='green', border='darkGreen', borderWidth=2)
                drawCircle(x - 5, y + bob - 3, 5, fill='lightGreen', border='darkGreen', borderWidth=1)
                drawCircle(x + 5, y + bob - 3, 5, fill='lightGreen', border='darkGreen', borderWidth=1)
            else:
                # Then sinks
                opacity = max(0, 100 - frame * 2)
                drawCircle(x, y + sink_amount, 12, fill='green', border='darkGreen', borderWidth=2, opacity=opacity)
                # X eyes
                drawLine(x - 7, y + sink_amount - 4, x - 3, y + sink_amount - 2, fill='black', lineWidth=2, opacity=opacity)
                drawLine(x - 3, y + sink_amount - 4, x - 7, y + sink_amount - 2, fill='black', lineWidth=2, opacity=opacity)
                drawLine(x + 3, y + sink_amount - 4, x + 7, y + sink_amount - 2, fill='black', lineWidth=2, opacity=opacity)
                drawLine(x + 7, y + sink_amount - 4, x + 3, y + sink_amount - 2, fill='black', lineWidth=2, opacity=opacity)
            # Bubbles
            if frame < 25:
                for i in range(3):
                    bubble_y = y - frame * 1.5 + i * 12
                    bubble_x = x + (i - 1) * 6
                    bubble_opacity = max(0, 100 - frame * 4)
                    drawCircle(bubble_x, bubble_y, 4, fill='lightBlue', opacity=bubble_opacity)
        
        elif game.character == 'fish':
            # Fish floats upside down (ironic death)
            float_y = y - frame * 1.5
            opacity = max(0, 100 - frame * 3)
            drawOval(x, float_y, 20, 12, fill='blue', border='darkBlue', borderWidth=2, opacity=opacity, rotateAngle=180)
            drawCircle(x - 5, float_y, 2, fill='white', opacity=opacity)
            # Bubbles
            if frame < 20:
                for i in range(3):
                    bubble_y = float_y - 10 - i * 8
                    bubble_size = max(1, 3 + i)
                    bubble_opacity = max(0, 100 - frame * 5)
                    drawCircle(x, bubble_y, bubble_size, fill='lightBlue', opacity=bubble_opacity)

def game_redrawAll(app):
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
    
    # Only show game over screen after death animation completes
    if game.game_over and game.death_animation_frame >= 30:
        drawRect(0, 0, 400, 400, fill='black', opacity=80)
        drawLabel('GAME OVER!', 200, 150, size=40, fill='red', bold=True)
        drawLabel(f'Final Score: {game.score}', 200, 200, size=25, fill='white', bold=True)
        drawLabel('Press R to Restart', 200, 250, size=20, fill='white')

############################################################
# Main
############################################################
def main():
    runAppWithScreens(initialScreen='start', width=400, height=400)

main()