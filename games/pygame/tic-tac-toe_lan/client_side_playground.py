import pygame 

class PLAYER_SIDE:
    def __init__(self, surf, width, height, color = (200,200,200)):
        
        self.surf = surf
        self.width = width/3
        self.height = height/3
        self.color = color
        self.difference = 10
    
    #draw grid    
    def draw(self):
        for x_index in range(3):
            for y_index in range(3):
                pygame.draw.rect(self.surf, (25,25,25), (x_index*self.width,y_index*self.height,self.width,self.height),2)
    #draw o or circle            
    def draw_circle(self,x,y):
        pygame.draw.circle(self.surf,(25,25,25),(self.width*x+ self.width/2,self.height*y+self.height/2),self.height/2-5,5)

    #draw X or cross      
    def draw_x(self,x,y):
        pygame.draw.line(self.surf,(25,25,25),(x*self.width+self.difference,y*self.height+self.difference),(x*self.width+self.width-self.difference,y*self.height+self.height-self.difference),5)
        pygame.draw.line(self.surf,(25,25,25),(x*self.width-self.difference+self.width,y*self.height+self.difference),(x*self.width+self.difference,y*self.height+self.height-self.difference),5)
    
    #draw line over patterns
    def draw_line(self,x,y,xT,yT):
        pygame.draw.line(self.surf,(150,0,0),(x*self.width + self.width/2,y*self.height + self.height/2 ),
                            (xT*self.width+ self.width/2 ,yT*self.height+ self.height/2 ),10)